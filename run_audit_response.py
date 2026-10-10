"""Reproduce audit envelope and scenario extensions; run after run_analysis.py."""
from pathlib import Path
from dataclasses import replace
from datetime import date,timedelta
import csv,itertools,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from src.model import Scenario,joint_distribution,decision
from src.operations import gate_joint,operational_decision
from run_analysis import csv_write

OUT=Path('results')
losses=np.linspace(250,2000,61);delays=np.linspace(0,100,51)
rev={'HH':(1,0,0,0),'HM':(0,1,0,0),'MH':(0,0,1,0),'MM':(0,0,0,1),'unknown':(.25,)*4}
gains=[]
for prior,theta,rel,rho,r,d in itertools.product(('uniform','jeffreys'),[(.6,.2,.2),(.2,.6,.2),(.1,.8,.1)],(0,.5,1),(0,.25),rev,(.7,1)):
    j=joint_distribution(Scenario(prior=prior,theta=theta,relevance=rel,rho=rho,revision_pair=rev[r],history_detection=d))
    gains.append([decision(j,loss=L)['net_wait_gain'] for L in losses])
gains=np.array(gains);lo=gains.min(axis=0)[None,:]-delays[:,None];hi=gains.max(axis=0)[None,:]-delays[:,None]
status=np.where(lo>.01,1,np.where(hi<-.01,0,np.where((lo<-.01)&(hi>.01),2,3)))
labels=['reallocate_all','wait_all','model_disagreement','boundary']
rows=[dict(delay_MUSD=D,loss_MUSD=L,min_net_wait_gain_MUSD=lo[i,k],max_net_wait_gain_MUSD=hi[i,k],status=labels[status[i,k]]) for i,D in enumerate(delays) for k,L in enumerate(losses)]
csv_write(OUT/'structural_envelope.csv',rows)
received=list(csv.DictReader(open('evidence/independent_audit/structural_envelope.csv')))
assert len(received)==len(rows)
for a,b in zip(rows,received):
    assert a['status']==b['status']
    for key in ('min_net_wait_gain_MUSD','max_net_wait_gain_MUSD'): assert abs(a[key]-float(b[key]))<1e-10
summary={v:int((status==i).sum()) for i,v in enumerate(labels)}
fig,ax=plt.subplots(figsize=(10,6),layout='constrained')
im=ax.pcolormesh(losses,delays,status,cmap=ListedColormap(['#456388','#1e9c7a','#f1ab4d','#cccccc']),vmin=-.5,vmax=3.5)
c=fig.colorbar(im,ax=ax,ticks=[0,1,2,3]);c.ax.set_yticklabels(['Reallocate in all','Wait in all','Model disagreement','Near threshold'])
ax.set(xlabel='Loss consequence (USD million)',ylabel='Incremental waiting cost (USD million)',title='Structural sensitivity across 360 scenarios\nIllustrative assumptions; not a rocket safety estimate')
fig.savefig(OUT/'structural_envelope.png',dpi=160);plt.close(fig)
# One-factor physics stress tests, separate from the original 360 envelope.
controls=[]
for field,values in {'target_multi_loss':(.1,.3,.55,.8),'history_risk_multipliers':[(1,1,1,1),(1,1,.5,.5),(.5,.5,1,1)],'history_detection_by_flight':[(1,1,1,1),(.7,1,.7,1)],'anomaly_disclosure':(.3,.6,.9)}.items():
    for value in values:
        s=replace(Scenario(),**{field:value},**({'mnar':True} if field=='anomaly_disclosure' else {}))
        result=decision(joint_distribution(s),delay_cost=10)
        controls.append(dict(parameter=field,value=str(value),net_wait_gain_MUSD=result['net_wait_gain'],evsi_MUSD=result['evsi']))
csv_write(OUT/'audit_physics_controls.csv',controls)
# Timing is measured from the actual hypothetical signal date, never NET alone.
# M* main planning window moved to Jan15--Mar15 2027; old window stress retained.
rows=[]
for strength in (0,.5,1):
    joint=gate_joint(Scenario(),strength=strength)
    for launch,lead,gate_days,slot,reserve,window in itertools.product((date(2026,10,29),date(2026,10,31),date(2026,12,1)),(30,90),(0,30),(0,.5,1),(False,True),('original','planning')):
        signal=launch+timedelta(days=14)
        deadline=date(2026,12,15) if window=='original' else date(2027,3,15)
        decision_date=signal+timedelta(days=gate_days)
        integration_ok=decision_date+timedelta(days=lead)<=deadline
        ready=decision_date+timedelta(days=lead)
        start=date(2026,11,15) if window=='original' else date(2027,1,15)
        delay=.1*max(0,(ready-start).days)
        r=operational_decision(joint,slot=slot,reserve=reserve,integration_ok=integration_ok,
            approval_in_time=decision_date<=deadline,target_ready=integration_ok,delay_cost=delay)
        rows.append(dict(private_strength=strength,LV_date=str(launch),signal_date=str(signal),decision_date=str(decision_date),window=window,lead_days=lead,gate_days=gate_days,slot_probability=slot,reserve=reserve,integration_ok=integration_ok,delay_MUSD=delay,net_wait_gain_MUSD=r['net_wait_gain']))
csv_write(OUT/'operational_sensitivity.csv',rows)
(OUT/'audit_summary.json').write_text(json.dumps({'original_360_envelope':summary,'agreement_with_attached_envelope':True,'operational_scenarios':len(rows),'physics_controls':len(controls)},indent=2)+'\n')
print((OUT/'audit_summary.json').read_text())

report=Path('results/RUN_REPORT.md')
text=report.read_text()
marker='\n## Original independent-audit response'
text=text.split(marker)[0]
text+=marker+'\n\nMain figure: `structural_envelope.png` records 2,775 reallocate-in-all cells, 336 model-disagreement cells, and no wait-in-all cells across the specified 360 scenarios. The previously submitted numerical envelope is reproduced.\n\nExtensions: 432 operational scenarios and 12 separately varied physics/observation controls. The newer M* planning window spans January 15–March 15, 2027; the fixed reference above retains its earlier assumptions for regression checks. These should not be conflated.\n\nThe original independent review logged 42 passing tests, including pgmpy. That is a historical claim, not a current CI test count. An independently submitted adaptive quadrature checker is available at `independent_numeric_check.py`. See `docs/AUDIT_RESPONSE.md` for limits and corrections. No archived DOI is claimed.\n'
report.write_text(text)
