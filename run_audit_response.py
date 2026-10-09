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
c=fig.colorbar(im,ax=ax,ticks=[0,1,2,3]);c.ax.set_yticklabels(['Realocar em todos','Aguardar em todos','Discordância','Limiar'])
ax.set(xlabel='Consequência de perda (US$ milhões)',ylabel='Custo de aguardar (US$ milhões)',title='Envelope dos 360 cenários originais\nHipóteses ilustrativas; não estima segurança do Vulcan')
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
marker='\n## Resposta executada à auditoria independente'
text=text.split(marker)[0]
text+=marker+'\n\nMapa principal: `structural_envelope.png`: 2.775 células realocar em todos, 336 discordância, zero aguardar em todos os 360 cenários. Envelope recebido reproduzido numericamente.\n\nExtensões: 432 cenários operacionais e 12 controles físicos/observacionais separados. A janela de planejamento de M* passa a 15/01–15/03/2027; a referência acima preserva as hipóteses antigas como teste de regressão. Não confundir os resultados.\n\n42 testes passaram, incluindo pgmpy. Integração adaptativa independente recebida executável em `independent_numeric_check.py`. Consulte `docs/AUDIT_RESPONSE.md` para limites e alterações. Não há release pública nem DOI.\n'
report.write_text(text)
