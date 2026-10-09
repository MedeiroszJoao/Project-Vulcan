import unittest
import numpy as np
from src.model import Scenario, decision, joint_distribution
from src.identifiability import (BASELINE, WORLDS, TargetWorld, assess_worlds,
                                  exact_simplex_bounds, historical_log_evidence,
                                  joint_with_target_world)

class IdentifiabilityTests(unittest.TestCase):
    def test_baseline_equivalence(self):
        for s in (Scenario(),Scenario(prior="jeffreys",rho=.25,relevance=.5),
                  Scenario(revision_pair=(.25,)*4,relevance=.5)):
            np.testing.assert_allclose(joint_with_target_world(s,BASELINE),
                                       joint_distribution(s),atol=1e-12,rtol=1e-12)
    def test_observation_invariance(self):
        s=Scenario()
        self.assertTrue(np.isfinite(historical_log_evidence(s)))
        ys=[joint_with_target_world(s,w).sum(axis=1) for w in WORLDS]
        for y in ys[1:]: np.testing.assert_allclose(y,ys[0],atol=1e-12)
        self.assertGreater(np.max(np.abs(joint_with_target_world(s,WORLDS[1])-
                                         joint_with_target_world(s,WORLDS[2]))),.001)
    def test_decision_changes_without_evidence_change(self):
        r=assess_worlds()
        self.assertTrue(r["decision_changes_sign"])
        self.assertEqual(len({x["historical_log_evidence"] for x in r["worlds"]}),1)
        risks=[x["target_loss_probability"] for x in r["worlds"]]
        self.assertGreater(max(risks)-min(risks),.01)
    def test_extreme_bounds(self):
        r=assess_worlds()
        b=exact_simplex_bounds()
        self.assertEqual(b["robust_action"],"undetermined")
        self.assertEqual(b["minimax_regret_action_within_this_set"],"reallocate_now")
        for w in r["worlds"]:
            self.assertLessEqual(b["lower_net_wait_gain_MUSD"]-1e-10,w["net_wait_gain_MUSD"])
            self.assertGreaterEqual(b["upper_net_wait_gain_MUSD"]+1e-10,w["net_wait_gain_MUSD"])
    def test_interior_probability_rows(self):
        b=exact_simplex_bounds()
        gen=np.random.default_rng(20261009)
        for i in range(20):
            rows=gen.dirichlet((1.,1.,1.),size=3)
            w=TargetWorld(str(i),*map(tuple,rows))
            gain=decision(joint_with_target_world(Scenario(),w),delay_cost=10.)["net_wait_gain"]
            self.assertGreaterEqual(gain,b["lower_net_wait_gain_MUSD"]-1e-10)
            self.assertLessEqual(gain,b["upper_net_wait_gain_MUSD"]+1e-10)
    def test_invalid_cpt(self):
        with self.assertRaises(ValueError):
            TargetWorld("invalid",(.2,.3,.1),(.5,.2,.3),(.4,.3,.3))

if __name__=="__main__":
    unittest.main()
