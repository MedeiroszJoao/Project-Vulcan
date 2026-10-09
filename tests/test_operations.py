import unittest
from dataclasses import replace
import numpy as np
from src.model import Scenario,joint_distribution,decision,posterior_nodes
from src.operations import gate_joint,operational_decision

class OperationsTests(unittest.TestCase):
    def test_baseline_recovery(self):
        s=Scenario();j=gate_joint(s)
        np.testing.assert_allclose(j.sum(axis=1),joint_distribution(s),atol=1e-14)
        a=operational_decision(j,slot=1,no_launch_cost=1e6)
        b=decision(joint_distribution(s),delay_cost=10)
        self.assertAlmostEqual(a['wait_cost'],b['wait_cost'],places=10)
    def test_private_gate_reweights_risk(self):
        j=gate_joint(Scenario(),strength=1)
        risks=j@np.array([0,.25,1]); probs=j.sum(axis=2)
        self.assertTrue(np.all(risks[:,1]/probs[:,1]<risks[:,0]/probs[:,0]))
        np.testing.assert_allclose(j.sum(axis=1),joint_distribution(Scenario()),atol=1e-14)
    def test_private_information_without_lv_transfer(self):
        j=gate_joint(replace(Scenario(),relevance=0),strength=1)
        risk=j@np.array([0,.25,1]);mass=j.sum(axis=2)
        self.assertTrue(np.all(risk[:,1]/mass[:,1]<risk[:,0]/mass[:,0]))
        np.testing.assert_allclose(j.sum(axis=1),joint_distribution(replace(Scenario(),relevance=0)),atol=1e-14)
    def test_unavailable_launchers_defer(self):
        r=operational_decision(gate_joint(Scenario()),slot=0,approval_in_time=False)
        self.assertAlmostEqual(r['wait_cost'],110)
        self.assertTrue(all(p['action']=='defer' for p in r['policy'] if p['probability']>0))
    def test_reservation_fee_and_slot(self):
        j=gate_joint(Scenario());a=operational_decision(j,slot=1)
        b=operational_decision(j,reserve=True,reserve_cost=7,reserved_slot=1)
        self.assertAlmostEqual(b['wait_cost']-a['wait_cost'],7)
        self.assertGreaterEqual(operational_decision(j,slot=0)['wait_cost'],a['wait_cost'])
    def test_severity_and_mnar(self):
        s=Scenario();j=joint_distribution(s)
        high=joint_distribution(replace(s,target_multi_loss=.8))
        self.assertGreater(high[:,2].sum(),j[:,2].sum())
        np.testing.assert_allclose(j.sum(axis=1),high.sum(axis=1),atol=1e-14)
        m=joint_distribution(replace(s,mnar=True,anomaly_disclosure=.3))
        self.assertGreater(m[3].sum(),j[3].sum())
        self.assertGreater(m[3,2]/m[3].sum(),j[3,2]/j[3].sum())
    def test_heterogeneous_history_quadrature(self):
        s=replace(Scenario(),history_detection_by_flight=(.7,1,.8,1),history_risk_multipliers=(1,1,.5,.5))
        np.testing.assert_allclose(joint_distribution(s),joint_distribution(replace(s,order=48)),atol=1e-13)
        p,w=posterior_nodes(s);q,v=posterior_nodes(Scenario())
        self.assertGreater(p@w,q@v)

if __name__=='__main__':unittest.main()
