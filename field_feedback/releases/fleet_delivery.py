"""按发布阶段分配设备升级名额，并保留已送达事实。"""
from __future__ import annotations

import json
import math

from field_feedback.observations.report import ContractError, DomainRecord, Decision, stable_hash


class FleetDelivery:
    def __init__(self, repository):
        self.repository = repository
        with repository.connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS fleet_scopes(
                    scope_id TEXT PRIMARY KEY, country TEXT NOT NULL, model TEXT NOT NULL,
                    firmware TEXT NOT NULL, units_json TEXT NOT NULL,
                    UNIQUE(country,model,firmware));
                CREATE TABLE IF NOT EXISTS rollout_intents(
                    intent_id TEXT PRIMARY KEY, scope_id TEXT NOT NULL,
                    record_id TEXT NOT NULL, record_version INTEGER NOT NULL,
                    stage TEXT NOT NULL, decision_id TEXT NOT NULL, target_count INTEGER NOT NULL,
                    UNIQUE(record_id,record_version,scope_id));
                CREATE TABLE IF NOT EXISTS fleet_deliveries(
                    scope_id TEXT NOT NULL, unit_id TEXT NOT NULL, intent_id TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('pending','delivered','cancelled')),
                    PRIMARY KEY(scope_id,unit_id));
            """)

    def register(self, country: str, model: str, firmware: str, units: list[str]) -> str:
        if not all(isinstance(v, str) and v.strip() for v in (country, model, firmware)):
            raise ContractError("地区、机型和固件不能为空")
        if not units or any(not isinstance(u, str) or not u.strip() for u in units) or len(set(units)) != len(units):
            raise ContractError("设备名单须非空且标识唯一")
        scope_id = stable_hash([country, model, firmware])[:24]
        encoded = json.dumps(sorted(units), ensure_ascii=False)
        with self.repository.transaction() as c:
            old = c.execute("SELECT units_json FROM fleet_scopes WHERE scope_id=?", (scope_id,)).fetchone()
            if old and old[0] != encoded:
                raise ContractError("已登记发布范围的设备名单不可改写")
            c.execute("INSERT OR IGNORE INTO fleet_scopes VALUES(?,?,?,?,?)",
                      (scope_id, country, model, firmware, encoded))
        return scope_id

    def reconcile(self, record: DomainRecord, decision: Decision) -> None:
        if decision.record_id != record.record_id:
            raise ContractError("发布评议不属于当前现场报告")
        if record.state not in {"canary", "rolled_out", "rolled_back"}:
            return
        payload = record.payload
        with self.repository.transaction() as c:
            evidence = c.execute("SELECT fingerprint FROM record_versions WHERE record_id=? AND version=?",
                                 (record.record_id, record.version)).fetchone()
            if evidence is None or evidence[0] != record.fingerprint or not c.execute(
                "SELECT 1 FROM decisions WHERE record_id=? AND decision_id=?",
                (record.record_id, decision.fingerprint)
            ).fetchone():
                raise ContractError("发布阶段及评议必须先形成可追溯记录")
            scope = c.execute("SELECT * FROM fleet_scopes WHERE country=? AND model=? AND firmware=?",
                              (str(payload.get("country", "")), str(payload.get("device_model", "")),
                               str(payload.get("firmware_version", "")))).fetchone()
            if scope is None:
                return
            units = json.loads(scope["units_json"])
            target = 0 if record.state == "rolled_back" else (
                len(units) if record.state == "rolled_out" else max(1, math.ceil(len(units) / 10)))
            intent_id = stable_hash([scope["scope_id"], record.record_id, record.version])[:24]
            old = c.execute("SELECT * FROM rollout_intents WHERE intent_id=?", (intent_id,)).fetchone()
            if old:
                if old["stage"] != record.state or old["decision_id"] != decision.fingerprint:
                    raise ContractError("同一发布版本包含冲突评议")
                return
            c.execute("INSERT INTO rollout_intents VALUES(?,?,?,?,?,?,?)",
                      (intent_id, scope["scope_id"], record.record_id, record.version,
                       record.state, decision.fingerprint, target))
            if record.state == "rolled_back":
                c.execute("UPDATE fleet_deliveries SET status='cancelled',intent_id=? "
                          "WHERE scope_id=? AND status='pending'", (intent_id, scope["scope_id"]))
                return
            delivered = {r[0] for r in c.execute(
                "SELECT unit_id FROM fleet_deliveries WHERE scope_id=? AND status='delivered'",
                (scope["scope_id"],))}
            wanted = set(sorted(set(units) - delivered)[:max(0, target - len(delivered))])
            c.execute("UPDATE fleet_deliveries SET status='cancelled',intent_id=? "
                      "WHERE scope_id=? AND status='pending'", (intent_id, scope["scope_id"]))
            for unit in sorted(wanted):
                c.execute("INSERT INTO fleet_deliveries VALUES(?,?,?,'pending') "
                          "ON CONFLICT(scope_id,unit_id) DO UPDATE SET intent_id=excluded.intent_id,status='pending'",
                          (scope["scope_id"], unit, intent_id))

    def delivered(self, scope_id: str, unit_id: str, intent_id: str) -> None:
        with self.repository.transaction() as c:
            row = c.execute("SELECT * FROM fleet_deliveries WHERE scope_id=? AND unit_id=?",
                            (scope_id, unit_id)).fetchone()
            if row is None or row["intent_id"] != intent_id or row["status"] == "cancelled":
                raise ContractError("升级名额已撤回或不属于当前发布意图")
            c.execute("UPDATE fleet_deliveries SET status='delivered' WHERE scope_id=? AND unit_id=?",
                      (scope_id, unit_id))

    def inspect(self) -> dict:
        with self.repository.connect() as c:
            return {"intents": [dict(r) for r in c.execute("SELECT * FROM rollout_intents ORDER BY intent_id")],
                    "deliveries": [dict(r) for r in c.execute("SELECT * FROM fleet_deliveries ORDER BY scope_id,unit_id")]}
