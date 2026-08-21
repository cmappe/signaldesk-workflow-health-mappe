import tempfile
import unittest
from pathlib import Path

from health_check import aggregate, build_report, load_and_clean


class HealthCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = Path(__file__).parent / "data" / "product_usage_events.csv"
        cls.rows, cls.issues = load_and_clean(cls.data)

    def test_cleaning(self):
        self.assertEqual(len(self.rows), 40)
        self.assertEqual({r["team"] for r in self.rows}, {"Sales", "Support", "Product"})
        self.assertEqual(sum(r["median_confidence"] is None for r in self.rows), 1)

    def test_rates_use_correct_denominators(self):
        metric = aggregate([{"sessions": 10, "completed": 8, "accepted_output": 6,
                             "flagged_for_review": 2, "avg_minutes_saved": 5}])
        self.assertEqual(metric["completion_rate"], .8)
        self.assertEqual(metric["acceptance_rate"], .75)
        self.assertEqual(metric["review_rate"], .25)

    def test_report_contains_decision_and_caveat(self):
        report = build_report(self.rows, self.issues, self.data.name)
        self.assertIn("best current expansion candidate", report)
        self.assertIn("not a causal estimate", report)
        self.assertIn("Final-day coverage is incomplete", report)


if __name__ == "__main__":
    unittest.main()
