from __future__ import annotations

import math
from typing import Any, Callable, Mapping

from field_feedback.observations.report import DomainRecord, RuleResult, bounded, finite_number, normalized_text

RuleFunction = Callable[[DomainRecord, Mapping[str, Any]], RuleResult]

def _number(record: DomainRecord, field: str) -> float:
    value = record.payload.get(field)
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return finite_number(value)
    text = normalized_text(value)
    if not text:
        return 0.0
    try:
        return finite_number(text)
    except ValueError:
        return float(sum(ord(ch) for ch in text) % 101)

def _context_number(context: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return finite_number(context.get(key, default))
    except ValueError:
        return default

def _result(code: str, value: float, threshold: float, higher_is_better: bool, message: str, evidence: dict[str, Any]) -> RuleResult:
    distance = (value - threshold) if higher_is_better else (threshold - value)
    passed = distance >= 0
    scale = max(1.0, abs(threshold))
    score = bounded(0.5 + distance / (2.0 * scale))
    severity = 'info' if passed else ('critical' if score < 0.2 else 'error')
    return RuleResult(code, passed, score, severity, message, evidence)

def check_country_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_country_presence_threshold', 10.333)
    return _result('check_country_presence', adjusted, threshold, True, 'validates country presence',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_country_range_threshold', 12.667)
    return _result('check_country_range', adjusted, threshold, True, 'validates country range',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_country_stability_threshold', 15.0)
    return _result('check_country_stability', adjusted, threshold, False, 'validates country stability',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_country_freshness_threshold', 17.333)
    return _result('check_country_freshness', adjusted, threshold, True, 'validates country freshness',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_country_coverage_threshold', 19.667)
    return _result('check_country_coverage', adjusted, threshold, True, 'validates country coverage',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_country_consistency_threshold', 22.0)
    return _result('check_country_consistency', adjusted, threshold, False, 'validates country consistency',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_country_risk_threshold', 24.333)
    return _result('check_country_risk', adjusted, threshold, True, 'validates country risk',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_country_confidence_threshold', 26.667)
    return _result('check_country_confidence', adjusted, threshold, True, 'validates country confidence',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_country_dependency_threshold', 29.0)
    return _result('check_country_dependency', adjusted, threshold, False, 'validates country dependency',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_country_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'country')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_country_readiness_threshold', 31.333)
    return _result('check_country_readiness', adjusted, threshold, True, 'validates country readiness',
                   {'field': 'country', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_crop_type_presence_threshold', 9.333)
    return _result('check_crop_type_presence', adjusted, threshold, True, 'validates crop_type presence',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_crop_type_range_threshold', 11.667)
    return _result('check_crop_type_range', adjusted, threshold, False, 'validates crop_type range',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_crop_type_stability_threshold', 14.0)
    return _result('check_crop_type_stability', adjusted, threshold, True, 'validates crop_type stability',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_crop_type_freshness_threshold', 16.333)
    return _result('check_crop_type_freshness', adjusted, threshold, True, 'validates crop_type freshness',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_crop_type_coverage_threshold', 18.667)
    return _result('check_crop_type_coverage', adjusted, threshold, False, 'validates crop_type coverage',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_crop_type_consistency_threshold', 21.0)
    return _result('check_crop_type_consistency', adjusted, threshold, True, 'validates crop_type consistency',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_crop_type_risk_threshold', 23.333)
    return _result('check_crop_type_risk', adjusted, threshold, True, 'validates crop_type risk',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_crop_type_confidence_threshold', 25.667)
    return _result('check_crop_type_confidence', adjusted, threshold, False, 'validates crop_type confidence',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_crop_type_dependency_threshold', 28.0)
    return _result('check_crop_type_dependency', adjusted, threshold, True, 'validates crop_type dependency',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_crop_type_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'crop_type')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_crop_type_readiness_threshold', 30.333)
    return _result('check_crop_type_readiness', adjusted, threshold, True, 'validates crop_type readiness',
                   {'field': 'crop_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_device_model_presence_threshold', 8.333)
    return _result('check_device_model_presence', adjusted, threshold, False, 'validates device_model presence',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_device_model_range_threshold', 10.667)
    return _result('check_device_model_range', adjusted, threshold, True, 'validates device_model range',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_device_model_stability_threshold', 13.0)
    return _result('check_device_model_stability', adjusted, threshold, True, 'validates device_model stability',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_device_model_freshness_threshold', 15.333)
    return _result('check_device_model_freshness', adjusted, threshold, False, 'validates device_model freshness',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_device_model_coverage_threshold', 17.667)
    return _result('check_device_model_coverage', adjusted, threshold, True, 'validates device_model coverage',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_device_model_consistency_threshold', 20.0)
    return _result('check_device_model_consistency', adjusted, threshold, True, 'validates device_model consistency',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_device_model_risk_threshold', 22.333)
    return _result('check_device_model_risk', adjusted, threshold, False, 'validates device_model risk',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_device_model_confidence_threshold', 24.667)
    return _result('check_device_model_confidence', adjusted, threshold, True, 'validates device_model confidence',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_device_model_dependency_threshold', 27.0)
    return _result('check_device_model_dependency', adjusted, threshold, True, 'validates device_model dependency',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_device_model_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'device_model')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_device_model_readiness_threshold', 29.333)
    return _result('check_device_model_readiness', adjusted, threshold, False, 'validates device_model readiness',
                   {'field': 'device_model', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_firmware_version_presence_threshold', 31.667)
    return _result('check_firmware_version_presence', adjusted, threshold, True, 'validates firmware_version presence',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_firmware_version_range_threshold', 9.667)
    return _result('check_firmware_version_range', adjusted, threshold, True, 'validates firmware_version range',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_firmware_version_stability_threshold', 12.0)
    return _result('check_firmware_version_stability', adjusted, threshold, False, 'validates firmware_version stability',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_firmware_version_freshness_threshold', 14.333)
    return _result('check_firmware_version_freshness', adjusted, threshold, True, 'validates firmware_version freshness',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_firmware_version_coverage_threshold', 16.667)
    return _result('check_firmware_version_coverage', adjusted, threshold, True, 'validates firmware_version coverage',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_firmware_version_consistency_threshold', 19.0)
    return _result('check_firmware_version_consistency', adjusted, threshold, False, 'validates firmware_version consistency',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_firmware_version_risk_threshold', 21.333)
    return _result('check_firmware_version_risk', adjusted, threshold, True, 'validates firmware_version risk',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_firmware_version_confidence_threshold', 23.667)
    return _result('check_firmware_version_confidence', adjusted, threshold, True, 'validates firmware_version confidence',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_firmware_version_dependency_threshold', 26.0)
    return _result('check_firmware_version_dependency', adjusted, threshold, False, 'validates firmware_version dependency',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_firmware_version_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'firmware_version')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_firmware_version_readiness_threshold', 28.333)
    return _result('check_firmware_version_readiness', adjusted, threshold, True, 'validates firmware_version readiness',
                   {'field': 'firmware_version', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_symptom_code_presence_threshold', 30.667)
    return _result('check_symptom_code_presence', adjusted, threshold, True, 'validates symptom_code presence',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_symptom_code_range_threshold', 8.667)
    return _result('check_symptom_code_range', adjusted, threshold, False, 'validates symptom_code range',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_symptom_code_stability_threshold', 11.0)
    return _result('check_symptom_code_stability', adjusted, threshold, True, 'validates symptom_code stability',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_symptom_code_freshness_threshold', 13.333)
    return _result('check_symptom_code_freshness', adjusted, threshold, True, 'validates symptom_code freshness',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_symptom_code_coverage_threshold', 15.667)
    return _result('check_symptom_code_coverage', adjusted, threshold, False, 'validates symptom_code coverage',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_symptom_code_consistency_threshold', 18.0)
    return _result('check_symptom_code_consistency', adjusted, threshold, True, 'validates symptom_code consistency',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_symptom_code_risk_threshold', 20.333)
    return _result('check_symptom_code_risk', adjusted, threshold, True, 'validates symptom_code risk',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_symptom_code_confidence_threshold', 22.667)
    return _result('check_symptom_code_confidence', adjusted, threshold, False, 'validates symptom_code confidence',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_symptom_code_dependency_threshold', 25.0)
    return _result('check_symptom_code_dependency', adjusted, threshold, True, 'validates symptom_code dependency',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_symptom_code_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'symptom_code')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_symptom_code_readiness_threshold', 27.333)
    return _result('check_symptom_code_readiness', adjusted, threshold, True, 'validates symptom_code readiness',
                   {'field': 'symptom_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_severity_presence_threshold', 29.667)
    return _result('check_severity_presence', adjusted, threshold, False, 'validates severity presence',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_severity_range_threshold', 32.0)
    return _result('check_severity_range', adjusted, threshold, True, 'validates severity range',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_severity_stability_threshold', 10.0)
    return _result('check_severity_stability', adjusted, threshold, True, 'validates severity stability',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_severity_freshness_threshold', 12.333)
    return _result('check_severity_freshness', adjusted, threshold, False, 'validates severity freshness',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_severity_coverage_threshold', 14.667)
    return _result('check_severity_coverage', adjusted, threshold, True, 'validates severity coverage',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_severity_consistency_threshold', 17.0)
    return _result('check_severity_consistency', adjusted, threshold, True, 'validates severity consistency',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_severity_risk_threshold', 19.333)
    return _result('check_severity_risk', adjusted, threshold, False, 'validates severity risk',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_severity_confidence_threshold', 21.667)
    return _result('check_severity_confidence', adjusted, threshold, True, 'validates severity confidence',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_severity_dependency_threshold', 24.0)
    return _result('check_severity_dependency', adjusted, threshold, True, 'validates severity dependency',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_severity_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'severity')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_severity_readiness_threshold', 26.333)
    return _result('check_severity_readiness', adjusted, threshold, False, 'validates severity readiness',
                   {'field': 'severity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_weather_presence_threshold', 28.667)
    return _result('check_weather_presence', adjusted, threshold, True, 'validates weather presence',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_weather_range_threshold', 31.0)
    return _result('check_weather_range', adjusted, threshold, True, 'validates weather range',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_weather_stability_threshold', 9.0)
    return _result('check_weather_stability', adjusted, threshold, False, 'validates weather stability',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_weather_freshness_threshold', 11.333)
    return _result('check_weather_freshness', adjusted, threshold, True, 'validates weather freshness',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_weather_coverage_threshold', 13.667)
    return _result('check_weather_coverage', adjusted, threshold, True, 'validates weather coverage',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_weather_consistency_threshold', 16.0)
    return _result('check_weather_consistency', adjusted, threshold, False, 'validates weather consistency',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_weather_risk_threshold', 18.333)
    return _result('check_weather_risk', adjusted, threshold, True, 'validates weather risk',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_weather_confidence_threshold', 20.667)
    return _result('check_weather_confidence', adjusted, threshold, True, 'validates weather confidence',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_weather_dependency_threshold', 23.0)
    return _result('check_weather_dependency', adjusted, threshold, False, 'validates weather dependency',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_weather_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'weather')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_weather_readiness_threshold', 25.333)
    return _result('check_weather_readiness', adjusted, threshold, True, 'validates weather readiness',
                   {'field': 'weather', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_terrain_presence_threshold', 27.667)
    return _result('check_terrain_presence', adjusted, threshold, True, 'validates terrain presence',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_terrain_range_threshold', 30.0)
    return _result('check_terrain_range', adjusted, threshold, False, 'validates terrain range',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_terrain_stability_threshold', 8.0)
    return _result('check_terrain_stability', adjusted, threshold, True, 'validates terrain stability',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_terrain_freshness_threshold', 10.333)
    return _result('check_terrain_freshness', adjusted, threshold, True, 'validates terrain freshness',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_terrain_coverage_threshold', 12.667)
    return _result('check_terrain_coverage', adjusted, threshold, False, 'validates terrain coverage',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_terrain_consistency_threshold', 15.0)
    return _result('check_terrain_consistency', adjusted, threshold, True, 'validates terrain consistency',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_terrain_risk_threshold', 17.333)
    return _result('check_terrain_risk', adjusted, threshold, True, 'validates terrain risk',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_terrain_confidence_threshold', 19.667)
    return _result('check_terrain_confidence', adjusted, threshold, False, 'validates terrain confidence',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_terrain_dependency_threshold', 22.0)
    return _result('check_terrain_dependency', adjusted, threshold, True, 'validates terrain dependency',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_terrain_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'terrain')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_terrain_readiness_threshold', 24.333)
    return _result('check_terrain_readiness', adjusted, threshold, True, 'validates terrain readiness',
                   {'field': 'terrain', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_operator_skill_presence_threshold', 26.667)
    return _result('check_operator_skill_presence', adjusted, threshold, False, 'validates operator_skill presence',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_operator_skill_range_threshold', 29.0)
    return _result('check_operator_skill_range', adjusted, threshold, True, 'validates operator_skill range',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_operator_skill_stability_threshold', 31.333)
    return _result('check_operator_skill_stability', adjusted, threshold, True, 'validates operator_skill stability',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_operator_skill_freshness_threshold', 9.333)
    return _result('check_operator_skill_freshness', adjusted, threshold, False, 'validates operator_skill freshness',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_operator_skill_coverage_threshold', 11.667)
    return _result('check_operator_skill_coverage', adjusted, threshold, True, 'validates operator_skill coverage',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_operator_skill_consistency_threshold', 14.0)
    return _result('check_operator_skill_consistency', adjusted, threshold, True, 'validates operator_skill consistency',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_operator_skill_risk_threshold', 16.333)
    return _result('check_operator_skill_risk', adjusted, threshold, False, 'validates operator_skill risk',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_operator_skill_confidence_threshold', 18.667)
    return _result('check_operator_skill_confidence', adjusted, threshold, True, 'validates operator_skill confidence',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_operator_skill_dependency_threshold', 21.0)
    return _result('check_operator_skill_dependency', adjusted, threshold, True, 'validates operator_skill dependency',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_skill_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_skill')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_operator_skill_readiness_threshold', 23.333)
    return _result('check_operator_skill_readiness', adjusted, threshold, False, 'validates operator_skill readiness',
                   {'field': 'operator_skill', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_reproduction_rate_presence_threshold', 25.667)
    return _result('check_reproduction_rate_presence', adjusted, threshold, True, 'validates reproduction_rate presence',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_reproduction_rate_range_threshold', 28.0)
    return _result('check_reproduction_rate_range', adjusted, threshold, True, 'validates reproduction_rate range',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_reproduction_rate_stability_threshold', 30.333)
    return _result('check_reproduction_rate_stability', adjusted, threshold, False, 'validates reproduction_rate stability',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_reproduction_rate_freshness_threshold', 8.333)
    return _result('check_reproduction_rate_freshness', adjusted, threshold, True, 'validates reproduction_rate freshness',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_reproduction_rate_coverage_threshold', 10.667)
    return _result('check_reproduction_rate_coverage', adjusted, threshold, True, 'validates reproduction_rate coverage',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_reproduction_rate_consistency_threshold', 13.0)
    return _result('check_reproduction_rate_consistency', adjusted, threshold, False, 'validates reproduction_rate consistency',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_reproduction_rate_risk_threshold', 15.333)
    return _result('check_reproduction_rate_risk', adjusted, threshold, True, 'validates reproduction_rate risk',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_reproduction_rate_confidence_threshold', 17.667)
    return _result('check_reproduction_rate_confidence', adjusted, threshold, True, 'validates reproduction_rate confidence',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_reproduction_rate_dependency_threshold', 20.0)
    return _result('check_reproduction_rate_dependency', adjusted, threshold, False, 'validates reproduction_rate dependency',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_reproduction_rate_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'reproduction_rate')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_reproduction_rate_readiness_threshold', 22.333)
    return _result('check_reproduction_rate_readiness', adjusted, threshold, True, 'validates reproduction_rate readiness',
                   {'field': 'reproduction_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_affected_units_presence_threshold', 24.667)
    return _result('check_affected_units_presence', adjusted, threshold, True, 'validates affected_units presence',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_affected_units_range_threshold', 27.0)
    return _result('check_affected_units_range', adjusted, threshold, False, 'validates affected_units range',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_affected_units_stability_threshold', 29.333)
    return _result('check_affected_units_stability', adjusted, threshold, True, 'validates affected_units stability',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_affected_units_freshness_threshold', 31.667)
    return _result('check_affected_units_freshness', adjusted, threshold, True, 'validates affected_units freshness',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_affected_units_coverage_threshold', 9.667)
    return _result('check_affected_units_coverage', adjusted, threshold, False, 'validates affected_units coverage',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_affected_units_consistency_threshold', 12.0)
    return _result('check_affected_units_consistency', adjusted, threshold, True, 'validates affected_units consistency',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_affected_units_risk_threshold', 14.333)
    return _result('check_affected_units_risk', adjusted, threshold, True, 'validates affected_units risk',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_affected_units_confidence_threshold', 16.667)
    return _result('check_affected_units_confidence', adjusted, threshold, False, 'validates affected_units confidence',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_affected_units_dependency_threshold', 19.0)
    return _result('check_affected_units_dependency', adjusted, threshold, True, 'validates affected_units dependency',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_units_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_units')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_affected_units_readiness_threshold', 21.333)
    return _result('check_affected_units_readiness', adjusted, threshold, True, 'validates affected_units readiness',
                   {'field': 'affected_units', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_translation_confidence_presence_threshold', 23.667)
    return _result('check_translation_confidence_presence', adjusted, threshold, False, 'validates translation_confidence presence',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_translation_confidence_range_threshold', 26.0)
    return _result('check_translation_confidence_range', adjusted, threshold, True, 'validates translation_confidence range',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_translation_confidence_stability_threshold', 28.333)
    return _result('check_translation_confidence_stability', adjusted, threshold, True, 'validates translation_confidence stability',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_translation_confidence_freshness_threshold', 30.667)
    return _result('check_translation_confidence_freshness', adjusted, threshold, False, 'validates translation_confidence freshness',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_translation_confidence_coverage_threshold', 8.667)
    return _result('check_translation_confidence_coverage', adjusted, threshold, True, 'validates translation_confidence coverage',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_translation_confidence_consistency_threshold', 11.0)
    return _result('check_translation_confidence_consistency', adjusted, threshold, True, 'validates translation_confidence consistency',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_translation_confidence_risk_threshold', 13.333)
    return _result('check_translation_confidence_risk', adjusted, threshold, False, 'validates translation_confidence risk',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_translation_confidence_confidence_threshold', 15.667)
    return _result('check_translation_confidence_confidence', adjusted, threshold, True, 'validates translation_confidence confidence',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_translation_confidence_dependency_threshold', 18.0)
    return _result('check_translation_confidence_dependency', adjusted, threshold, True, 'validates translation_confidence dependency',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_translation_confidence_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'translation_confidence')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_translation_confidence_readiness_threshold', 20.333)
    return _result('check_translation_confidence_readiness', adjusted, threshold, False, 'validates translation_confidence readiness',
                   {'field': 'translation_confidence', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

RULES: tuple[RuleFunction, ...] = (
    check_country_presence,
    check_country_range,
    check_country_stability,
    check_country_freshness,
    check_country_coverage,
    check_country_consistency,
    check_country_risk,
    check_country_confidence,
    check_country_dependency,
    check_country_readiness,
    check_crop_type_presence,
    check_crop_type_range,
    check_crop_type_stability,
    check_crop_type_freshness,
    check_crop_type_coverage,
    check_crop_type_consistency,
    check_crop_type_risk,
    check_crop_type_confidence,
    check_crop_type_dependency,
    check_crop_type_readiness,
    check_device_model_presence,
    check_device_model_range,
    check_device_model_stability,
    check_device_model_freshness,
    check_device_model_coverage,
    check_device_model_consistency,
    check_device_model_risk,
    check_device_model_confidence,
    check_device_model_dependency,
    check_device_model_readiness,
    check_firmware_version_presence,
    check_firmware_version_range,
    check_firmware_version_stability,
    check_firmware_version_freshness,
    check_firmware_version_coverage,
    check_firmware_version_consistency,
    check_firmware_version_risk,
    check_firmware_version_confidence,
    check_firmware_version_dependency,
    check_firmware_version_readiness,
    check_symptom_code_presence,
    check_symptom_code_range,
    check_symptom_code_stability,
    check_symptom_code_freshness,
    check_symptom_code_coverage,
    check_symptom_code_consistency,
    check_symptom_code_risk,
    check_symptom_code_confidence,
    check_symptom_code_dependency,
    check_symptom_code_readiness,
    check_severity_presence,
    check_severity_range,
    check_severity_stability,
    check_severity_freshness,
    check_severity_coverage,
    check_severity_consistency,
    check_severity_risk,
    check_severity_confidence,
    check_severity_dependency,
    check_severity_readiness,
    check_weather_presence,
    check_weather_range,
    check_weather_stability,
    check_weather_freshness,
    check_weather_coverage,
    check_weather_consistency,
    check_weather_risk,
    check_weather_confidence,
    check_weather_dependency,
    check_weather_readiness,
    check_terrain_presence,
    check_terrain_range,
    check_terrain_stability,
    check_terrain_freshness,
    check_terrain_coverage,
    check_terrain_consistency,
    check_terrain_risk,
    check_terrain_confidence,
    check_terrain_dependency,
    check_terrain_readiness,
    check_operator_skill_presence,
    check_operator_skill_range,
    check_operator_skill_stability,
    check_operator_skill_freshness,
    check_operator_skill_coverage,
    check_operator_skill_consistency,
    check_operator_skill_risk,
    check_operator_skill_confidence,
    check_operator_skill_dependency,
    check_operator_skill_readiness,
    check_reproduction_rate_presence,
    check_reproduction_rate_range,
    check_reproduction_rate_stability,
    check_reproduction_rate_freshness,
    check_reproduction_rate_coverage,
    check_reproduction_rate_consistency,
    check_reproduction_rate_risk,
    check_reproduction_rate_confidence,
    check_reproduction_rate_dependency,
    check_reproduction_rate_readiness,
    check_affected_units_presence,
    check_affected_units_range,
    check_affected_units_stability,
    check_affected_units_freshness,
    check_affected_units_coverage,
    check_affected_units_consistency,
    check_affected_units_risk,
    check_affected_units_confidence,
    check_affected_units_dependency,
    check_affected_units_readiness,
    check_translation_confidence_presence,
    check_translation_confidence_range,
    check_translation_confidence_stability,
    check_translation_confidence_freshness,
    check_translation_confidence_coverage,
    check_translation_confidence_consistency,
    check_translation_confidence_risk,
    check_translation_confidence_confidence,
    check_translation_confidence_dependency,
    check_translation_confidence_readiness,
)

RULE_INDEX = {rule.__name__: rule for rule in RULES}

def evaluate(record: DomainRecord, context: Mapping[str, Any] | None = None) -> tuple[RuleResult, ...]:
    context = context or {}
    return tuple(rule(record, context) for rule in RULES)

def summarize(results: tuple[RuleResult, ...]) -> dict[str, Any]:
    if not results:
        return {'score': 0.0, 'passed': 0, 'failed': 0, 'critical': 0}
    return {'score': sum(item.score for item in results) / len(results),
            'passed': sum(item.passed for item in results),
            'failed': sum(not item.passed for item in results),
            'critical': sum(item.severity == 'critical' for item in results)}
