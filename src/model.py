"""Public-data decision laboratory. All engineering CPTs are scenario assumptions.

No simulation: enumerate finite outcomes and integrate polynomial likelihoods
against Beta priors by Gauss-Jacobi quadrature (exact to polynomial degree).
"""
from dataclasses import dataclass
from math import comb
import numpy as np
from scipy.special import roots_jacobi

Y_NAMES = ['clean_report', 'anomaly_report', 'loss_or_degraded_report', 'inconclusive']
Z_NAMES = ['success', 'degraded', 'loss']
REGIMES = ['historical_equivalent', 'effective_correction', 'ineffective_correction']
HISTORY = [(2, 0), (2, 1), (4, 0), (4, 1)]

@dataclass(frozen=True)
class Scenario:
    prior: str = 'uniform'
    heritage_weight: float = 0.0
    theta: tuple = (0.20, 0.60, 0.20)
    # HH, HM, MH, MM. Unknown is a distribution, not a physical type.
    revision_pair: tuple = (0.0, 0.0, 0.0, 1.0)
    relevance: float = 1.0
    rho: float = 0.0
    history_detection: float = 1.0
    detection: float = 0.90
    disclosure: float = 0.90
    false_positive: float = 0.0
    effective_multiplier: float = 0.10
    ineffective_increment: float = 0.0
    lv_severe: float = 0.20
    target_severe: float = 0.25
    history_detection_by_flight: tuple = ()
    history_risk_multipliers: tuple = (1., 1., 1., 1.)
    anomaly_disclosure: float = .90
    mnar: bool = False
    target_multi_loss: float = .55
    n_lv: int = 6
    n_target: int = 4
    order: int = 24

def validate(s):
    if s.prior not in ('uniform', 'jeffreys'): raise ValueError('prior')
    for v in (s.theta, s.revision_pair):
        if any(x < 0 for x in v) or not np.isclose(sum(v), 1): raise ValueError('probabilities')
    if len(s.theta) != 3 or len(s.revision_pair) != 4: raise ValueError('shape')
    for v in (s.heritage_weight,s.relevance,s.rho,s.history_detection,s.detection,
              s.disclosure,s.false_positive,s.effective_multiplier,
              s.ineffective_increment,s.lv_severe,s.target_severe):
        if not 0 <= v <= 1: raise ValueError('probability outside [0,1]')
    if len(s.history_risk_multipliers)!=4 or any(not 0<x<=1 for x in s.history_risk_multipliers): raise ValueError('historical multipliers')
    if s.history_detection_by_flight and (len(s.history_detection_by_flight)!=4 or any(not 0<x<=1 for x in s.history_detection_by_flight)): raise ValueError('historical detection')
    if not 0<=s.anomaly_disclosure<=1 or not 0<=s.target_multi_loss<=.8: raise ValueError('extended CPT')
    if s.history_detection == 0: raise ValueError('positive reported history impossible')
    if not (1 <= s.n_lv <= 6 and 1 <= s.n_target <= 6): raise ValueError('booster counts')
    if 2*s.order-1 < 12+s.n_lv+s.n_target: raise ValueError('insufficient quadrature order')

def count_pmf(n, p, rho=0):
    """Mixture: iid with probability 1-rho; all share Bernoulli(p) with rho.
    Marginal p is unchanged; pairwise correlation conditional on p equals rho.
    The all-or-none branch is a stress model, not an inferred physical mechanism.
    """
    v=np.array([comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1)])*(1-rho)
    v[0]+=rho*(1-p); v[-1]+=rho*p
    return v

def reported_count_likelihood(n, observed, p, rho, sensitivity):
    return sum(pk*comb(k,observed)*sensitivity**observed*(1-sensitivity)**(k-observed)
               for k,pk in enumerate(count_pmf(n,p,rho)) if k>=observed)

def posterior_nodes(s):
    validate(s)
    a=b=1.0 if s.prior=='uniform' else 0.5
    # Fixed-power heritage likelihood assumes 32 independent, perfectly observed
    # non-anomalous motor exposures. Sensitivity-only; not the main analysis.
    b += 32*s.heritage_weight
    x,w=roots_jacobi(s.order,b-1,a-1)
    p=(x+1)/2; w=w/w.sum()
    likelihood=np.array([np.prod([reported_count_likelihood(n,k,q*s.history_risk_multipliers[i],s.rho,
                                     (s.history_detection_by_flight or (s.history_detection,)*4)[i])
                                 for i,(n,k) in enumerate(HISTORY)]) for q in p])
    weights=w*likelihood
    if weights.sum()<=0: raise ValueError('impossible history')
    return p, weights/weights.sum()

def regime_risk(p, theta, modified, s):
    if not modified or theta==0: return p
    if theta==1: return s.effective_multiplier*p
    return p+(1-p)*s.ineffective_increment

def mission_cpt(k, severe, target=False):
    # Separate LV and target tables. No learning of compensation from LV outcomes.
    if k==0: return np.array([.998,.001,.001])
    if target:
        if k>=2: return np.array([.25,.20,.55])
        return np.array([.55,.20,.25] if severe else [.97,.02,.01])
    if k>=2: return np.array([.40,.20,.40])
    return np.array([.75,.15,.10] if severe else [.985,.010,.005])

