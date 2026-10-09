import math
import unittest
from dataclasses import replace
import numpy as np
from scipy.special import betaln
from src.model import Scenario
from src.prospective import physical_count_forecast, reported_count_forecast, build_forecast, categorical_score

class TestProspective(unittest.TestCase):
    def test_analytic_beta_binomial_hh(self):
        from math import comb
        v=physical_count_forecast(Scenario(revision_pair=(1,0,0,0),rho=0))
        target=np.array([comb(6,k)*np.exp(betaln(3+k,11+6-k)-betaln(3,11)) for k in range(7)])
        np.testing.assert_allclose(v,target,atol=1e-14)

    def test_probabilities_sum_to_one(self):
        for s in [Scenario(),Scenario(rho=.25),Scenario(revision_pair=(.25,)*4), Scenario(prior='jeffreys')]:
            f=build_forecast(s)
            for name in ['public_report_signal_pmf','latent_physical_anomaly_count_pmf','hypothetical_disclosed_count_pmf']:
                p=np.array(f[name]); self.assertAlmostEqual(sum(p),1,13)
                self.assertTrue(np.all(p>=-1e-13))

    def test_public_y_marginal_invariant_to_target_revision(self):
        a=build_forecast(Scenario(revision_pair=(1,0,0,0)))
        b=build_forecast(Scenario(revision_pair=(0,1,0,0)))
        np.testing.assert_allclose(a['public_report_signal_pmf'],b['public_report_signal_pmf'],atol=1e-14)

    def test_no_transfer_effect_on_unconditional_lv(self):
        a=build_forecast(Scenario(relevance=0))
        b=build_forecast(Scenario(relevance=1))
        np.testing.assert_allclose(a['public_report_signal_pmf'],b['public_report_signal_pmf'],atol=1e-14)

    def test_report_count_zero_detection(self):
        x=reported_count_forecast(Scenario(detection=0,disclosure=1,false_positive=0))
        self.assertAlmostEqual(x[0],1,13)
        self.assertAlmostEqual(sum(x[1:]),0,13)

    def test_unreported_mass(self):
        s=Scenario(disclosure=.45)
        self.assertAlmostEqual(reported_count_forecast(s)[-1],.55)

    def test_proper_scoring_simple(self):
        t=categorical_score([.1,.7,.1,.1],1)
        self.assertAlmostEqual(t['brier_multiclass_sum'],.12)
        self.assertAlmostEqual(t['negative_log_likelihood_nats'],-math.log(.7))

    def test_log_zero_is_explicit(self):
        t=categorical_score([1,0],1)
        self.assertTrue(t['zero_probability_observed'])
        self.assertIsNone(t['negative_log_likelihood_nats'])

    def test_invalid_probabilities(self):
        with self.assertRaises(ValueError): categorical_score([.5,.7],0)
        with self.assertRaises(ValueError): categorical_score([.3,.7],2)

if __name__=='__main__':unittest.main()
