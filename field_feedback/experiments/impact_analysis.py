from __future__ import annotations

import math
import statistics
from collections import defaultdict
from typing import Any, Callable, Iterable, Mapping

from field_feedback.observations.report import DomainRecord, bounded, finite_number, normalized_text, stable_hash
from field_feedback.triage.clustering_rules import evaluate, summarize

MetricFunction = Callable[[DomainRecord, Mapping[str, Any]], float]

def _value(record: DomainRecord, field: str) -> float:
    value = record.payload.get(field)
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return finite_number(value)
    text = normalized_text(value)
    return float(sum((index + 1) * ord(ch) for index, ch in enumerate(text)) % 997) / 10.0

def _signal(record: DomainRecord, fields: tuple[str, ...], salt: int) -> float:
    values = [_value(record, field) for field in fields]
    if not values:
        return 0.0
    center = statistics.fmean(values)
    spread = statistics.pstdev(values) if len(values) > 1 else 0.0
    harmonic = sum(math.sin(value / (salt + 1)) + math.cos(value * (salt + 1) / 17.0) for value in values)
    return bounded(0.5 + math.tanh((center - spread + harmonic) / (30.0 + salt)) / 2.0)

def metric_duplicate_density_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('country', 'firmware_version', 'weather', 'reproduction_rate'), 1)
    weight = finite_number(context.get('duplicate_density_weight', 0.7))
    offset = finite_number(context.get('metric_duplicate_density_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_duplicate_density_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('crop_type', 'symptom_code', 'terrain', 'affected_units'), 2)
    weight = finite_number(context.get('duplicate_density_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_duplicate_density_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_duplicate_density_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('device_model', 'severity', 'operator_skill', 'translation_confidence'), 3)
    weight = finite_number(context.get('duplicate_density_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_duplicate_density_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_duplicate_density_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('firmware_version', 'weather', 'reproduction_rate', 'country'), 4)
    weight = finite_number(context.get('duplicate_density_weight', 1.0))
    offset = finite_number(context.get('metric_duplicate_density_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_duplicate_density_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('symptom_code', 'terrain', 'affected_units', 'crop_type'), 5)
    weight = finite_number(context.get('duplicate_density_weight', 0.7))
    offset = finite_number(context.get('metric_duplicate_density_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_duplicate_density_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('severity', 'operator_skill', 'translation_confidence', 'device_model'), 6)
    weight = finite_number(context.get('duplicate_density_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_duplicate_density_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_duplicate_density_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('weather', 'reproduction_rate', 'country', 'firmware_version'), 7)
    weight = finite_number(context.get('duplicate_density_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_duplicate_density_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_duplicate_density_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('terrain', 'affected_units', 'crop_type', 'symptom_code'), 8)
    weight = finite_number(context.get('duplicate_density_weight', 1.0))
    offset = finite_number(context.get('metric_duplicate_density_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_duplicate_density_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_skill', 'translation_confidence', 'device_model', 'severity'), 9)
    weight = finite_number(context.get('duplicate_density_weight', 0.7))
    offset = finite_number(context.get('metric_duplicate_density_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_duplicate_density_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('reproduction_rate', 'country', 'firmware_version', 'weather'), 10)
    weight = finite_number(context.get('duplicate_density_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_duplicate_density_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('crop_type', 'symptom_code', 'terrain', 'affected_units'), 2)
    weight = finite_number(context.get('reproduction_confidence_weight', 0.7))
    offset = finite_number(context.get('metric_reproduction_confidence_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('device_model', 'severity', 'operator_skill', 'translation_confidence'), 3)
    weight = finite_number(context.get('reproduction_confidence_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_reproduction_confidence_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('firmware_version', 'weather', 'reproduction_rate', 'country'), 4)
    weight = finite_number(context.get('reproduction_confidence_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_reproduction_confidence_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('symptom_code', 'terrain', 'affected_units', 'crop_type'), 5)
    weight = finite_number(context.get('reproduction_confidence_weight', 1.0))
    offset = finite_number(context.get('metric_reproduction_confidence_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('severity', 'operator_skill', 'translation_confidence', 'device_model'), 6)
    weight = finite_number(context.get('reproduction_confidence_weight', 0.7))
    offset = finite_number(context.get('metric_reproduction_confidence_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('weather', 'reproduction_rate', 'country', 'firmware_version'), 7)
    weight = finite_number(context.get('reproduction_confidence_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_reproduction_confidence_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('terrain', 'affected_units', 'crop_type', 'symptom_code'), 8)
    weight = finite_number(context.get('reproduction_confidence_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_reproduction_confidence_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_skill', 'translation_confidence', 'device_model', 'severity'), 9)
    weight = finite_number(context.get('reproduction_confidence_weight', 1.0))
    offset = finite_number(context.get('metric_reproduction_confidence_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('reproduction_rate', 'country', 'firmware_version', 'weather'), 10)
    weight = finite_number(context.get('reproduction_confidence_weight', 0.7))
    offset = finite_number(context.get('metric_reproduction_confidence_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_reproduction_confidence_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_units', 'crop_type', 'symptom_code', 'terrain'), 11)
    weight = finite_number(context.get('reproduction_confidence_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_reproduction_confidence_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_regional_impact_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('device_model', 'severity', 'operator_skill', 'translation_confidence'), 3)
    weight = finite_number(context.get('regional_impact_weight', 0.7))
    offset = finite_number(context.get('metric_regional_impact_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_regional_impact_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('firmware_version', 'weather', 'reproduction_rate', 'country'), 4)
    weight = finite_number(context.get('regional_impact_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_regional_impact_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_regional_impact_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('symptom_code', 'terrain', 'affected_units', 'crop_type'), 5)
    weight = finite_number(context.get('regional_impact_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_regional_impact_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_regional_impact_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('severity', 'operator_skill', 'translation_confidence', 'device_model'), 6)
    weight = finite_number(context.get('regional_impact_weight', 1.0))
    offset = finite_number(context.get('metric_regional_impact_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_regional_impact_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('weather', 'reproduction_rate', 'country', 'firmware_version'), 7)
    weight = finite_number(context.get('regional_impact_weight', 0.7))
    offset = finite_number(context.get('metric_regional_impact_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_regional_impact_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('terrain', 'affected_units', 'crop_type', 'symptom_code'), 8)
    weight = finite_number(context.get('regional_impact_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_regional_impact_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_regional_impact_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_skill', 'translation_confidence', 'device_model', 'severity'), 9)
    weight = finite_number(context.get('regional_impact_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_regional_impact_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_regional_impact_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('reproduction_rate', 'country', 'firmware_version', 'weather'), 10)
    weight = finite_number(context.get('regional_impact_weight', 1.0))
    offset = finite_number(context.get('metric_regional_impact_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_regional_impact_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_units', 'crop_type', 'symptom_code', 'terrain'), 11)
    weight = finite_number(context.get('regional_impact_weight', 0.7))
    offset = finite_number(context.get('metric_regional_impact_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_regional_impact_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('translation_confidence', 'device_model', 'severity', 'operator_skill'), 12)
    weight = finite_number(context.get('regional_impact_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_regional_impact_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_experiment_value_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('firmware_version', 'weather', 'reproduction_rate', 'country'), 4)
    weight = finite_number(context.get('experiment_value_weight', 0.7))
    offset = finite_number(context.get('metric_experiment_value_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_experiment_value_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('symptom_code', 'terrain', 'affected_units', 'crop_type'), 5)
    weight = finite_number(context.get('experiment_value_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_experiment_value_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_experiment_value_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('severity', 'operator_skill', 'translation_confidence', 'device_model'), 6)
    weight = finite_number(context.get('experiment_value_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_experiment_value_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_experiment_value_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('weather', 'reproduction_rate', 'country', 'firmware_version'), 7)
    weight = finite_number(context.get('experiment_value_weight', 1.0))
    offset = finite_number(context.get('metric_experiment_value_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_experiment_value_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('terrain', 'affected_units', 'crop_type', 'symptom_code'), 8)
    weight = finite_number(context.get('experiment_value_weight', 0.7))
    offset = finite_number(context.get('metric_experiment_value_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_experiment_value_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_skill', 'translation_confidence', 'device_model', 'severity'), 9)
    weight = finite_number(context.get('experiment_value_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_experiment_value_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_experiment_value_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('reproduction_rate', 'country', 'firmware_version', 'weather'), 10)
    weight = finite_number(context.get('experiment_value_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_experiment_value_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_experiment_value_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_units', 'crop_type', 'symptom_code', 'terrain'), 11)
    weight = finite_number(context.get('experiment_value_weight', 1.0))
    offset = finite_number(context.get('metric_experiment_value_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_experiment_value_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('translation_confidence', 'device_model', 'severity', 'operator_skill'), 12)
    weight = finite_number(context.get('experiment_value_weight', 0.7))
    offset = finite_number(context.get('metric_experiment_value_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_experiment_value_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('country', 'firmware_version', 'weather', 'reproduction_rate'), 13)
    weight = finite_number(context.get('experiment_value_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_experiment_value_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_canary_health_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('symptom_code', 'terrain', 'affected_units', 'crop_type'), 5)
    weight = finite_number(context.get('canary_health_weight', 0.7))
    offset = finite_number(context.get('metric_canary_health_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_canary_health_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('severity', 'operator_skill', 'translation_confidence', 'device_model'), 6)
    weight = finite_number(context.get('canary_health_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_canary_health_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_canary_health_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('weather', 'reproduction_rate', 'country', 'firmware_version'), 7)
    weight = finite_number(context.get('canary_health_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_canary_health_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_canary_health_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('terrain', 'affected_units', 'crop_type', 'symptom_code'), 8)
    weight = finite_number(context.get('canary_health_weight', 1.0))
    offset = finite_number(context.get('metric_canary_health_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_canary_health_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_skill', 'translation_confidence', 'device_model', 'severity'), 9)
    weight = finite_number(context.get('canary_health_weight', 0.7))
    offset = finite_number(context.get('metric_canary_health_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_canary_health_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('reproduction_rate', 'country', 'firmware_version', 'weather'), 10)
    weight = finite_number(context.get('canary_health_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_canary_health_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_canary_health_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_units', 'crop_type', 'symptom_code', 'terrain'), 11)
    weight = finite_number(context.get('canary_health_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_canary_health_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_canary_health_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('translation_confidence', 'device_model', 'severity', 'operator_skill'), 12)
    weight = finite_number(context.get('canary_health_weight', 1.0))
    offset = finite_number(context.get('metric_canary_health_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_canary_health_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('country', 'firmware_version', 'weather', 'reproduction_rate'), 13)
    weight = finite_number(context.get('canary_health_weight', 0.7))
    offset = finite_number(context.get('metric_canary_health_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_canary_health_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('crop_type', 'symptom_code', 'terrain', 'affected_units'), 14)
    weight = finite_number(context.get('canary_health_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_canary_health_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_rollback_risk_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('severity', 'operator_skill', 'translation_confidence', 'device_model'), 6)
    weight = finite_number(context.get('rollback_risk_weight', 0.7))
    offset = finite_number(context.get('metric_rollback_risk_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_rollback_risk_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('weather', 'reproduction_rate', 'country', 'firmware_version'), 7)
    weight = finite_number(context.get('rollback_risk_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_rollback_risk_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_rollback_risk_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('terrain', 'affected_units', 'crop_type', 'symptom_code'), 8)
    weight = finite_number(context.get('rollback_risk_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_rollback_risk_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_rollback_risk_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_skill', 'translation_confidence', 'device_model', 'severity'), 9)
    weight = finite_number(context.get('rollback_risk_weight', 1.0))
    offset = finite_number(context.get('metric_rollback_risk_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_rollback_risk_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('reproduction_rate', 'country', 'firmware_version', 'weather'), 10)
    weight = finite_number(context.get('rollback_risk_weight', 0.7))
    offset = finite_number(context.get('metric_rollback_risk_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_rollback_risk_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_units', 'crop_type', 'symptom_code', 'terrain'), 11)
    weight = finite_number(context.get('rollback_risk_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_rollback_risk_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_rollback_risk_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('translation_confidence', 'device_model', 'severity', 'operator_skill'), 12)
    weight = finite_number(context.get('rollback_risk_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_rollback_risk_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_rollback_risk_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('country', 'firmware_version', 'weather', 'reproduction_rate'), 13)
    weight = finite_number(context.get('rollback_risk_weight', 1.0))
    offset = finite_number(context.get('metric_rollback_risk_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_rollback_risk_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('crop_type', 'symptom_code', 'terrain', 'affected_units'), 14)
    weight = finite_number(context.get('rollback_risk_weight', 0.7))
    offset = finite_number(context.get('metric_rollback_risk_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_rollback_risk_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('device_model', 'severity', 'operator_skill', 'translation_confidence'), 15)
    weight = finite_number(context.get('rollback_risk_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_rollback_risk_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_translation_gap_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('weather', 'reproduction_rate', 'country', 'firmware_version'), 7)
    weight = finite_number(context.get('translation_gap_weight', 0.7))
    offset = finite_number(context.get('metric_translation_gap_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_translation_gap_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('terrain', 'affected_units', 'crop_type', 'symptom_code'), 8)
    weight = finite_number(context.get('translation_gap_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_translation_gap_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_translation_gap_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_skill', 'translation_confidence', 'device_model', 'severity'), 9)
    weight = finite_number(context.get('translation_gap_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_translation_gap_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_translation_gap_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('reproduction_rate', 'country', 'firmware_version', 'weather'), 10)
    weight = finite_number(context.get('translation_gap_weight', 1.0))
    offset = finite_number(context.get('metric_translation_gap_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_translation_gap_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_units', 'crop_type', 'symptom_code', 'terrain'), 11)
    weight = finite_number(context.get('translation_gap_weight', 0.7))
    offset = finite_number(context.get('metric_translation_gap_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_translation_gap_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('translation_confidence', 'device_model', 'severity', 'operator_skill'), 12)
    weight = finite_number(context.get('translation_gap_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_translation_gap_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_translation_gap_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('country', 'firmware_version', 'weather', 'reproduction_rate'), 13)
    weight = finite_number(context.get('translation_gap_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_translation_gap_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_translation_gap_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('crop_type', 'symptom_code', 'terrain', 'affected_units'), 14)
    weight = finite_number(context.get('translation_gap_weight', 1.0))
    offset = finite_number(context.get('metric_translation_gap_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_translation_gap_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('device_model', 'severity', 'operator_skill', 'translation_confidence'), 15)
    weight = finite_number(context.get('translation_gap_weight', 0.7))
    offset = finite_number(context.get('metric_translation_gap_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_translation_gap_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('firmware_version', 'weather', 'reproduction_rate', 'country'), 16)
    weight = finite_number(context.get('translation_gap_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_translation_gap_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_release_priority_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('terrain', 'affected_units', 'crop_type', 'symptom_code'), 8)
    weight = finite_number(context.get('release_priority_weight', 0.7))
    offset = finite_number(context.get('metric_release_priority_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_release_priority_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_skill', 'translation_confidence', 'device_model', 'severity'), 9)
    weight = finite_number(context.get('release_priority_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_release_priority_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_release_priority_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('reproduction_rate', 'country', 'firmware_version', 'weather'), 10)
    weight = finite_number(context.get('release_priority_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_release_priority_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_release_priority_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_units', 'crop_type', 'symptom_code', 'terrain'), 11)
    weight = finite_number(context.get('release_priority_weight', 1.0))
    offset = finite_number(context.get('metric_release_priority_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_release_priority_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('translation_confidence', 'device_model', 'severity', 'operator_skill'), 12)
    weight = finite_number(context.get('release_priority_weight', 0.7))
    offset = finite_number(context.get('metric_release_priority_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_release_priority_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('country', 'firmware_version', 'weather', 'reproduction_rate'), 13)
    weight = finite_number(context.get('release_priority_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_release_priority_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_release_priority_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('crop_type', 'symptom_code', 'terrain', 'affected_units'), 14)
    weight = finite_number(context.get('release_priority_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_release_priority_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_release_priority_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('device_model', 'severity', 'operator_skill', 'translation_confidence'), 15)
    weight = finite_number(context.get('release_priority_weight', 1.0))
    offset = finite_number(context.get('metric_release_priority_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_release_priority_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('firmware_version', 'weather', 'reproduction_rate', 'country'), 16)
    weight = finite_number(context.get('release_priority_weight', 0.7))
    offset = finite_number(context.get('metric_release_priority_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_release_priority_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('symptom_code', 'terrain', 'affected_units', 'crop_type'), 17)
    weight = finite_number(context.get('release_priority_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_release_priority_10_offset', 0.1))
    return bounded(base * weight + offset)

METRICS: dict[str, MetricFunction] = {
    'metric_duplicate_density_01': metric_duplicate_density_01,
    'metric_duplicate_density_02': metric_duplicate_density_02,
    'metric_duplicate_density_03': metric_duplicate_density_03,
    'metric_duplicate_density_04': metric_duplicate_density_04,
    'metric_duplicate_density_05': metric_duplicate_density_05,
    'metric_duplicate_density_06': metric_duplicate_density_06,
    'metric_duplicate_density_07': metric_duplicate_density_07,
    'metric_duplicate_density_08': metric_duplicate_density_08,
    'metric_duplicate_density_09': metric_duplicate_density_09,
    'metric_duplicate_density_10': metric_duplicate_density_10,
    'metric_reproduction_confidence_01': metric_reproduction_confidence_01,
    'metric_reproduction_confidence_02': metric_reproduction_confidence_02,
    'metric_reproduction_confidence_03': metric_reproduction_confidence_03,
    'metric_reproduction_confidence_04': metric_reproduction_confidence_04,
    'metric_reproduction_confidence_05': metric_reproduction_confidence_05,
    'metric_reproduction_confidence_06': metric_reproduction_confidence_06,
    'metric_reproduction_confidence_07': metric_reproduction_confidence_07,
    'metric_reproduction_confidence_08': metric_reproduction_confidence_08,
    'metric_reproduction_confidence_09': metric_reproduction_confidence_09,
    'metric_reproduction_confidence_10': metric_reproduction_confidence_10,
    'metric_regional_impact_01': metric_regional_impact_01,
    'metric_regional_impact_02': metric_regional_impact_02,
    'metric_regional_impact_03': metric_regional_impact_03,
    'metric_regional_impact_04': metric_regional_impact_04,
    'metric_regional_impact_05': metric_regional_impact_05,
    'metric_regional_impact_06': metric_regional_impact_06,
    'metric_regional_impact_07': metric_regional_impact_07,
    'metric_regional_impact_08': metric_regional_impact_08,
    'metric_regional_impact_09': metric_regional_impact_09,
    'metric_regional_impact_10': metric_regional_impact_10,
    'metric_experiment_value_01': metric_experiment_value_01,
    'metric_experiment_value_02': metric_experiment_value_02,
    'metric_experiment_value_03': metric_experiment_value_03,
    'metric_experiment_value_04': metric_experiment_value_04,
    'metric_experiment_value_05': metric_experiment_value_05,
    'metric_experiment_value_06': metric_experiment_value_06,
    'metric_experiment_value_07': metric_experiment_value_07,
    'metric_experiment_value_08': metric_experiment_value_08,
    'metric_experiment_value_09': metric_experiment_value_09,
    'metric_experiment_value_10': metric_experiment_value_10,
    'metric_canary_health_01': metric_canary_health_01,
    'metric_canary_health_02': metric_canary_health_02,
    'metric_canary_health_03': metric_canary_health_03,
    'metric_canary_health_04': metric_canary_health_04,
    'metric_canary_health_05': metric_canary_health_05,
    'metric_canary_health_06': metric_canary_health_06,
    'metric_canary_health_07': metric_canary_health_07,
    'metric_canary_health_08': metric_canary_health_08,
    'metric_canary_health_09': metric_canary_health_09,
    'metric_canary_health_10': metric_canary_health_10,
    'metric_rollback_risk_01': metric_rollback_risk_01,
    'metric_rollback_risk_02': metric_rollback_risk_02,
    'metric_rollback_risk_03': metric_rollback_risk_03,
    'metric_rollback_risk_04': metric_rollback_risk_04,
    'metric_rollback_risk_05': metric_rollback_risk_05,
    'metric_rollback_risk_06': metric_rollback_risk_06,
    'metric_rollback_risk_07': metric_rollback_risk_07,
    'metric_rollback_risk_08': metric_rollback_risk_08,
    'metric_rollback_risk_09': metric_rollback_risk_09,
    'metric_rollback_risk_10': metric_rollback_risk_10,
    'metric_translation_gap_01': metric_translation_gap_01,
    'metric_translation_gap_02': metric_translation_gap_02,
    'metric_translation_gap_03': metric_translation_gap_03,
    'metric_translation_gap_04': metric_translation_gap_04,
    'metric_translation_gap_05': metric_translation_gap_05,
    'metric_translation_gap_06': metric_translation_gap_06,
    'metric_translation_gap_07': metric_translation_gap_07,
    'metric_translation_gap_08': metric_translation_gap_08,
    'metric_translation_gap_09': metric_translation_gap_09,
    'metric_translation_gap_10': metric_translation_gap_10,
    'metric_release_priority_01': metric_release_priority_01,
    'metric_release_priority_02': metric_release_priority_02,
    'metric_release_priority_03': metric_release_priority_03,
    'metric_release_priority_04': metric_release_priority_04,
    'metric_release_priority_05': metric_release_priority_05,
    'metric_release_priority_06': metric_release_priority_06,
    'metric_release_priority_07': metric_release_priority_07,
    'metric_release_priority_08': metric_release_priority_08,
    'metric_release_priority_09': metric_release_priority_09,
    'metric_release_priority_10': metric_release_priority_10,
}

def metric_vector(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, float]:
    context = context or {}
    return {name: function(record, context) for name, function in METRICS.items()}

def grouped_metrics(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, float]:
    vector = metric_vector(record, context)
    groups: dict[str, list[float]] = defaultdict(list)
    for name, value in vector.items():
        key = name.rsplit('_', 1)[0].removeprefix('metric_')
        groups[key].append(value)
    return {key: statistics.fmean(values) for key, values in groups.items()}

def record_score(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    context = context or {}
    rules = evaluate(record, context)
    rule_summary = summarize(rules)
    metrics = grouped_metrics(record, context)
    metric_score = statistics.fmean(metrics.values()) if metrics else 0.0
    combined = bounded(rule_summary['score'] * 0.55 + metric_score * 0.45)
    return {'score': combined, 'rule_summary': rule_summary, 'metrics': metrics,
            'fingerprint': stable_hash({'record': record.fingerprint, 'metrics': metrics, 'rules': rule_summary})}

def portfolio(records: Iterable[DomainRecord], context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    rows = [record_score(record, context) | {'record_id': record.record_id} for record in records]
    if not rows:
        return {'count': 0, 'average': 0.0, 'minimum': 0.0, 'maximum': 0.0, 'rows': []}
    scores = [row['score'] for row in rows]
    return {'count': len(rows), 'average': statistics.fmean(scores),
            'minimum': min(scores), 'maximum': max(scores), 'rows': sorted(rows, key=lambda row: (-row['score'], row['record_id']))}

def compare(left: DomainRecord, right: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    left_metrics = grouped_metrics(left, context)
    right_metrics = grouped_metrics(right, context)
    delta = {key: right_metrics.get(key, 0.0) - left_metrics.get(key, 0.0) for key in sorted(set(left_metrics) | set(right_metrics))}
    return {'left': left.record_id, 'right': right.record_id, 'delta': delta,
            'winner': right.record_id if sum(delta.values()) >= 0 else left.record_id}