def outcomes_given_p(p,s,target=False):
    n=s.n_target if target else s.n_lv
    severe_prob=s.target_severe if target else s.lv_severe
    out=np.zeros(3 if target else 4)
    for k, pk in enumerate(count_pmf(n,p,s.rho)):
        sev=1-(1-severe_prob)**k
        for severe,ps in [(False,1-sev),(True,sev)]:
            z=mission_cpt(k,severe,target)
            if target and k>=2: z=np.array([.8-s.target_multi_loss,.2,s.target_multi_loss])
            if target: out+=pk*ps*z; continue
            # Priority: missing disclosure, then degraded/loss, then reported anomaly.
            detect=1-(1-s.detection)**k if k else s.false_positive
            disclosure=s.anomaly_disclosure if s.mnar and k>0 else s.disclosure
            y=np.array([disclosure*z[0]*(1-detect),disclosure*z[0]*detect,
                        disclosure*(z[1]+z[2]),1-disclosure])
            out+=pk*ps*y
    return out

def latent_model(s, retain_target_latent=False):
    """Return weights and Y/Z CPT rows for an explicit finite latent mixture.
    Matched revision: shared technical hypothesis/p with probability relevance.
    Mismatched revision: independent copies (strict no-transfer scenario).
    Revision-pair uncertainty can still transmit evidence via the revision itself.
    """
    p,w=posterior_nodes(s)
    weights=np.array([pt*wp for pt in s.theta for wp in w])
    ys={}; zs={}
    for modified in (False,True):
        ys[modified]=np.array([outcomes_given_p(regime_risk(q,t,modified,s),s)
                              for t in range(3) for q in p])
        zs[modified]=np.array([outcomes_given_p(regime_risk(q,t,modified,s),s,True)
                              for t in range(3) for q in p])
    W=[]; Y=[]; Z=[]
    for prob,(rl,rm) in zip(s.revision_pair,[(False,False),(False,True),(True,False),(True,True)]):
        if prob==0: continue
        shared=s.relevance if rl==rm else 0.
        if shared:
            for i,wi in enumerate(weights):
                if wi>0: W.append(prob*shared*wi);Y.append(ys[rl][i]);Z.append(zs[rm][i])
        if shared<1:
            if retain_target_latent:
                for i,wi in enumerate(weights):
                    if wi>0: W.append(prob*(1-shared)*wi);Y.append(weights@ys[rl]);Z.append(zs[rm][i])
            else:
                W.append(prob*(1-shared));Y.append(weights@ys[rl]);Z.append(weights@zs[rm])
    return np.array(W),np.array(Y),np.array(Z)

def joint_distribution(s):
    w,y,z=latent_model(s)
    return np.einsum('i,iy,iz->yz',w,y,z)

def decision(joint, loss=1000., degraded_fraction=.25, alternative_cost=30.,
             alternative_loss=.005, alternative_degraded=.003, delay_cost=0.,
             approval=(.90,.30,.05,.40), later_alternative_cost=5.):
    """Amounts USD millions. EVSI holds action sets fixed (counterfactual).
    Net waiting policy observes Y and actual G approval, then selects feasible action.
    Approval is a user scenario P(G|Y), not evidence learned from public history.
    """
    j=np.asarray(joint,float)
    if j.shape!=(4,3) or np.any(j< -1e-12) or not np.isclose(j.sum(),1): raise ValueError('joint')
    if min(loss,alternative_cost,delay_cost,later_alternative_cost)<0: raise ValueError('negative cost')
    if len(approval)!=4 or any(not 0<=x<=1 for x in approval): raise ValueError('approval')
    if not (0<=degraded_fraction<=1 and 0<=alternative_loss and 0<=alternative_degraded
            and alternative_loss+alternative_degraded<=1): raise ValueError('utility parameters')
    py=j.sum(axis=1); z=j.sum(axis=0)
    loss_vector=np.array([0,degraded_fraction*loss,loss])
    alt=alternative_cost+loss*(alternative_loss+degraded_fraction*alternative_degraded)
    unconditional_v=float(z@loss_vector)
    conditional=np.divide(j@loss_vector,py,out=np.full(4,unconditional_v),where=py>0)
    before=min(unconditional_v,alt)
    after=float(py@np.minimum(conditional,alt))
    evsi=before-after
    # All waiting branches pay the incremental waiting cost; fallback pays its own extra cost.
    alt_later=alt+later_alternative_cost
    approved_best=np.minimum(conditional,alt_later)
    g=np.array(approval)
    waiting=delay_cost+float(py@(g*approved_best+(1-g)*alt_later))
    return dict(evsi=evsi,wait_cost=waiting,realocate_now_cost=alt,
                net_wait_gain=alt-waiting,counterfactual_launch_cost=unconditional_v,
                counterfactual_constraint_cost=alt-before,
                y_probability=py.tolist(),target_outcome=z.tolist(),
                conditional_target_loss=conditional.tolist(),
                policy_if_approved=['vulcan' if v<alt_later else 'alternative' for v in conditional],
                policy_if_denied=['alternative']*4,
                preferred='wait' if waiting<alt else 'realocate_now')
