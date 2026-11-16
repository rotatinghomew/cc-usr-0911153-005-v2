import tempfile
import unittest
from pathlib import Path

from field_feedback.observations.report import ContractError, DomainRecord, Decision
from field_feedback.product_loop import Application


class FleetDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.app = Application(Path(self.tmp.name) / "fleet.db")
        self.service = self.app.fleet_delivery
        self.scope = self.service.register("vn", "m1", "v2", [f"u{i:02}" for i in range(20)])

    def publish(self, stage, version):
        record = DomainRecord("r1", {"country": "vn", "device_model": "m1", "firmware_version": "v2"},
                              stage, version, "2026-11-16T00:00:00Z")
        decision = Decision("r1", "approve", .8, ("复核通过",), (), {}, "2026-11-16T00:00:00Z")
        self.app.repository.save_record(record)
        self.app.repository.save_decision(decision)
        self.service.reconcile(record, decision)
        return record, decision

    def test_canary_delivery_survives_rollback_and_restart(self):
        self.publish("canary", 3)
        pending = [r for r in self.service.inspect()["deliveries"] if r["status"] == "pending"]
        self.assertEqual(len(pending), 2)
        item = pending[0]
        self.service.delivered(self.scope, item["unit_id"], item["intent_id"])
        self.publish("rolled_back", 4)
        rows = Application(Path(self.tmp.name) / "fleet.db").fleet_delivery.inspect()["deliveries"]
        self.assertEqual(sorted(r["status"] for r in rows), ["cancelled", "delivered"])
        with self.assertRaises(ContractError):
            self.service.delivered(self.scope, pending[1]["unit_id"], pending[1]["intent_id"])

    def test_rollout_counts_delivered_units_and_keeps_other_firmware_isolated(self):
        other = self.service.register("vn", "m1", "v3", ["x"])
        self.publish("canary", 3)
        item = self.service.inspect()["deliveries"][0]
        self.service.delivered(self.scope, item["unit_id"], item["intent_id"])
        record, decision = self.publish("rolled_out", 4)
        self.service.reconcile(record, decision)
        report = self.service.inspect()
        self.assertEqual(len(report["intents"]), 2)
        self.assertEqual(len(report["deliveries"]), 20)
        self.assertEqual(sum(r["status"] == "delivered" for r in report["deliveries"]), 1)
        self.assertFalse(any(r["scope_id"] == other for r in report["deliveries"]))

    def test_scope_replay_and_collision(self):
        self.assertEqual(self.scope, self.service.register("vn", "m1", "v2", [f"u{i:02}" for i in reversed(range(20))]))
        with self.assertRaises(ContractError):
            self.service.register("vn", "m1", "v2", ["different"])
