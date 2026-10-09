import copy
import unittest
from src.model import Scenario
from src.prospective import build_forecast
from verify_frozen_forecasts import check_nested,verify

class ForecastProtectionTests(unittest.TestCase):
    def test_all_five_frozen_files_preserved_and_recomputed(self):
        self.assertTrue(verify())
    def test_reject_changed_probability(self):
        a=build_forecast(Scenario())
        b=copy.deepcopy(a)
        b["public_report_signal_pmf"][0]+=1e-5
        with self.assertRaises(AssertionError): check_nested(a,b)
    def test_reject_changed_status(self):
        a=build_forecast(Scenario())
        b=copy.deepcopy(a)
        b["status"]="VALIDATED_PHYSICAL_RISK"
        with self.assertRaises(AssertionError): check_nested(a,b)
