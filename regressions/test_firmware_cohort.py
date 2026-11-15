import unittest

from field_feedback.observations.report import DomainRecord
from field_feedback.triage.multilingual_clusters import clusters, similarity


class FirmwareCohortTests(unittest.TestCase):
    def test_same_symptom_in_distinct_firmware_cohorts_is_not_one_incident(self):
        before = DomainRecord("before-release", {
            "symptom_code": "camera", "device_model": "m1",
            "firmware_version": "v2", "country": "c1",
        }, "reported")
        after = DomainRecord("after-release", {
            "symptom_code": "blocked camera", "device_model": "m1",
            "firmware_version": "v1", "country": "c1",
        }, "reported")

        self.assertGreater(similarity(before, after), 0.45)
        self.assertEqual({frozenset(row.record_id for row in group)
                          for group in clusters([before, after])},
                         {frozenset({"before-release"}),
                          frozenset({"after-release"})})


if __name__ == "__main__":
    unittest.main()
