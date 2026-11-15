from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from field_feedback.observations.report import ContractError, Decision, DomainRecord, RuleResult, bounded
from field_feedback.experiments.impact_analysis import grouped_metrics, record_score
from field_feedback.triage.clustering_rules import evaluate

STATES = ['reported', 'triaged', 'experimenting', 'canary', 'rolled_out', 'rolled_back']
TRANSITIONS = {state: tuple(STATES[i + 1:i + 3]) for i, state in enumerate(STATES)}

@dataclass(frozen=True)
class TransitionPlan:
    from_state: str
    to_state: str
    allowed: bool
    reasons: tuple[str, ...]
    score: float

def allowed_targets(state: str) -> tuple[str, ...]:
    if state not in TRANSITIONS:
        raise ContractError('unknown workflow state')
    return TRANSITIONS[state]

def plan_transition(record: DomainRecord, target: str, context: Mapping[str, Any] | None = None) -> TransitionPlan:
    context = context or {}
    if target not in STATES:
        raise ContractError('unknown target state')
    scorecard = record_score(record, context)
    reasons: list[str] = []
    structurally_allowed = target in allowed_targets(record.state)
    if not structurally_allowed:
        reasons.append('transition is not adjacent in the lifecycle')
    threshold = float(context.get('transition_threshold', 0.42))
    if scorecard['score'] < threshold:
        reasons.append('record score is below the transition threshold')
    return TransitionPlan(record.state, target, structurally_allowed and not reasons, tuple(reasons or ['eligible']), scorecard['score'])

def apply_transition(record: DomainRecord, target: str, context: Mapping[str, Any] | None = None) -> DomainRecord:
    plan = plan_transition(record, target, context)
    if not plan.allowed:
        raise ContractError('; '.join(plan.reasons))
    return record.with_state(target)

