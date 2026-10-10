"""Controlled precision/consequence-set sensitivity, not an EVSI experiment.
Run from repository root: python -m research.information_limits.experiment
"""
import itertools,json
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection
from scipy.special import roots_jacobi
from src.model import outcomes_given_p,Scenario

BASE=np.array([[.97,.02,.01],[.55,.20,.25],[.25,.20,.55]])
ZERO=np.array([.998,.001,.001])
POLICIES=[None]+list(itertools.product([0,1],repeat=4))
G=np.array([.9,.3,.05,.4])

@lru_cache(None)
def vertices():
    # Coordinates (a1,b1,a2,b2,a3,b3): a=P(degraded or loss), b=P(loss).
    h=[]
    def add(d,c):
        row=np.zeros(7)
        for k,v in d.items():row[k]=v
        row[-1]=c;h.append(row)
    for i in (0,2,4):
        add({i:1},-1);add({i:-1,i+1:1},0)
    add({0:-1},.002);add({1:-1},.001)
    for i in (0,1,2,3):add({i:1,i+2:-1},0)
    x=HalfspaceIntersection(np.array(h),np.array([.2,.1,.5,.3,.8,.6])).intersections
    x=np.array(sorted(map(tuple,np.round(x,12))))
    return np.array([[[1-v[i],v[i]-v[i+1],v[i+1]] for i in (0,2,4)] for v in x])

@lru_cache(None)
def kernel(precision,order=24):
    if precision is None:p,w=np.array([3/14]),np.ones(1)
    else:
        a=precision*3/14;b=precision-a
        x,w=roots_jacobi(order,b-1,a-1);p=(x+1)/2;w=w/w.sum()
    k=np.zeros((4,4))
    for mass,mult in [(.4,1.),(.6,.1)]:
        for point,weight in zip(p,w):
            q=mult*point;one=4*q*(1-q)**3;zero=(1-q)**4
            target=np.array([zero,.75*one,.25*one,1-zero-one])
            k+=mass*weight*np.outer(outcomes_given_p(q,Scenario()),target)
    return k

def joint(k,c):return k@np.vstack([ZERO,c])

def cost_matrix(precision,r):
    k=kernel(precision);costs=[]
    for v in vertices():
        j=joint(k,(1-r)*BASE+r*v);py=j.sum(1);loss=j@np.array([0.,250.,1000.])
        costs.append([35.75]+[10+np.sum((1-G*np.array(b))*py*40.75+G*np.array(b)*loss) for b in POLICIES[1:]])
    return np.array(costs)

def analyze(precision,r):
    c=cost_matrix(precision,r);regret=c-c.min(1)[:,None];n=len(c)
    res=linprog(np.r_[np.zeros(17),1.],A_ub=np.c_[regret,-np.ones(n)],b_ub=np.zeros(n),A_eq=[np.r_[np.ones(17),0]],b_eq=[1],bounds=[(0,None)]*18,method='highs')
    # Maximize minimum wait-policy cost over convex combinations of vertices.
    worst=linprog(np.r_[np.zeros(n),-1.],A_ub=np.c_[-c[:,1:].T,np.ones(16)],b_ub=np.zeros(16),A_eq=[np.r_[np.ones(n),0]],b_eq=[1],bounds=[(0,None)]*n+[(None,None)],method='highs')
    assert res.success and worst.success
    return {'precision':precision,'consequence_radius':r,'wait_gain_min':float(35.75+worst.fun),'wait_gain_max':float(35.75-c[:,1:].min()),'deterministic_regret':float(regret.max(0).min()),'deterministic_policy_index':int(regret.max(0).argmin()),'mixed_regret':float(res.fun),'mixture':[{'policy':POLICIES[i],'weight':float(w)} for i,w in enumerate(res.x[:-1]) if w>1e-9],'dual_gap':float(abs(res.fun-res.eqlin.marginals[0])),'max_constraint_violation':float(np.max(regret@res.x[:-1]-res.fun))}

def threshold(precision):
    # Nested sets around BASE. Largest radius with every wait policy >= now.
    def gap(r):return float(cost_matrix(precision,r)[:,1:].min()-35.75)
    if gap(0)<0:return None
    if gap(1)>=0:return [1.,1.]
    lo,hi=0.,1.
    while hi-lo>1e-10:
        mid=(lo+hi)/2
        if gap(mid)>=0:lo=mid
        else:hi=mid
    return [lo,hi]

def analytic_threshold(precision):
    c0=cost_matrix(precision,0)[:,1:];d=cost_matrix(precision,1)[:,1:]-c0
    if np.min(c0)<35.75:return None
    negative=d<0
    return float(min(1.,np.min((c0[negative]-35.75)/(-d[negative])))) if negative.any() else 1.


def run():
    precisions=[14,28,70,140,700,None];radii=[1,.75,.5,.25,.1,0]
    rows=[analyze(t,r) for t in precisions for r in radii]
    errors={str(t):float(np.max(np.abs(kernel(t,24)-kernel(t,48)))) for t in precisions}
    assert max(errors.values())<1e-12
    return {'units':'USD million','scope':'Controlled contraction, not expected value of future data; no physical calibration','policy_order':POLICIES,'vertices':vertices().tolist(),'grid':rows,'uniform_now_radius_brackets':{str(t):threshold(t) for t in precisions},'analytic_uniform_now_radii':{str(t):analytic_threshold(t) for t in precisions},'quadrature_max_abs_errors':errors}

if __name__=='__main__':
    data=run();Path('research/information_limits/results.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    for row in data['grid']:
        if row['consequence_radius'] in (1,.5,0):print(row['precision'],row['consequence_radius'],row['wait_gain_max'],row['mixed_regret'])
    print(data['uniform_now_radius_brackets'])
