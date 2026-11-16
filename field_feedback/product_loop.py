from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from field_feedback.observations.report import ContractError, Decision, DomainRecord, records_from_fixture, stable_hash
from field_feedback.history.release_archive import Repository
from field_feedback.releases.progressive_delivery import advance_for_outcome, decide
from field_feedback.insights.regional_digest import export_bundle, verify_bundle
from field_feedback.triage.multilingual_clusters import derive_context
from field_feedback.releases.fleet_delivery import FleetDelivery


def strategy_fingerprint(context: Mapping[str, Any]) -> str:
    """对分析策略（评分上下文）做稳定指纹。

    同一份证据在同一策略下的重复分析视为同一次请求的重试；
    策略被调整后再分析，才会被识别为一次新的分析依据。
    """
    return stable_hash(context)


class Application:
    def __init__(self, database: str | Path, context: Mapping[str, Any] | None = None):
        self.repository = Repository(database)
        self.fleet_delivery = FleetDelivery(self.repository)
        self.context = dict(context or {})

    def ingest(self, record: DomainRecord) -> DomainRecord:
        with self.repository.unit_of_work():
            current = self.repository.get_record(record.record_id)
            if current is None:
                self.repository.save_record(record)
                return record
            if current.evidence_fingerprint == record.evidence_fingerprint:
                # 同一份证据再次导入：保留既有版本与状态，不制造新版本。
                return current
            replacement = DomainRecord(record.record_id, record.payload, current.state,
                                       current.version + 1, record.occurred_at, record.source)
            self.repository.save_record(replacement, expected_version=current.version)
            return replacement

    def process(self, record: DomainRecord) -> tuple[DomainRecord, Decision]:
        """处理一份现场反馈，并保证整次处理在单个数据库事务内完成。

        - 同一证据 + 同一策略的重复分析：直接返回已落库的有效评议，不推进阶段、不增生记录。
        - 同一证据 + 新策略的再分析：形成新的分析依据，但只有证据版本的首次评议能推进阶段。
        - 真实修订后的报告：产生新的证据版本与新的分析依据，由当前流程决定是否推进。
        """
        with self.repository.unit_of_work():
            stored = self.ingest(record)
            # 策略指纹只包含显式配置的评议策略；derive_context 得出的是当前机队状态，
            # 会随其它报告的处理顺序变化，属于决策输入而非请求身份，因此不参与幂等判定。
            strategy_fp = strategy_fingerprint(self.context)
            context = dict(self.context)
            context.update(derive_context(stored, self.repository))

            prior = self.repository.get_analysis(stored.record_id, stored.version, strategy_fp)
            if prior is not None:
                decision = self.repository.get_decision(prior["decision_id"])
                if decision is None:  # pragma: no cover - 外键保证不会发生
                    raise ContractError("stored analysis references a missing decision")
                return self.repository.get_record(stored.record_id) or stored, decision

            decision = decide(stored, context)
            self.repository.save_decision(decision)

            from_state = stored.state
            # 阶段推进只允许由该证据版本的首次评议触发；同证据重试或换策略重算都不能再推一步。
            version_seen = self.repository.has_analysis_for_version(stored.record_id, stored.version)
            if version_seen:
                advanced = stored
            else:
                advanced = advance_for_outcome(stored, decision)
            if advanced.fingerprint != stored.fingerprint:
                self.repository.save_record(advanced, expected_version=stored.version)

            self.repository.save_analysis(advanced, decision, strategy_fp, from_state, advanced.state)
            self.fleet_delivery.reconcile(advanced, decision)
            return advanced, decision

    def run_fixture(self, fixture: Mapping[str, Any], output: str | Path) -> dict[str, Any]:
        records = records_from_fixture(fixture)
        fixture_hash = stable_hash(fixture)
        run_id = self.repository.begin_run(fixture_hash, len(records))
        completed = self.repository.completed_run(run_id)
        if completed is not None:
            return completed
        decisions: dict[str, Decision] = {}
        final_records: list[DomainRecord] = []
        # 每份报告各自在单个事务内完成；中途失败会整体回滚该报告，已完成报告的结果仍然完整。
        for record in records:
            final_record, decision = self.process(record)
            final_records.append(final_record)
            decisions[record.record_id] = decision
        snapshot = self.repository.snapshot()
        snapshot["fleet_delivery"] = self.fleet_delivery.inspect()
        if snapshot["chain_errors"]:
            raise ContractError("audit chain verification failed")
        analyses = self.repository.analysis_rows()
        manifest = export_bundle(output, final_records, decisions, snapshot,
                                 self.repository.event_rows(), analyses)
        result = {"run_id": run_id, "fixture_hash": fixture_hash, "records": len(final_records),
                  "decisions": len(decisions), "manifest": manifest, "snapshot": snapshot}
        return self.repository.finish_run(run_id, result)

    def inspect(self) -> dict[str, Any]:
        return {"snapshot": self.repository.snapshot(), "records": [record.__dict__ for record in self.repository.list_records()],
                "decisions": self.repository.decision_rows(), "analyses": self.repository.analysis_rows(),
                "fleet_delivery": self.fleet_delivery.inspect()}


def load_fixture(path: str | Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read fixture: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("fixture root must be an object")
    return value


def run(fixture_path: str | Path, database: str | Path, output: str | Path,
        context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return Application(database, context).run_fixture(load_fixture(fixture_path), output)


def verify(database: str | Path, output: str | Path) -> dict[str, Any]:
    repository = Repository(database)
    chain_errors = repository.verify_chain()
    bundle_errors = verify_bundle(output)
    return {"ok": not chain_errors and not bundle_errors, "chain_errors": chain_errors,
            "bundle_errors": bundle_errors, "snapshot": repository.snapshot()}
