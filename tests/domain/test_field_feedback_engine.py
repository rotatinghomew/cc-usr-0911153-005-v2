from __future__ import annotations

import unittest
from field_feedback.observations.report import DomainRecord
from field_feedback.triage.multilingual_clusters import canary_health, clusters, similarity, tokens


class ClusterTests(unittest.TestCase):
    def record(self, key, symptom, country="th"):
        return DomainRecord(key, {"country": country, "crop_type": "durian", "device_model": "r1", "firmware_version": "1",
            "symptom_code": symptom, "severity": 7, "weather": "wet", "terrain": "slope", "operator_skill": 2,
            "reproduction_rate": .8, "affected_units": 4, "translation_confidence": .9})

    def test_synonyms_cluster_across_languages(self):
        left, right = self.record("a", "stuck arm"), self.record("b", "卡住 arm")
        self.assertIn("blocked", tokens("卡住"))
        self.assertGreater(similarity(left, right), .5)
        self.assertEqual(len(clusters([left, right])), 1)

    def test_canary_health_tracks_risk(self):
        health = canary_health([self.record("a", "slow"), self.record("b", "lambat")])
        self.assertGreater(health["rollback_risk"], 0.0)
