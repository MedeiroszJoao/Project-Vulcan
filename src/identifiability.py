"""Ex-post, separate scientific extension. Never modifies original LV-01 forecast.

Target consequence CPTs are hypothetical mathematics, not rocket safety data.
"""
from dataclasses import dataclass
from math import log
import numpy as np
from scipy.special import roots_jacobi
from .model import (Scenario, HISTORY, count_pmf, decision, joint_distribution,
                    outcomes_given_p, posterior_nodes, regime_risk,
                    reported_count_likelihood, validate)

@dataclass(frozen=True)
class TargetWorld:
    name: str
    one_nonsevere: tuple
    one_severe: tuple
    multiple: tuple
    zero: tuple = (.998, .001, .001)

    def __post_init__(self):
        for row in (self.zero, self.one_nonsevere, self.one_severe, self.multiple):
            if len(row) != 3 or min(row) < 0 or not np.isclose(sum(row), 1, atol=1e-12):
                raise ValueError("Target consequence CPT rows must sum to one")

BASELINE=TargetWorld("current_reference",(.970,.020,.010),(.550,.200,.250),(.250,.200,.550))
OPTIMISTIC=TargetWorld("low_consequence_witness",(.994,.005,.001),(.980,.015,.005),(.950,.040,.010))
ADVERSE=TargetWorld("high_consequence_witness",(.600,.100,.300),(.150,.150,.700),(.050,.150,.800))
WORLDS=(BASELINE,OPTIMISTIC,ADVERSE)
ALL_SUCCESS=TargetWorld("all_success_if_K_positive",(1.,0.,0.),(1.,0.,0.),(1.,0.,0.))
ALL_LOSS=TargetWorld("all_loss_if_K_positive",(0.,0.,1.),(0.,0.,1.),(0.,0.,1.))

def target_outcome_probs(q,s,world):
    result=np.zeros(3)
    for k,pk in enumerate(count_pmf(s.n_target,q,s.rho)):
        if k==0:
            result += pk*np.asarray(world.zero)
        elif k==1:
            v=s.target_severe
            result += pk*((1-v)*np.asarray(world.one_nonsevere)+v*np.asarray(world.one_severe))
        else:
            result += pk*np.asarray(world.multiple)
    return result

def joint_with_target_world(s,world):
    """Retain original latent transfer factorization; vary only target outcome CPT."""
    validate(s)
    p,post=posterior_nodes(s)
    w=np.tile(post,len(s.theta))*np.repeat(np.asarray(s.theta),len(p))
    ys={};zs={}
    for modified in (False,True):
        ys[modified]=np.asarray([outcomes_given_p(regime_risk(q,t,modified,s),s)
                                 for t in range(3) for q in p])
        zs[modified]=np.asarray([target_outcome_probs(regime_risk(q,t,modified,s),s,world)
                                 for t in range(3) for q in p])
    j=np.zeros((4,3))
    for pairprob,(lv,mt) in zip(s.revision_pair,
                                ((False,False),(False,True),(True,False),(True,True))):
        if not pairprob: continue
        shared=s.relevance if lv==mt else 0.
        if shared:
            j += pairprob*shared*np.einsum("i,iy,iz->yz",w,ys[lv],zs[mt])
        if shared<1:
            j += pairprob*(1-shared)*np.outer(w@ys[lv],w@zs[mt])
    if not np.isclose(j.sum(),1.,atol=1e-11):
        raise AssertionError("joint normalization")
    return j

def historical_log_evidence(s):
    """Marginal evidence of four historical reported booster-count rows only."""
    validate(s)
    a=b=1. if s.prior=="uniform" else .5
    b += 32*s.heritage_weight
    x,w=roots_jacobi(s.order,b-1,a-1)
    p=(x+1)/2
    w/=w.sum()
    h=np.asarray([np.prod([
       reported_count_likelihood(n,k,q*s.history_risk_multipliers[i],s.rho,
          (s.history_detection_by_flight or (s.history_detection,)*4)[i])
       for i,(n,k) in enumerate(HISTORY)]) for q in p])
    return log(float(w@h))

