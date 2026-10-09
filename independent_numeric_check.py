"""Independent implementation of reference model via adaptive numerical integration.
Does not import, call or reuse src.model in its numerical calculation.
Scenarios not Vulcan risk estimates.
"""
from math import comb
from scipy.integrate import quad
from scipy.stats import beta
import numpy as np, json

def outcome(n,q,target):
    ztot=np.zeros(3)
    ytot=np.zeros(4)
    for k in range(n+1):
        pk=comb(n,k)*q**k*(1-q)**(n-k)
        h=.25 if target else .20
        sev=1-(1-h)**k
        if k==0: z=np.array([.998,.001,.001])
        elif k>=2: z=np.array([.25,.2,.55] if target else [.4,.2,.4])
        else:
            mild=np.array([.97,.02,.01] if target else [.985,.010,.005])
            strong=np.array([.55,.2,.25] if target else [.75,.15,.10])
            z=(1-sev)*mild+sev*strong
        if target: ztot+=pk*z
        else:
            detection=1-(1-.9)**k
            y=np.array([.9*z[0]*(1-detection),.9*z[0]*detection,.9*(z[1]+z[2]),.1])
            ytot+=pk*y
    return ztot if target else ytot

def calc_joint():
    J=np.zeros((4,3)); theta=[.2,.6,.2]
    for t, wt in enumerate(theta):
        def q_of_p(p):
            return p if t!=1 else .1*p
        for i in range(4):
            for k in range(3):
                def integrand(p):
                    q=q_of_p(p)
                    return beta.pdf(p,3,11)*outcome(6,q,False)[i]*outcome(4,q,True)[k]
                J[i,k]+=wt*quad(integrand,0,1,epsabs=2e-12,epsrel=1e-11)[0]
    return J
J=calc_joint(); py=J.sum(axis=1); z=J.sum(axis=0)
L=1000; alt=30+L*(.005+.25*.003)
conditional=(J@np.array([0,.25*L,L]))/py
pure_evsi=min(z@np.array([0,.25*L,L]),alt)-py@np.minimum(conditional,alt)
approval=np.array([.9,.3,.05,.4]); alt_later=alt+5
wait_cost=10+np.sum(py*(approval*np.minimum(conditional,alt_later)+(1-approval)*alt_later))
reference=json.load(open('results/reference.json'))
rawjoint=json.load(open('results/reference_joint.json'))
print('INDEPENDENT_REFERENCE_JOINT_MAX_ABS_DIFF',np.max(np.abs(J-np.array(rawjoint))))
print('INDEPENDENT_EVSI',pure_evsi, 'PROJECT_EVSI',reference['evsi'])
print('INDEPENDENT_WAIT_COST',wait_cost,'PROJECT_WAIT_COST',reference['wait_cost'])
print('INDEPENDENT_NET_WAIT_GAIN',alt-wait_cost)
print('MAX_NUMERIC_ERROR',max(abs(pure_evsi-reference['evsi']),abs(wait_cost-reference['wait_cost'])))
result={'max_abs_joint_error':float(np.max(np.abs(J-np.array(rawjoint)))),'independent_evsi':float(pure_evsi),'independent_wait_cost':float(wait_cost),'independent_net_wait_gain':float(alt-wait_cost),'project_evsi':reference['evsi'],'project_wait_cost':reference['wait_cost']}
open('results/independent_numeric_results.json','w').write(json.dumps(result,indent=2)+'\n')
