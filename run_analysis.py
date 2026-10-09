"""Reproduce all illustrative results. Run from repository root."""
from pathlib import Path
from dataclasses import asdict,replace
import csv,json,itertools,platform
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from src.model import *

OUT=Path('results'); OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'figure.facecolor':'#f6f8fc','axes.facecolor':'#ffffff'})

def csv_write(path,rows):
    with open(path,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    base=Scenario(); j=joint_distribution(base)
    (OUT/'reference_joint.json').write_text(json.dumps(j.tolist(),indent=2)+'\n')
    r=decision(j,delay_cost=10)
    Path('data/reference_scenario.json').write_text(json.dumps(asdict(base),indent=2)+'\n')
    (OUT/'reference.json').write_text(json.dumps(r,indent=2)+'\n')
    policies=[]
    for prior in ('uniform','jeffreys'):
        d=decision(joint_distribution(replace(base,prior=prior)),delay_cost=10)
        for i,y in enumerate(Y_NAMES):
            policies.append(dict(prior=prior,observation=y,probability=d['y_probability'][i],
              conditional_target_expected_loss_MUSD=d['conditional_target_loss'][i],
              action_if_approved=d['policy_if_approved'][i],action_if_denied='alternative'))
    csv_write(OUT/'policy.csv',policies)

    losses=np.linspace(250,2000,61); delays=np.linspace(0,100,51)
    gains=[]; rows=[]
    for prior in ('uniform','jeffreys'):
        jj=joint_distribution(replace(base,prior=prior))
        g=np.array([[decision(jj,loss=L,delay_cost=D)['net_wait_gain'] for L in losses] for D in delays])
        gains.append(g)
        for di,D in enumerate(delays):
            for li,L in enumerate(losses): rows.append(dict(prior=prior,delay_MUSD=D,loss_MUSD=L,net_wait_gain_MUSD=g[di,li]))
    csv_write(OUT/'decision_map.csv',rows)
    gains=np.array(gains); epsilon=.01 # numerical/economic indifference band USD 10,000
    robust=np.where(np.min(gains,axis=0)>epsilon,1,
            np.where(np.max(gains,axis=0)<-epsilon,0,2))
    fig,axes=plt.subplots(1,2,figsize=(13,5.4),layout='constrained')
    im=axes[0].pcolormesh(losses,delays,gains[0],cmap='RdBu',shading='auto',vmin=-100,vmax=100)
    fig.colorbar(im,ax=axes[0],label='Net benefit of waiting (USD million)')
    axes[0].set_title('Net waiting benefit · uniform prior')
    im2=axes[1].pcolormesh(losses,delays,robust,cmap=ListedColormap(['#355c7d','#2a9d8f','#e9b44c']),vmin=-.5,vmax=2.5,shading='auto')
    cb=fig.colorbar(im2,ax=axes[1],ticks=[0,1,2]);cb.ax.set_yticklabels(['Reallocate','Wait','Undetermined'])
    axes[1].set_title('Agreement across uniform / Jeffreys priors')
    for ax in axes: ax.set(xlabel='Loss consequence (USD million)',ylabel='Incremental waiting cost (USD million)')
    fig.suptitle('ILLUSTRATIVE SCENARIOS — not a Vulcan safety estimate',fontweight='bold')
    fig.savefig(OUT/'decision_map.png',dpi=160);plt.close(fig)

    values=np.linspace(0,1,11); ev=np.zeros((11,11)); evrows=[]
    for i,q in enumerate(values):
        for k,rel in enumerate(values):
            sc=replace(base,theta=((1-q)/2,q,(1-q)/2),relevance=float(rel))
            rr=decision(joint_distribution(sc))
            ev[i,k]=rr['evsi']; evrows.append(dict(effective_regime_weight=q,relevance=rel,evsi_MUSD=rr['evsi']))
    csv_write(OUT/'evsi_surface.csv',evrows)
    fig,ax=plt.subplots(figsize=(8,5.5),layout='constrained')
    im=ax.pcolormesh(values,values,ev,cmap='viridis',shading='auto')
    fig.colorbar(im,ax=ax,label='Pure EVSI (USD million)')
    ax.set(xlabel='Same-revision transfer relevance',ylabel='Scenario weight: effective correction',
           title='Pure EVSI · fixed counterfactual action set\nHypothetical CPTs; no waiting cost or approval gate')
    fig.savefig(OUT/'evsi_surface.png',dpi=160);plt.close(fig)

    # Structural scenarios are not assigned probabilities or averaged into a result.
    sensitivity=[]
    revisions={'HH':(1,0,0,0),'HM':(0,1,0,0),'MH':(0,0,1,0),'MM':(0,0,0,1),'unknown':(.25,)*4}
    theta_grid=[(.6,.2,.2),(.2,.6,.2),(.1,.8,.1)]
    for prior,theta,rel,rho,rev,detect in itertools.product(
          ('uniform','jeffreys'),theta_grid,(0,.5,1),(0,.25),revisions,(.7,1)):
        sc=replace(base,prior=prior,theta=theta,relevance=rel,rho=rho,
                   revision_pair=revisions[rev],history_detection=detect)
        jj=joint_distribution(sc)
        rr=decision(jj,delay_cost=10)
        sensitivity.append(dict(prior=prior,theta=str(theta),relevance=rel,rho=rho,
            revisions=rev,history_detection=detect,evsi_MUSD=rr['evsi'],
            net_wait_gain_MUSD=rr['net_wait_gain'],preferred=rr['preferred']))
    csv_write(OUT/'structural_sensitivity.csv',sensitivity)
    heritage=[]
    for prior,w in itertools.product(('uniform','jeffreys'),(0,.25,.5)):
        rr=decision(joint_distribution(replace(base,prior=prior,heritage_weight=w)),delay_cost=10)
        heritage.append(dict(prior=prior,heritage_weight=w,evsi_MUSD=rr['evsi'],net_wait_gain_MUSD=rr['net_wait_gain']))
    csv_write(OUT/'heritage_sensitivity.csv',heritage)
    # Additional controls: severity, correction efficacy, observability, authorization.
    controls=[]
    for field,grid in {'effective_multiplier':(.05,.1,.3),'ineffective_increment':(0,.05,.15),
                       'target_severe':(.1,.25,.5),'disclosure':(.5,.9,1),'detection':(.5,.9,1)}.items():
        for value in grid:
            rr=decision(joint_distribution(replace(base,**{field:value})),delay_cost=10)
            controls.append(dict(parameter=field,value=str(value),evsi_MUSD=rr['evsi'],net_wait_gain_MUSD=rr['net_wait_gain']))
    for gate in [(0,0,0,0),(.5,.1,0,.1),(.9,.3,.05,.4),(1,1,1,1)]:
        rr=decision(j,delay_cost=10,approval=gate)
        controls.append(dict(parameter='approval',value=str(gate),evsi_MUSD=rr['evsi'],net_wait_gain_MUSD=rr['net_wait_gain']))
    for key,grid in {'alternative_cost':(10,30,100),'alternative_loss':(.001,.005,.02),
                     'alternative_degraded':(.001,.003,.01),'later_alternative_cost':(0,5,20),
                     'degraded_fraction':(.1,.25,.5)}.items():
        for value in grid:
            rr=decision(j,delay_cost=10,**{key:value})
            controls.append(dict(parameter=key,value=str(value),evsi_MUSD=rr['evsi'],net_wait_gain_MUSD=rr['net_wait_gain']))
    from datetime import datetime,timedelta
    calendar=[]
    for days,daily in itertools.product((7,45,715),(0,.1,.5)):
        date=datetime(2026,11,15)+timedelta(days=days)
        penalty=20 if date>=datetime(2026,12,16) else 0
        cost=days*daily+penalty
        rr=decision(j,delay_cost=cost)
        calendar.append(dict(additional_days=days,date_UTC=date.date().isoformat(),daily_MUSD=daily,
                             window_penalty_MUSD=penalty,delay_MUSD=cost,net_wait_gain_MUSD=rr['net_wait_gain']))
    csv_write(OUT/'calendar_sensitivity.csv',calendar)
    csv_write(OUT/'controls.csv',controls)
    (OUT/'RUN_REPORT.md').write_text(f'''# Resultado executado — laboratório de decisão Vulcan

Exercício independente com dados públicos. Nenhuma CPT de engenharia abaixo é uma estimativa validada do Vulcan.
Estado: implementação executada; não é registro público congelado.

## Cenário ilustrativo de referência
M*: 3.000 kg, comunicações resilientes, GEO direto, janela 15/11–15/12/2026.
Revisões MM são hipótese, não conhecimento do hardware instalado.
Prior uniforme; sem Atlas; 6 boosters no LV e 4 no alvo; P(Θ)=(.2,.6,.2).
Consequência de perda US$ 1.000 milhões; atraso incremental US$ 10 milhões.

| Métrica | US$ milhões |
|---|---:|
| EVSI puro, conjunto de ações fixo contrafactual | {r['evsi']:.6f} |
| Custo esperado de realocar agora | {r['realocate_now_cost']:.6f} |
| Custo esperado de aguardar e decidir com autorização | {r['wait_cost']:.6f} |
| Ganho líquido de aguardar | {r['net_wait_gain']:.6f} |

Ação preferida neste cenário: **{r['preferred']}**. Não extrapolar para recomendação operacional.

## Arquivos
- decision_map.png / decision_map.csv: benefício de esperar e discordância entre dois priors, demais premissas fixas.
- evsi_surface.png / evsi_surface.csv: grade de pesos de regime e relevância; ação fixa para EVSI.
- policy.csv: quatro observações, condicionadas a autorização concedida ou negada.
- structural_sensitivity.csv: {len(sensitivity)} cenários estruturais, sem média entre cenários.
- heritage_sensitivity.csv: análise secundária sob observabilidade perfeita da herança.
- controls.csv: eficácias, severidade, observação e política de autorização.

Uma região estável entre dois priors não é robustez universal. Custos, CPTs, transferência e governança
continuam hipóteses. O mesmo número de anomalias pode produzir consequências muito diferentes.
O ensaio pgmpy valida a inferência a partir das CPTs emitidas, não valida a física dessas CPTs.
''',encoding='utf-8')
    print(json.dumps({'reference':r,'structural_scenarios':len(sensitivity)},indent=2))

if __name__=='__main__': main()
