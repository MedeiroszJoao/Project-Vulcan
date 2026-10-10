"""Regression checks for archived forecast integrity and numeric reruns."""
import copy
import unittest

from src.model import Scenario
from src.prospective import build_forecast
from verify_frozen_forecasts import compare_nested, verify


class ForecastIntegrityTests(unittest.TestCase):
    def test_original_forecast_files_and_recomputation(self):
        self.assertTrue(verify())

    def test_detects_changed_probability(self):
        expected = build_forecast(Scenario())
        tampered = copy.deepcopy(expected)
        tampered["public_report_signal_pmf"][0] += 1e-5
        with self.assertRaises(AssertionError):
            compare_nested(expected, tampered)

    def test_detects_changed_category(self):
        expected = build_forecast(Scenario())
        tampered = copy.deepcopy(expected)
        tampered["report_signal_categories"][0] = "new_category"
        with self.assertRaises(AssertionError):
            compare_nested(expected, tampered)

    def test_rejects_changed_metadata(self):
        expected = build_forecast(Scenario())
        tampered = copy.deepcopy(expected)
        tampered["status"] = "VALIDATED_SAFETY"
        with self.assertRaises(AssertionError):
            compare_nested(expected, tampered)

    def test_rejects_non_finite_numbers(self):
        with self.assertRaises(AssertionError):
            compare_nested([0.5, 0.5], [float("nan"), 0.5])


if __name__ == "__main__":
    unittest.main()