def guard_country_duplicate_density_01(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_country_duplicate_density_01_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_duplicate_density_01' + (':passed' if allowed else ':blocked')

def guard_crop_type_reproduction_confidence_02(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_crop_type_reproduction_confidence_02_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_reproduction_confidence_02' + (':passed' if allowed else ':blocked')

def guard_device_model_regional_impact_03(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_device_model_regional_impact_03_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_regional_impact_03' + (':passed' if allowed else ':blocked')

def guard_firmware_version_experiment_value_04(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_firmware_version_experiment_value_04_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_experiment_value_04' + (':passed' if allowed else ':blocked')

def guard_symptom_code_canary_health_05(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_symptom_code_canary_health_05_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_canary_health_05' + (':passed' if allowed else ':blocked')

def guard_severity_rollback_risk_06(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_severity_rollback_risk_06_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_rollback_risk_06' + (':passed' if allowed else ':blocked')

def guard_weather_translation_gap_07(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_weather_translation_gap_07_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_translation_gap_07' + (':passed' if allowed else ':blocked')

def guard_terrain_release_priority_08(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_terrain_release_priority_08_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_release_priority_08' + (':passed' if allowed else ':blocked')

def guard_operator_skill_duplicate_density_09(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_operator_skill_duplicate_density_09_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_duplicate_density_09' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_reproduction_confidence_10(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_reproduction_rate_reproduction_confidence_10_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_reproduction_confidence_10' + (':passed' if allowed else ':blocked')

def guard_affected_units_regional_impact_11(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_affected_units_regional_impact_11_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_regional_impact_11' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_experiment_value_12(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_translation_confidence_experiment_value_12_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_experiment_value_12' + (':passed' if allowed else ':blocked')

def guard_country_canary_health_13(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_country_canary_health_13_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_canary_health_13' + (':passed' if allowed else ':blocked')

def guard_crop_type_rollback_risk_14(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_crop_type_rollback_risk_14_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_rollback_risk_14' + (':passed' if allowed else ':blocked')

def guard_device_model_translation_gap_15(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_device_model_translation_gap_15_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_translation_gap_15' + (':passed' if allowed else ':blocked')

def guard_firmware_version_release_priority_16(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_firmware_version_release_priority_16_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_release_priority_16' + (':passed' if allowed else ':blocked')

def guard_symptom_code_duplicate_density_17(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_symptom_code_duplicate_density_17_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_duplicate_density_17' + (':passed' if allowed else ':blocked')

def guard_severity_reproduction_confidence_18(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_severity_reproduction_confidence_18_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_reproduction_confidence_18' + (':passed' if allowed else ':blocked')

def guard_weather_regional_impact_19(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_weather_regional_impact_19_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_regional_impact_19' + (':passed' if allowed else ':blocked')

def guard_terrain_experiment_value_20(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_terrain_experiment_value_20_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_experiment_value_20' + (':passed' if allowed else ':blocked')

def guard_operator_skill_canary_health_21(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_operator_skill_canary_health_21_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_canary_health_21' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_rollback_risk_22(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_reproduction_rate_rollback_risk_22_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_rollback_risk_22' + (':passed' if allowed else ':blocked')

def guard_affected_units_translation_gap_23(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_affected_units_translation_gap_23_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_translation_gap_23' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_release_priority_24(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_translation_confidence_release_priority_24_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_release_priority_24' + (':passed' if allowed else ':blocked')

def guard_country_duplicate_density_25(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_country_duplicate_density_25_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_duplicate_density_25' + (':passed' if allowed else ':blocked')

def guard_crop_type_reproduction_confidence_26(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_crop_type_reproduction_confidence_26_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_reproduction_confidence_26' + (':passed' if allowed else ':blocked')

def guard_device_model_regional_impact_27(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_device_model_regional_impact_27_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_regional_impact_27' + (':passed' if allowed else ':blocked')

def guard_firmware_version_experiment_value_28(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_firmware_version_experiment_value_28_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_experiment_value_28' + (':passed' if allowed else ':blocked')

def guard_symptom_code_canary_health_29(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_symptom_code_canary_health_29_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_canary_health_29' + (':passed' if allowed else ':blocked')

def guard_severity_rollback_risk_30(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_severity_rollback_risk_30_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_rollback_risk_30' + (':passed' if allowed else ':blocked')

def guard_weather_translation_gap_31(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_weather_translation_gap_31_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_translation_gap_31' + (':passed' if allowed else ':blocked')

def guard_terrain_release_priority_32(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_terrain_release_priority_32_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_release_priority_32' + (':passed' if allowed else ':blocked')

def guard_operator_skill_duplicate_density_33(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_operator_skill_duplicate_density_33_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_duplicate_density_33' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_reproduction_confidence_34(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_reproduction_rate_reproduction_confidence_34_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_reproduction_confidence_34' + (':passed' if allowed else ':blocked')

def guard_affected_units_regional_impact_35(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_affected_units_regional_impact_35_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_regional_impact_35' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_experiment_value_36(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_translation_confidence_experiment_value_36_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_experiment_value_36' + (':passed' if allowed else ':blocked')

def guard_country_canary_health_37(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_country_canary_health_37_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_canary_health_37' + (':passed' if allowed else ':blocked')

def guard_crop_type_rollback_risk_38(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_crop_type_rollback_risk_38_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_rollback_risk_38' + (':passed' if allowed else ':blocked')

def guard_device_model_translation_gap_39(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_device_model_translation_gap_39_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_translation_gap_39' + (':passed' if allowed else ':blocked')

def guard_firmware_version_release_priority_40(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_firmware_version_release_priority_40_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_release_priority_40' + (':passed' if allowed else ':blocked')

def guard_symptom_code_duplicate_density_41(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_symptom_code_duplicate_density_41_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_duplicate_density_41' + (':passed' if allowed else ':blocked')

def guard_severity_reproduction_confidence_42(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_severity_reproduction_confidence_42_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_reproduction_confidence_42' + (':passed' if allowed else ':blocked')

def guard_weather_regional_impact_43(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_weather_regional_impact_43_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_regional_impact_43' + (':passed' if allowed else ':blocked')

def guard_terrain_experiment_value_44(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_terrain_experiment_value_44_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_experiment_value_44' + (':passed' if allowed else ':blocked')

def guard_operator_skill_canary_health_45(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_operator_skill_canary_health_45_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_canary_health_45' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_rollback_risk_46(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_reproduction_rate_rollback_risk_46_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_rollback_risk_46' + (':passed' if allowed else ':blocked')

def guard_affected_units_translation_gap_47(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_affected_units_translation_gap_47_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_translation_gap_47' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_release_priority_48(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_translation_confidence_release_priority_48_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_release_priority_48' + (':passed' if allowed else ':blocked')

def guard_country_duplicate_density_49(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_country_duplicate_density_49_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_duplicate_density_49' + (':passed' if allowed else ':blocked')

def guard_crop_type_reproduction_confidence_50(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_crop_type_reproduction_confidence_50_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_reproduction_confidence_50' + (':passed' if allowed else ':blocked')

def guard_device_model_regional_impact_51(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_device_model_regional_impact_51_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_regional_impact_51' + (':passed' if allowed else ':blocked')

def guard_firmware_version_experiment_value_52(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_firmware_version_experiment_value_52_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_experiment_value_52' + (':passed' if allowed else ':blocked')

def guard_symptom_code_canary_health_53(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_symptom_code_canary_health_53_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_canary_health_53' + (':passed' if allowed else ':blocked')

def guard_severity_rollback_risk_54(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_severity_rollback_risk_54_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_rollback_risk_54' + (':passed' if allowed else ':blocked')

def guard_weather_translation_gap_55(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_weather_translation_gap_55_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_translation_gap_55' + (':passed' if allowed else ':blocked')

def guard_terrain_release_priority_56(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_terrain_release_priority_56_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_release_priority_56' + (':passed' if allowed else ':blocked')

def guard_operator_skill_duplicate_density_57(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_operator_skill_duplicate_density_57_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_duplicate_density_57' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_reproduction_confidence_58(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_reproduction_rate_reproduction_confidence_58_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_reproduction_confidence_58' + (':passed' if allowed else ':blocked')

def guard_affected_units_regional_impact_59(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_affected_units_regional_impact_59_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_regional_impact_59' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_experiment_value_60(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_translation_confidence_experiment_value_60_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_experiment_value_60' + (':passed' if allowed else ':blocked')

def guard_country_canary_health_61(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_country_canary_health_61_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_canary_health_61' + (':passed' if allowed else ':blocked')

def guard_crop_type_rollback_risk_62(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_crop_type_rollback_risk_62_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_rollback_risk_62' + (':passed' if allowed else ':blocked')

def guard_device_model_translation_gap_63(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_device_model_translation_gap_63_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_translation_gap_63' + (':passed' if allowed else ':blocked')

def guard_firmware_version_release_priority_64(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_firmware_version_release_priority_64_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_release_priority_64' + (':passed' if allowed else ':blocked')

def guard_symptom_code_duplicate_density_65(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_symptom_code_duplicate_density_65_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_duplicate_density_65' + (':passed' if allowed else ':blocked')

def guard_severity_reproduction_confidence_66(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_severity_reproduction_confidence_66_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_reproduction_confidence_66' + (':passed' if allowed else ':blocked')

def guard_weather_regional_impact_67(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_weather_regional_impact_67_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_regional_impact_67' + (':passed' if allowed else ':blocked')

def guard_terrain_experiment_value_68(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_terrain_experiment_value_68_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_experiment_value_68' + (':passed' if allowed else ':blocked')

def guard_operator_skill_canary_health_69(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_operator_skill_canary_health_69_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_canary_health_69' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_rollback_risk_70(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_reproduction_rate_rollback_risk_70_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_rollback_risk_70' + (':passed' if allowed else ':blocked')

def guard_affected_units_translation_gap_71(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_affected_units_translation_gap_71_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_translation_gap_71' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_release_priority_72(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_translation_confidence_release_priority_72_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_release_priority_72' + (':passed' if allowed else ':blocked')

def guard_country_duplicate_density_73(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_country_duplicate_density_73_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_duplicate_density_73' + (':passed' if allowed else ':blocked')

def guard_crop_type_reproduction_confidence_74(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_crop_type_reproduction_confidence_74_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_reproduction_confidence_74' + (':passed' if allowed else ':blocked')

def guard_device_model_regional_impact_75(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_device_model_regional_impact_75_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_regional_impact_75' + (':passed' if allowed else ':blocked')

def guard_firmware_version_experiment_value_76(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_firmware_version_experiment_value_76_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_experiment_value_76' + (':passed' if allowed else ':blocked')

def guard_symptom_code_canary_health_77(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_symptom_code_canary_health_77_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_canary_health_77' + (':passed' if allowed else ':blocked')

def guard_severity_rollback_risk_78(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_severity_rollback_risk_78_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_rollback_risk_78' + (':passed' if allowed else ':blocked')

def guard_weather_translation_gap_79(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_weather_translation_gap_79_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_translation_gap_79' + (':passed' if allowed else ':blocked')

def guard_terrain_release_priority_80(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_terrain_release_priority_80_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_release_priority_80' + (':passed' if allowed else ':blocked')

def guard_operator_skill_duplicate_density_81(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_operator_skill_duplicate_density_81_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_duplicate_density_81' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_reproduction_confidence_82(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_reproduction_rate_reproduction_confidence_82_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_reproduction_confidence_82' + (':passed' if allowed else ':blocked')

def guard_affected_units_regional_impact_83(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_affected_units_regional_impact_83_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_regional_impact_83' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_experiment_value_84(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_translation_confidence_experiment_value_84_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_experiment_value_84' + (':passed' if allowed else ':blocked')

def guard_country_canary_health_85(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_country_canary_health_85_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_canary_health_85' + (':passed' if allowed else ':blocked')

def guard_crop_type_rollback_risk_86(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_crop_type_rollback_risk_86_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_rollback_risk_86' + (':passed' if allowed else ':blocked')

def guard_device_model_translation_gap_87(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_device_model_translation_gap_87_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_translation_gap_87' + (':passed' if allowed else ':blocked')

def guard_firmware_version_release_priority_88(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_firmware_version_release_priority_88_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_release_priority_88' + (':passed' if allowed else ':blocked')

def guard_symptom_code_duplicate_density_89(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_symptom_code_duplicate_density_89_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_duplicate_density_89' + (':passed' if allowed else ':blocked')

def guard_severity_reproduction_confidence_90(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_severity_reproduction_confidence_90_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_reproduction_confidence_90' + (':passed' if allowed else ':blocked')

def guard_weather_regional_impact_91(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_weather_regional_impact_91_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_regional_impact_91' + (':passed' if allowed else ':blocked')

def guard_terrain_experiment_value_92(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_terrain_experiment_value_92_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_experiment_value_92' + (':passed' if allowed else ':blocked')

def guard_operator_skill_canary_health_93(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_operator_skill_canary_health_93_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_canary_health_93' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_rollback_risk_94(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_reproduction_rate_rollback_risk_94_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_rollback_risk_94' + (':passed' if allowed else ':blocked')

def guard_affected_units_translation_gap_95(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_affected_units_translation_gap_95_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_translation_gap_95' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_release_priority_96(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_translation_confidence_release_priority_96_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_release_priority_96' + (':passed' if allowed else ':blocked')

def guard_country_duplicate_density_97(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_country_duplicate_density_97_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_duplicate_density_97' + (':passed' if allowed else ':blocked')

def guard_crop_type_reproduction_confidence_98(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_crop_type_reproduction_confidence_98_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_reproduction_confidence_98' + (':passed' if allowed else ':blocked')

def guard_device_model_regional_impact_99(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_device_model_regional_impact_99_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_regional_impact_99' + (':passed' if allowed else ':blocked')

def guard_firmware_version_experiment_value_100(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_firmware_version_experiment_value_100_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_experiment_value_100' + (':passed' if allowed else ':blocked')

def guard_symptom_code_canary_health_101(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_symptom_code_canary_health_101_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_canary_health_101' + (':passed' if allowed else ':blocked')

def guard_severity_rollback_risk_102(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_severity_rollback_risk_102_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_rollback_risk_102' + (':passed' if allowed else ':blocked')

def guard_weather_translation_gap_103(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_weather_translation_gap_103_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_translation_gap_103' + (':passed' if allowed else ':blocked')

def guard_terrain_release_priority_104(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_terrain_release_priority_104_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_release_priority_104' + (':passed' if allowed else ':blocked')

def guard_operator_skill_duplicate_density_105(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_operator_skill_duplicate_density_105_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_duplicate_density_105' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_reproduction_confidence_106(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_reproduction_rate_reproduction_confidence_106_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_reproduction_confidence_106' + (':passed' if allowed else ':blocked')

def guard_affected_units_regional_impact_107(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_affected_units_regional_impact_107_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_regional_impact_107' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_experiment_value_108(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_translation_confidence_experiment_value_108_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_experiment_value_108' + (':passed' if allowed else ':blocked')

def guard_country_canary_health_109(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_country_canary_health_109_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_country_canary_health_109' + (':passed' if allowed else ':blocked')

def guard_crop_type_rollback_risk_110(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_crop_type_rollback_risk_110_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_crop_type_rollback_risk_110' + (':passed' if allowed else ':blocked')

def guard_device_model_translation_gap_111(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_device_model_translation_gap_111_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_device_model_translation_gap_111' + (':passed' if allowed else ':blocked')

def guard_firmware_version_release_priority_112(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_firmware_version_release_priority_112_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_firmware_version_release_priority_112' + (':passed' if allowed else ':blocked')

def guard_symptom_code_duplicate_density_113(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('duplicate_density', 0.0)
    floor = float(context.get('guard_symptom_code_duplicate_density_113_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_symptom_code_duplicate_density_113' + (':passed' if allowed else ':blocked')

def guard_severity_reproduction_confidence_114(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('reproduction_confidence', 0.0)
    floor = float(context.get('guard_severity_reproduction_confidence_114_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_severity_reproduction_confidence_114' + (':passed' if allowed else ':blocked')

def guard_weather_regional_impact_115(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('regional_impact', 0.0)
    floor = float(context.get('guard_weather_regional_impact_115_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_weather_regional_impact_115' + (':passed' if allowed else ':blocked')

def guard_terrain_experiment_value_116(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('experiment_value', 0.0)
    floor = float(context.get('guard_terrain_experiment_value_116_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('triaged')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_terrain_experiment_value_116' + (':passed' if allowed else ':blocked')

def guard_operator_skill_canary_health_117(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('canary_health', 0.0)
    floor = float(context.get('guard_operator_skill_canary_health_117_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('experimenting')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_operator_skill_canary_health_117' + (':passed' if allowed else ':blocked')

def guard_reproduction_rate_rollback_risk_118(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('rollback_risk', 0.0)
    floor = float(context.get('guard_reproduction_rate_rollback_risk_118_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('canary')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_reproduction_rate_rollback_risk_118' + (':passed' if allowed else ':blocked')

def guard_affected_units_translation_gap_119(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('translation_gap', 0.0)
    floor = float(context.get('guard_affected_units_translation_gap_119_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_out')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_units_translation_gap_119' + (':passed' if allowed else ':blocked')

def guard_translation_confidence_release_priority_120(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('release_priority', 0.0)
    floor = float(context.get('guard_translation_confidence_release_priority_120_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('rolled_back')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_translation_confidence_release_priority_120' + (':passed' if allowed else ':blocked')

GUARDS: tuple[Callable[[DomainRecord, Mapping[str, Any]], tuple[bool, str]], ...] = (
    guard_country_duplicate_density_01,
    guard_crop_type_reproduction_confidence_02,
    guard_device_model_regional_impact_03,
    guard_firmware_version_experiment_value_04,
    guard_symptom_code_canary_health_05,
    guard_severity_rollback_risk_06,
    guard_weather_translation_gap_07,
    guard_terrain_release_priority_08,
    guard_operator_skill_duplicate_density_09,
    guard_reproduction_rate_reproduction_confidence_10,
    guard_affected_units_regional_impact_11,
    guard_translation_confidence_experiment_value_12,
    guard_country_canary_health_13,
    guard_crop_type_rollback_risk_14,
    guard_device_model_translation_gap_15,
    guard_firmware_version_release_priority_16,
    guard_symptom_code_duplicate_density_17,
    guard_severity_reproduction_confidence_18,
    guard_weather_regional_impact_19,
    guard_terrain_experiment_value_20,
    guard_operator_skill_canary_health_21,
    guard_reproduction_rate_rollback_risk_22,
    guard_affected_units_translation_gap_23,
    guard_translation_confidence_release_priority_24,
    guard_country_duplicate_density_25,
    guard_crop_type_reproduction_confidence_26,
    guard_device_model_regional_impact_27,
    guard_firmware_version_experiment_value_28,
    guard_symptom_code_canary_health_29,
    guard_severity_rollback_risk_30,
    guard_weather_translation_gap_31,
    guard_terrain_release_priority_32,
    guard_operator_skill_duplicate_density_33,
    guard_reproduction_rate_reproduction_confidence_34,
    guard_affected_units_regional_impact_35,
    guard_translation_confidence_experiment_value_36,
    guard_country_canary_health_37,
    guard_crop_type_rollback_risk_38,
    guard_device_model_translation_gap_39,
    guard_firmware_version_release_priority_40,
    guard_symptom_code_duplicate_density_41,
    guard_severity_reproduction_confidence_42,
    guard_weather_regional_impact_43,
    guard_terrain_experiment_value_44,
    guard_operator_skill_canary_health_45,
    guard_reproduction_rate_rollback_risk_46,
    guard_affected_units_translation_gap_47,
    guard_translation_confidence_release_priority_48,
    guard_country_duplicate_density_49,
    guard_crop_type_reproduction_confidence_50,
    guard_device_model_regional_impact_51,
    guard_firmware_version_experiment_value_52,
    guard_symptom_code_canary_health_53,
    guard_severity_rollback_risk_54,
    guard_weather_translation_gap_55,
    guard_terrain_release_priority_56,
    guard_operator_skill_duplicate_density_57,
    guard_reproduction_rate_reproduction_confidence_58,
    guard_affected_units_regional_impact_59,
    guard_translation_confidence_experiment_value_60,
    guard_country_canary_health_61,
    guard_crop_type_rollback_risk_62,
    guard_device_model_translation_gap_63,
    guard_firmware_version_release_priority_64,
    guard_symptom_code_duplicate_density_65,
    guard_severity_reproduction_confidence_66,
    guard_weather_regional_impact_67,
    guard_terrain_experiment_value_68,
    guard_operator_skill_canary_health_69,
    guard_reproduction_rate_rollback_risk_70,
    guard_affected_units_translation_gap_71,
    guard_translation_confidence_release_priority_72,
    guard_country_duplicate_density_73,
    guard_crop_type_reproduction_confidence_74,
    guard_device_model_regional_impact_75,
    guard_firmware_version_experiment_value_76,
    guard_symptom_code_canary_health_77,
    guard_severity_rollback_risk_78,
    guard_weather_translation_gap_79,
    guard_terrain_release_priority_80,
    guard_operator_skill_duplicate_density_81,
    guard_reproduction_rate_reproduction_confidence_82,
    guard_affected_units_regional_impact_83,
    guard_translation_confidence_experiment_value_84,
    guard_country_canary_health_85,
    guard_crop_type_rollback_risk_86,
    guard_device_model_translation_gap_87,
    guard_firmware_version_release_priority_88,
    guard_symptom_code_duplicate_density_89,
    guard_severity_reproduction_confidence_90,
    guard_weather_regional_impact_91,
    guard_terrain_experiment_value_92,
    guard_operator_skill_canary_health_93,
    guard_reproduction_rate_rollback_risk_94,
    guard_affected_units_translation_gap_95,
    guard_translation_confidence_release_priority_96,
    guard_country_duplicate_density_97,
    guard_crop_type_reproduction_confidence_98,
    guard_device_model_regional_impact_99,
    guard_firmware_version_experiment_value_100,
    guard_symptom_code_canary_health_101,
    guard_severity_rollback_risk_102,
    guard_weather_translation_gap_103,
    guard_terrain_release_priority_104,
    guard_operator_skill_duplicate_density_105,
    guard_reproduction_rate_reproduction_confidence_106,
    guard_affected_units_regional_impact_107,
    guard_translation_confidence_experiment_value_108,
    guard_country_canary_health_109,
    guard_crop_type_rollback_risk_110,
    guard_device_model_translation_gap_111,
    guard_firmware_version_release_priority_112,
    guard_symptom_code_duplicate_density_113,
    guard_severity_reproduction_confidence_114,
    guard_weather_regional_impact_115,
    guard_terrain_experiment_value_116,
    guard_operator_skill_canary_health_117,
    guard_reproduction_rate_rollback_risk_118,
    guard_affected_units_translation_gap_119,
    guard_translation_confidence_release_priority_120,
)

def guard_report(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    context = dict(context or {})
    context['_metrics'] = grouped_metrics(record, context)
    results = [guard(record, context) for guard in GUARDS]
    return {'passed': sum(item[0] for item in results), 'failed': sum(not item[0] for item in results),
            'messages': [item[1] for item in results]}

def decide(record: DomainRecord, context: Mapping[str, Any] | None = None) -> Decision:
    context = context or {}
    rules = evaluate(record, context)
    scorecard = record_score(record, context)
    guards = guard_report(record, context)
    critical = sum(item.severity == 'critical' for item in rules)
    if critical:
        outcome = 'hold'
    elif scorecard['score'] >= float(context.get('approve_threshold', 0.62)) and guards['passed'] >= guards['failed']:
        outcome = 'approve'
    elif scorecard['score'] >= float(context.get('review_threshold', 0.38)):
        outcome = 'review'
    else:
        outcome = 'reject'
    reasons = (f"score={scorecard['score']:.6f}", f"critical={critical}",
               f"guards={guards['passed']}/{guards['passed'] + guards['failed']}")
    return Decision(record.record_id, outcome, scorecard['score'], reasons, rules, scorecard['metrics'])

def advance_for_outcome(record: DomainRecord, decision: Decision) -> DomainRecord:
    current = STATES.index(record.state)
    if decision.outcome == 'approve' and current + 1 < len(STATES):
        return record.with_state(STATES[current + 1])
    if decision.outcome == 'hold' and STATES[-1] != record.state:
        return record.with_state(STATES[-1])
    return record
