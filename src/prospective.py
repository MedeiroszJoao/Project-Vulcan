"""Prospective, *scenario-conditional* probabilistic forecast and proper scoring.

Not calibrated launch reliability probabilities. Distinguishes latent physical events
from modeled availability/detection and the publicly observed signal.
"""
import math
from dataclasses import replace, asdict
import numpy as np
from .model import Scenario, posterior_nodes, regime_risk, count_pmf, joint_distribution, Y_NAMES

COUNT_UNREPORTED = 'count_not_ascertainable'

def physical_count_forecast(s: Scenario):
    """Return P(K=k), k=0..n_lv, integrating all uncertain parameters.

    Only the LV revision marginal is relevant; M* revision / transfer weight
    have no effect on the unconditional forecast for LV-01.
    """
    p, w = posterior_nodes(s)
    out = np.zeros(s.n_lv + 1, dtype=float)
    for pair_prob, (lv_modified, _) in zip(s.revision_pair,
            [(False,False),(False,True),(True,False),(True,True)]):
        if pair_prob <= 0:
            continue
        for theta_idx, theta_prob in enumerate(s.theta):
            for pi, wi in zip(p,w):
                q=regime_risk(pi,theta_idx,lv_modified,s)
                out += pair_prob * theta_prob * wi * count_pmf(s.n_lv,q,s.rho)
    assert np.isclose(out.sum(),1.0,atol=1e-12)
    return out

def reported_count_forecast(s: Scenario):
    """Hypothetical disclosed anomaly-count signal, NOT physical K.

    A disclosure indicator d is assumed independent of state. Conditional on
    disclosure, physical anomaly detections thin K with probability detection.
    At K=0 the reference false-positive probability is the chance of reporting
    one anomaly.  This is a *secondary*, observation-model-dependent endpoint.
    """
    pmf = physical_count_forecast(s)
    observed = np.zeros(s.n_lv+1)
    missing = 0.
    for k, mass in enumerate(pmf):
        disclosure=s.anomaly_disclosure if s.mnar and k>0 else s.disclosure
        missing += mass*(1-disclosure)
        mass *= disclosure
        if k == 0:
            observed[0] += mass*(1-s.false_positive)
            observed[1] += mass*s.false_positive
            continue
        for r in range(k+1):
            observed[r] += mass*math.comb(k,r)*s.detection**r*(1-s.detection)**(k-r)
    return [float(z) for z in observed] + [float(missing)]

def categorical_score(probs, outcome_index):
    """Lower is better. Multiclass Brier sum_i(p_i-1{i=y})^2 (0..2).

    Log loss -ln p_y. Zero-probability realized event has infinite log loss;
    NEVER clip silently or choose an epsilon after seeing an outcome.
    """
    a=np.asarray(probs,dtype=float)
    if a.ndim != 1 or not np.isclose(a.sum(),1.0,atol=1e-11,rtol=0) or not np.all(np.isfinite(a)) or np.any(a<0) or np.any(a>1):
        raise ValueError('invalid categorical probabilities')
    if not isinstance(outcome_index,int) or not (0<=outcome_index<len(a)):
        raise ValueError('invalid observed outcome')
    target=np.zeros(len(a)); target[outcome_index]=1.
    return {'brier_multiclass_sum':float(np.sum((a-target)**2)),
            'negative_log_likelihood_nats':float(-np.log(a[outcome_index])) if a[outcome_index] > 0 else None,
            'zero_probability_observed':bool(a[outcome_index]==0)}

def build_forecast(s=None):
    s = s or Scenario()
    y = joint_distribution(s).sum(axis=1)
    physical = physical_count_forecast(s)
    report = reported_count_forecast(s)
    return {
       'episode_id':'VULCAN_LV01_2026_01',
       'asof_nominal_date':'2026-10-09',
       'status':'freeze_candidate_UNPUBLISHED',
       'event':'Amazon Leo LV-01, Vulcan VC6L; outcome conditional on flight occurring',
       'scope':'ILLUSTRATIVE MODEL-IMPLIED SCENARIO FORECAST; not calibrated actual launch probability',
       'reference_configuration':'Scenario() model defaults; MM revision is HYPOTHESIS, not verified hardware',
       'target':'four-category public reporting signal at end of the 14th UTC calendar day after liftoff',
       'valid_until_utc_exclusive':'2027-01-01T00:00:00Z',
       'forecast_valid_from_rule':'independently verified public registration before liftoff',
       'configuration_change_rule':'six boosters and nominal VC6L unchanged; otherwise episode void, not rescored',
       'evaluation_cutoff_rule':'00:00:00 UTC at start of liftoff_date + 15 days; evidence timestamps strictly earlier',
       'full_scenario_parameters':asdict(s),
       'report_signal_categories':Y_NAMES,
       'public_report_signal_pmf':[float(t) for t in y],
       'physical_anomaly_count_categories':list(range(s.n_lv+1)),
       'latent_physical_anomaly_count_pmf':[float(t) for t in physical],
       'count_report_categories':[str(k) for k in range(s.n_lv+1)]+[COUNT_UNREPORTED],
       'hypothetical_disclosed_count_pmf':report,
       'primary_score':'multiclass Brier SUM and negative natural log probability on Y at T+14d',
       'secondary_count_score':'DO NOT SCORE unless a separately predeclared count ascertainment protocol is met',
       'event_disposition':'Delay within validity preserves primary forecast; no liftoff by expiry => NOT_LAUNCHED and no score. Later flight requires a new prospective episode.',
       'T_plus_72_hours':'publish preliminary evidence collection without revising the primary forecast',
       'T_plus_14_days':'one and only primary Y coding; incomplete reporting => inconclusive',
       'scenario_parameters':{
           'prior':s.prior,'theta':list(s.theta),'revision_pair_HH_HM_MH_MM':list(s.revision_pair),
           'rho':s.rho,'history_detection':s.history_detection,'correction_multiplier':s.effective_multiplier,
           'ineffective_increment':s.ineffective_increment,'detection':s.detection,
           'disclosure':s.disclosure,'false_positive':s.false_positive,'n_lv':s.n_lv,
       }
    }
