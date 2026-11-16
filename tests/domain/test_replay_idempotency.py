from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path

from field_feedback.observations.report import Decision, DomainRecord, RuleResult
from field_feedback.product_loop import Application, strategy_fingerprint
from field_feedback.history.release_archive import Repository


PAYLOAD = {"country": "vn", "crop_type": "rice", "device_model": "m1",
           "firmware_version": "v2", "symptom_code": "s1", "severity": 5,
           "weather": "dry", "terrain": "flat", "operator_skill": 3,
           "reproduction_rate": 0.5, "affected_units": 10, "translation_confidence": 0.8}


class ReplayIdempotencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app = Application(Path(self.temp.name) / "replay.db")

    def test_identical_evidence_replay_returns_existing_judgement(self):
        record = DomainRecord("r1", dict(PAYLOAD), "reported", 1)
        first_record, first_decision = self.app.process(record)
        second_record, second_decision = self.app.process(DomainRecord("r1", dict(PAYLOAD), "reported", 1))

        self.assertEqual(second_record.fingerprint, first_record.fingerprint)
        self.assertEqual(second_decision.fingerprint, first_decision.fingerprint)
        counts = self.app.repository.snapshot()["counts"]
        self.assertEqual(counts["analyses"], 1)
        self.assertEqual(counts["decisions"], 1)
        self.assertEqual(counts["record_versions"], first_record.version)

    def test_repeated_replay_never_advances_the_stage(self):
        record = DomainRecord("r1", dict(PAYLOAD), "reported", 1)
        advanced, _ = self.app.process(record)
        expected = (advanced.state, advanced.version)
        for _ in range(5):
            replayed, _ = self.app.process(DomainRecord("r1", dict(PAYLOAD), "reported", 1))
            self.assertEqual((replayed.state, replayed.version), expected)

    def test_revised_report_creates_new_evidence_version_and_analysis(self):
        first_record, _ = self.app.process(DomainRecord("r1", dict(PAYLOAD), "reported", 1))
        revised_payload = dict(PAYLOAD, affected_units=42)
        revised_record, revised_decision = self.app.process(
            DomainRecord("r1", revised_payload, "reported", 1))

        self.assertNotEqual(revised_record.evidence_fingerprint, first_record.evidence_fingerprint)
        self.assertEqual(revised_record.version, first_record.version + 1)
        rows = self.app.repository.analysis_rows()
        self.assertEqual(len(rows), 2)
        old_rows = [row for row in rows if row["record_version"] == first_record.version]
        self.assertEqual(len(old_rows), 1)
        self.assertEqual(old_rows[0]["evidence_fingerprint"], first_record.evidence_fingerprint)

    def test_unchanged_evidence_with_new_strategy_records_basis_without_stage_advance(self):
        first_record, _ = self.app.process(DomainRecord("r1", dict(PAYLOAD), "reported", 1))
        self.app.context["approve_threshold"] = 0.99
        replayed, _ = self.app.process(DomainRecord("r1", dict(PAYLOAD), "reported", 1))

        self.assertEqual((replayed.state, replayed.version), (first_record.state, first_record.version))
        rows = self.app.repository.analysis_rows()
        self.assertEqual(len(rows), 2)
        self.assertEqual(len({row["strategy_fingerprint"] for row in rows}), 2)

    def test_strategy_fingerprint_is_stable_and_distinguishes_policy(self):
        left = strategy_fingerprint({"approve_threshold": 0.62})
        right = strategy_fingerprint({"approve_threshold": 0.62})
        changed = strategy_fingerprint({"approve_threshold": 0.99})
        self.assertEqual(left, right)
        self.assertNotEqual(left, changed)

    def test_concurrent_identical_replays_collapse_to_one_analysis(self):
        errors: list[Exception] = []

        def worker() -> None:
            try:
                for _ in range(5):
                    self.app.process(DomainRecord("r1", dict(PAYLOAD), "reported", 1))
            except Exception as exc:  # pragma: no cover - asserted below
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(errors, [])
        counts = self.app.repository.snapshot()["counts"]
        self.assertEqual(counts["analyses"], 1)
        self.assertEqual(counts["decisions"], 1)
        self.assertEqual(self.app.repository.verify_chain(), [])

    def test_failure_inside_process_rolls_back_the_whole_unit_of_work(self):
        self.app.process(DomainRecord("r1", dict(PAYLOAD), "reported", 1))
        before = self.app.repository.snapshot()["counts"]

        def boom(record, decision):  # pragma: no cover - replaces collaborator
            raise RuntimeError("service interruption")

        self.app.fleet_delivery.reconcile = boom
        with self.assertRaises(RuntimeError):
            self.app.process(DomainRecord("r1", dict(PAYLOAD, affected_units=77), "reported", 1))
        self.assertEqual(self.app.repository.snapshot()["counts"], before)
        self.assertEqual(self.app.repository.verify_chain(), [])

    def test_analysis_rows_link_decision_to_evidence_and_strategy(self):
        record, decision = self.app.process(DomainRecord("r1", dict(PAYLOAD), "reported", 1))
        row = self.app.repository.analysis_rows()[0]
        self.assertEqual(row["record_id"], "r1")
        self.assertEqual(row["record_version"], record.version)
        self.assertEqual(row["evidence_fingerprint"], record.evidence_fingerprint)
        self.assertEqual(row["decision_id"], decision.fingerprint)
        self.assertEqual(row["strategy_fingerprint"], strategy_fingerprint({}))
        self.assertEqual(row["to_state"], record.state)


class ReplayFleetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app = Application(Path(self.temp.name) / "fleet-replay.db")
        self.scope = self.app.fleet_delivery.register(
            "vn", "m1", "v2", [f"u{i:02}" for i in range(20)])

    def publish(self, stage, version, timestamp):
        record = DomainRecord("r1", {"country": "vn", "device_model": "m1", "firmware_version": "v2"},
                              stage, version, timestamp)
        decision = Decision("r1", "approve", .8, ("复核通过",), (), {}, timestamp)
        if version == 1:
            self.app.repository.save_record(record)
        else:
            self.app.repository.save_record(record, expected_version=version - 1)
        self.app.repository.save_decision(decision)
        for _ in range(3):
            self.app.fleet_delivery.reconcile(record, decision)
        return record, decision

    def test_replayed_reconcile_does_not_duplicate_or_conflict_intents(self):
        canary, canary_decision = self.publish("canary", 1, "2026-11-16T00:00:00Z")
        report = self.app.fleet_delivery.inspect()
        self.assertEqual(len(report["intents"]), 1)
        self.assertEqual(sum(row["status"] == "pending" for row in report["deliveries"]), 2)

        item = report["deliveries"][0]
        self.app.fleet_delivery.delivered(self.scope, item["unit_id"], item["intent_id"])
        self.publish("rolled_out", 2, "2026-11-16T00:00:01Z")

        final = self.app.fleet_delivery.inspect()
        self.assertEqual(len(final["intents"]), 2)
        self.assertEqual(len({row["intent_id"] for row in final["intents"]}), 2)
        self.assertEqual(len(final["deliveries"]), 20)
        self.assertEqual(sum(row["status"] == "delivered" for row in final["deliveries"]), 1)
        self.assertEqual(self.app.repository.verify_chain(), [])


class DecisionRoundTripTests(unittest.TestCase):
    def test_decision_and_rule_result_round_trip_through_json(self):
        rule = RuleResult("check_country_presence", True, 0.7, "info", "ok", {"field": "country"})
        decision = Decision("r1", "approve", 0.81, ("a", "b"), (rule,), {"rollback_risk": 0.2},
                            "2026-11-16T00:00:00Z")
        restored = Decision.from_dict(decision.as_dict())
        self.assertEqual(restored.fingerprint, decision.fingerprint)
        self.assertEqual(restored.rule_results[0].code, rule.code)
        self.assertEqual(restored.rule_results[0].evidence, rule.evidence)


class FinishedRunReplayTests(unittest.TestCase):
    FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "acceptance.json"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.app = Application(self.root / "run.db")
        self.fixture = json.loads(self.FIXTURE.read_text(encoding="utf-8"))

    def test_concurrent_fixture_runs_share_one_finished_result(self):
        results: list[dict] = []
        errors: list[Exception] = []

        def worker() -> None:
            try:
                results.append(self.app.run_fixture(self.fixture, self.root / "output"))
            except Exception as exc:  # pragma: no cover - asserted below
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(errors, [])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["run_id"], results[1]["run_id"])
        counts = self.app.repository.snapshot()["counts"]
        self.assertEqual(counts["analyses"], 8)
        self.assertEqual(counts["decisions"], 8)

    def test_inspect_exposes_analysis_ledger_and_summary_carries_evidence(self):
        self.app.run_fixture(self.fixture, self.root / "output")
        inspect = self.app.inspect()
        self.assertEqual(len(inspect["analyses"]), 8)
        summary = json.loads((self.root / "output" / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["analysis_count"], 8)
        self.assertTrue(all("evidence_fingerprint" in row for row in summary["analyses"]))


if __name__ == "__main__":
    unittest.main()