def assess_worlds(s=Scenario(),delay_cost=10.):
    """Counterexamples: identical observed likelihood and Y, opposite decisions."""
    le=historical_log_evidence(s)
    baseline_y=joint_distribution(s).sum(axis=1)
    rows=[]
    for world in WORLDS:
        j=joint_with_target_world(s,world)
        d=decision(j,delay_cost=delay_cost)
        d0=decision(j,delay_cost=0.)
        if not np.allclose(j.sum(axis=1),baseline_y,atol=1e-11):
            raise AssertionError("LV observation forecast must be invariant")
        rows.append({
            "world":world.name,"historical_log_evidence":le,
            "probability_y":j.sum(axis=1).tolist(),
            "target_loss_probability":float(j.sum(axis=0)[2]),
            "target_expected_loss_MUSD":float(j.sum(axis=0)@np.array([0,250,1000])),
            "wait_cost_MUSD":d["wait_cost"],
            "reallocate_cost_MUSD":d["realocate_now_cost"],
            "net_wait_gain_MUSD":d["net_wait_gain"],
            "delay_break_even_MUSD":d0["net_wait_gain"],
            "preferred_action":d["preferred"]})
    gains=[r["net_wait_gain_MUSD"] for r in rows]
    return {
      "scientific_status":"MODEL-SPECIFIC NON-IDENTIFICATION WITNESS; NOT PHYSICAL VALIDATION",
      "historical_data_likelihood_scope":"four rows of reported booster counts only",
      "changed":"target M* consequence CPT conditional on K and severity; all others fixed",
      "reference_lv_y_probability":baseline_y.tolist(),
      "delay_cost_MUSD":delay_cost,
      "worlds":rows,
      "witness_envelope_net_wait_gain_MUSD":[min(gains),max(gains)],
      "decision_changes_sign":min(gains)<0<max(gains),
      "minimax_regret_over_three_illustrative_worlds_MUSD":{
       "reallocate_now":max(0.,max(gains)),"wait":max(0.,-min(gains))},
      "caution":"Constructed witnesses are not an empirical admissible class or posterior confidence."
    }

def exact_simplex_bounds(s=Scenario(),delay_cost=10.):
    """Sharp decision bounds if all K>=1 target CPT rows range over full simplexes.

    For fixed P(Y), fixed P(K_target|Y), K=0 CPT, approval, and costs,
    the wait cost is nondecreasing in every future-target expected loss.
    Extreme rows all-success / all-loss therefore attain both bounds.
    Not a physically credible interval or actual mission risk estimate.
    """
    good=decision(joint_with_target_world(s,ALL_SUCCESS),delay_cost=delay_cost)
    bad=decision(joint_with_target_world(s,ALL_LOSS),delay_cost=delay_cost)
    lo=bad["net_wait_gain"]; hi=good["net_wait_gain"]
    if lo>hi+1e-10: raise AssertionError("ordered-cost monotonicity")
    regret_wait=max(0.,-lo); regret_realloc=max(0.,hi)
    return {
      "scope":"Exact under fully unconstrained K>=1 target-consequence CPT simplexes; other inputs fixed",
      "zero_K_CPT_fixed":BASELINE.zero,
      "lower_net_wait_gain_MUSD":lo,
      "upper_net_wait_gain_MUSD":hi,
      "robust_action":"wait" if lo>0 else "reallocate_now" if hi<0 else "undetermined",
      "max_regret_wait_MUSD":regret_wait,
      "max_regret_reallocate_now_MUSD":regret_realloc,
      "minimax_regret_action_within_this_set":"wait" if regret_wait<regret_realloc else "reallocate_now",
      "proof":"Nonnegative weights and ordered loss imply wait cost monotone in each CPT conditional expected loss. Both pointwise extreme rows attain the bounds.",
      "caution":"Broad mathematical set only; extremes are NOT physical risk estimates. Alternative pricing, observation, gate, and calendar are held fixed."
    }
