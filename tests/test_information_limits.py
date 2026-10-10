import unittest
from pathlib import Path
import numpy as np

class InformationLimitsTests(unittest.TestCase):
    def test_reference_and_nested_sets(self):
        self.assertTrue(Path('research/information_limits/experiment.py').exists())
        from research.information_limits.experiment import analyze, vertices, kernel, BASE, joint, threshold, analytic_threshold
        from src.model import joint_distribution, Scenario
        self.assertEqual(len(vertices()),20)
        np.testing.assert_allclose(joint(kernel(14),BASE),joint_distribution(Scenario()),atol=1e-12)
        result=analyze(14,1)
        self.assertAlmostEqual(result['deterministic_regret'],10.46023708911737,places=7)
        self.assertAlmostEqual(result['mixed_regret'],9.5972218571463,places=7)
        self.assertAlmostEqual(analyze(14,0)['mixed_regret'],0,places=8)
        np.testing.assert_allclose(kernel(700,24),kernel(700,48),atol=1e-12)
        for t in [14,70,None]:
            bracket=threshold(t)
            self.assertLessEqual(bracket[0],analytic_threshold(t))
            self.assertGreaterEqual(bracket[1],analytic_threshold(t))
            values=[analyze(t,r)['mixed_regret'] for r in [0,.25,.5,1]]
            self.assertTrue(np.all(np.diff(values)>=-1e-8))
