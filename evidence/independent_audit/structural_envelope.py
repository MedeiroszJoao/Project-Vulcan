"""Recompute the decision frontier across *all* scenarios in the supplied structural grid.
This is an adversarial sensitivity extension USING src.model, not an independent implementation.
"""
import sys,itertools,csv
from dataclasses import replace
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,'/mnt/data/vulcan_audit_work/vulcan-decision')
from src.model import Scenario, joint_distribution, decision
root=Path('/mnt/data/Vulcan_Independent_Audit')
losses=np.linspace(250,2000,61);delays=np.linspace(0,100,51)
revisions={'HH':(1,0,0,0),'HM':(0,1,0,0),'MH':(0,0,1,0),'MM':(0,0,0,1),'unknown':(.25,)*4}
theta_grid=[(.6,.2,.2),(.2,.6,.2),(.1,.8,.1)]
results=[]
for prior,theta,rel,rho,rev,detect in itertools.product(('uniform','jeffreys'),theta_grid,(0,.5,1),(0,.25),revisions,(.7,1)):
    s=replace(Scenario(), prior=prior,theta=theta,relevance=rel,rho=rho,
              revision_pair=revisions[rev],history_detection=detect)
    j=joint_distribution(s)
    z=j.sum(axis=0);py=j.sum(axis=1)
    # exact expected cost for each L; no waiting cost before the last line
    cond_rates=np.divide(j@np.array([0.,.25,1.]),py,out=np.full(4,float(z@np.array([0.,.25,1.]))),where=py>0)
    G=np.array([.9,.3,.05,.4])
    alternative=30+losses*(.005+.25*.003)
    alt_later=alternative+5
    c_v=cond_rates[:,None]*losses[None,:]
    wait0=np.sum(py[:,None]*(G[:,None]*np.minimum(c_v,alt_later[None,:])+(1-G[:,None])*alt_later[None,:]),axis=0)
    gain=alternative-wait0
    results.append(gain)
R=np.stack(results)
lo=R.min(axis=0);hi=R.max(axis=0)
mat_lo=lo[None,:]-delays[:,None]
mat_hi=hi[None,:]-delays[:,None]
eps=.01
robust_wait=mat_lo>eps
robust_reallocate=mat_hi<-eps
mixed=(mat_lo < -eps)&(mat_hi > eps)
ambig=~(robust_wait|robust_reallocate|mixed)
print('structural map scenarios',len(R),'cells',mat_lo.size)
print('robust wait',int(robust_wait.sum()),'robust realocate',int(robust_reallocate.sum()),'mixed',int(mixed.sum()),'near-zero',int(ambig.sum()))
print('L=1000 representative, D=10',float(R[:,26].min()-10),float(R[:,26].max()-10))
with (root/'structural_envelope.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['delay_MUSD','loss_MUSD','min_net_wait_gain_MUSD','max_net_wait_gain_MUSD','status'])
    for i,d in enumerate(delays):
        for k,L in enumerate(losses):
            status='wait_all' if robust_wait[i,k] else 'reallocate_all' if robust_reallocate[i,k] else 'model_disagreement' if mixed[i,k] else 'boundary'
            w.writerow([d,L,mat_lo[i,k],mat_hi[i,k],status])
from matplotlib.colors import ListedColormap
status=np.where(robust_reallocate,0,np.where(robust_wait,1,np.where(mixed,2,3)))
fig,ax=plt.subplots(figsize=(8.3,5.8),layout='constrained')
im=ax.pcolormesh(losses,delays,status,cmap=ListedColormap(['#456388','#1e9c7a','#f1ab4d','#cccccc']),shading='auto',vmin=-.5,vmax=3.5)
cbar=fig.colorbar(im,ax=ax,ticks=[0,1,2,3]); cbar.ax.set_yticklabels(['Reallocate in all','Wait in all','Model disagreement','Near threshold'])
ax.set(xlabel='Loss consequence ($ millions)', ylabel='Waiting cost ($ millions)', title='Structural sensitivity envelope — all 360 scenarios\nNo probability assigned to models, no robustness claim outside this grid')
fig.savefig(root/'structural_envelope.png',dpi=170);plt.close(fig)
