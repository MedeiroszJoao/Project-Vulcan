import itertools
import unittest
from dataclasses import replace
import numpy as np
from scipy.special import betaln
from src.model import *

class TestModel(unittest.TestCase):
    def test_evidence_table_consistency(self):
        import csv
        from datetime import date
        with open('data/vulcan_flights.csv') as f: vulcan=list(csv.DictReader(f))
        self.assertEqual([(int(r['boosters']),int(r['reported_anomalies'])) for r in vulcan],HISTORY)
        with open('data/atlas_gem63.csv') as f: atlas=list(csv.DictReader(f))
        self.assertEqual(len(atlas),9)
        self.assertEqual(sum(int(r['boosters']) for r in atlas),32)
        self.assertEqual((date(2024,12,5)-date(2022,12,21)).days,715)

    def test_toy(self):
        p=.99**6/(.99**6+.90**6)
        self.assertAlmostEqual(p,.6391924983790723,14)

    def test_beta_posteriors_and_predictive(self):
        for prior,a,b in [('uniform',3,11),('jeffreys',2.5,10.5)]:
            p,w=posterior_nodes(Scenario(prior=prior))
            self.assertAlmostEqual(float(p@w),a/(a+b),13)
            self.assertAlmostEqual(float(w@(1-p)**6),np.exp(betaln(a,b+6)-betaln(a,b)),13)

    def test_plate_against_binary_enumeration(self):
        for n in (2,4,6):
            brute=np.zeros(n+1)
            for bits in itertools.product((0,1),repeat=n):
                k=sum(bits); brute[k]+=.17**k*.83**(n-k)
            np.testing.assert_allclose(brute,count_pmf(n,.17),atol=1e-14)

    def test_correlation_keeps_marginal(self):
        for rho in (0,.15,.4,1):
            v=count_pmf(6,.2,rho); k=np.arange(7)
            self.assertAlmostEqual(v.sum(),1)
            self.assertAlmostEqual(float(v@k)/6,.2)
            jointpair=float(v@(k*(k-1)))/30
            self.assertAlmostEqual((jointpair-.04)/.16,rho)

    def test_no_transfer(self):
        for s in (Scenario(relevance=0),Scenario(revision_pair=(0,1,0,0))):
            j=joint_distribution(s)
            np.testing.assert_allclose(j,np.outer(j.sum(1),j.sum(0)),atol=1e-13)
            self.assertAlmostEqual(decision(j)['evsi'],0,10)

    def test_evsi_nonnegative_and_evpi_bound(self):
        for prior,rho,rel in itertools.product(('uniform','jeffreys'),(0,.15,.4),(0,.5,1)):
            j=joint_distribution(Scenario(prior=prior,rho=rho,relevance=rel))
            for loss in (250,1000,2000):
                r=decision(j,loss=loss)
                self.assertGreaterEqual(r['evsi'],-1e-10)
                alt=r['realocate_now_cost']
                perfect=j.sum(0)@np.minimum([0,.25*loss,loss],alt)
                evpi=min(r['counterfactual_launch_cost'],alt)-perfect
                self.assertLessEqual(r['evsi'],evpi+1e-9)

    def test_uninformative_disclosure(self):
        j=joint_distribution(Scenario(disclosure=0))
        self.assertAlmostEqual(j[3].sum(),1)
        self.assertAlmostEqual(decision(j)['evsi'],0,10)

    def test_no_authorization(self):
        r=decision(joint_distribution(Scenario()),approval=(0,0,0,0),delay_cost=10)
        self.assertAlmostEqual(r['net_wait_gain'],-15,10)
        self.assertEqual(r['preferred'],'realocate_now')

    def test_cost_monotonicity(self):
        j=joint_distribution(Scenario())
        self.assertAlmostEqual(decision(j,delay_cost=12)['wait_cost']-
                               decision(j,delay_cost=2)['wait_cost'],10)

    def test_cpts_and_quadrature(self):
        for s in (Scenario(),Scenario(rho=.4,history_detection=.7,heritage_weight=.25,
                                     revision_pair=(.25,.25,.25,.25))):
            w,y,z=latent_model(s)
            for v in (w,y,z): self.assertTrue((v>=0).all())
            self.assertAlmostEqual(w.sum(),1)
            np.testing.assert_allclose(y.sum(1),1,atol=1e-13)
            np.testing.assert_allclose(z.sum(1),1,atol=1e-13)
            np.testing.assert_allclose(joint_distribution(s),joint_distribution(replace(s,order=48)),atol=2e-13)

    def test_config_separation(self):
        for k in (1,2): self.assertFalse(np.array_equal(mission_cpt(k,True),mission_cpt(k,True,True)))
        # Changing target severity cannot change the LV public signal marginal.
        np.testing.assert_allclose(joint_distribution(Scenario()).sum(1),
          joint_distribution(Scenario(target_severe=.8)).sum(1),atol=1e-13)

    def test_pgmpy_variable_elimination(self):
        from pgmpy.models import DiscreteBayesianNetwork
        from pgmpy.factors.discrete import TabularCPD
        from pgmpy.inference import VariableElimination
        for s in (Scenario(),Scenario(relevance=.5,rho=.15,revision_pair=(.25,)*4)):
            w,y,z=latent_model(s); n=len(w)
            model=DiscreteBayesianNetwork([('X','Y'),('X','Z')])
            model.add_cpds(TabularCPD('X',n,w[:,None]),
                           TabularCPD('Y',4,y.T,evidence=['X'],evidence_card=[n]),
                           TabularCPD('Z',3,z.T,evidence=['X'],evidence_card=[n]))
            self.assertTrue(model.check_model())
            infer=VariableElimination(model)
            result=infer.query(['Y','Z'],show_progress=False)
            arr=result.values
            if result.variables!=['Y','Z']: arr=arr.T
            j=joint_distribution(s)
            np.testing.assert_allclose(arr,j,atol=1e-12)
            for i in range(4):
                post=infer.query(['Z'],evidence={'Y':i},show_progress=False).values
                np.testing.assert_allclose(post,j[i]/j[i].sum(),atol=1e-12)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): posterior_nodes(Scenario(order=2))
        with self.assertRaises(ValueError): posterior_nodes(Scenario(theta=(1,1,1)))
        with self.assertRaises(ValueError): posterior_nodes(Scenario(history_detection=0))

if __name__=='__main__': unittest.main()
