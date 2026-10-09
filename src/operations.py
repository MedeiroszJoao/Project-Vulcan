"""Scenario gate and feasible opportunities; never calibrated regulator behavior."""
import numpy as np
from .model import latent_model

def gate_joint(s, strength=0., approval=(.9,.3,.05,.4)):
    """P(Y,G,Z): G responds to a latent risk score, not future realized Z.
    strength=0 reproduces G independent of Z given Y. Positive strength makes
    permission less likely for latent states with higher expected target loss.
    This is a reduced-form private-evidence scenario, not a telemetry model.
    """
    if not 0<=strength<=1 or len(approval)!=4 or any(not 0<=v<=1 for v in approval): raise ValueError('gate')
    w,y,z=latent_model(s,retain_target_latent=True)
    score=z@np.array([0,.25,1])
    g=np.array(approval)[None,:]*(1-strength*score[:,None])
    approved=np.einsum('i,iy,iy,iz->yz',w,y,g,z)
    total=np.einsum('i,iy,iz->yz',w,y,z)
    return np.stack([total-approved,approved],axis=1)

def operational_decision(j, loss=1000., delay_cost=10., slot=.9, integration_ok=True,
                         approval_in_time=True, target_ready=True, reserve=False, reserve_cost=10.,
                         reserved_slot=1., no_launch_cost=100., alternative_now=True):
    """Observe (Y,G), then slot availability. If no feasible launcher, defer M*.
    Slot is independent of technical state by assumption. Deferral cost includes
    all consequences in a declared scenario; it is not automatically payload loss.
    Reserving is a t0 action paid in every waiting branch; fee is non-refundable.
    integration_ok refers to the later alternative, not the target launcher.
    """
    j=np.asarray(j)
    if j.shape!=(4,2,3) or np.any(j<0) or not np.isclose(j.sum(),1): raise ValueError('joint')
    if any(not 0<=x<=1 for x in (slot,reserved_slot)): raise ValueError('slot')
    if min(loss,delay_cost,reserve_cost,no_launch_cost)<0: raise ValueError('cost')
    alt=30+.00575*loss; later=alt+5
    q=(reserved_slot if reserve else slot) if integration_ok else 0.
    cost=delay_cost+(reserve_cost if reserve else 0.)
    policy=[]
    for y in range(4):
        for g in range(2):
            py=j[y,g].sum()
            if py==0: continue
            cv=float(j[y,g]@np.array([0,.25*loss,loss])/py)
            for available,p in [(True,q),(False,1-q)]:
                choices={'defer':no_launch_cost}
                if available: choices['alternative']=later
                if g and approval_in_time and target_ready: choices['vulcan']=cv
                action=min(choices,key=choices.get)
                cost+=py*p*choices[action]
                policy.append(dict(y=y,approved=g,slot=available,probability=float(py*p),action=action))
    now=min(alt,no_launch_cost) if alternative_now else no_launch_cost
    return dict(wait_cost=float(cost),now_cost=now,net_wait_gain=float(now-cost),policy=policy)
