"""Report reference waiting threshold, sensitivity drivers, and structural regret."""
import csv, json
from pathlib import Path
from src.model import Scenario,joint_distribution,decision

def rows(path):
    with open(path,newline='') as f: return list(csv.DictReader(f))

ref=decision(joint_distribution(Scenario()),delay_cost=0)
threshold=ref['net_wait_gain']
control=rows('results/controls.csv')
groups={}
for r in control:
    k=r['parameter'];groups.setdefault(k,[]).append((r['value'],float(r['net_wait_gain_MUSD'])+10))
drivers=[]
for k,g in groups.items():
    values=[v for _,v in g]
    drivers.append(dict(parameter=k,range_threshold_MUSD=max(values)-min(values),
                        minimum_threshold_MUSD=min(values),maximum_threshold_MUSD=max(values),
                        values='; '.join(f'{x}: {v:.4f}' for x,v in g)))
drivers.sort(key=lambda x:x['range_threshold_MUSD'],reverse=True)
with open('results/threshold_drivers.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=drivers[0].keys());w.writeheader();w.writerows(drivers)
structural=rows('results/structural_sensitivity.csv')
structural_threshold=[float(r['net_wait_gain_MUSD'])+10 for r in structural]
result={'reference_delay_cost_threshold_MUSD':threshold,
        'reference_policy_at_D10':'realocate_now',
        'top_three_one_at_a_time_threshold_drivers':drivers[:3],
        '360_grid_threshold_min_MUSD':min(structural_threshold),
        '360_grid_threshold_max_MUSD':max(structural_threshold),
        '360_grid_wait_at_D10':sum(float(r['net_wait_gain_MUSD'])>0 for r in structural),
        '360_grid_reallocate_at_D10':sum(float(r['net_wait_gain_MUSD'])<=0 for r in structural),
        'worst_case_regret_of_reallocate_at_D10_MUSD':max(0,max(t-10 for t in structural_threshold)),
        'worst_case_regret_of_wait_at_D10_MUSD':max(0,max(10-t for t in structural_threshold)),
        'disclaimer':'Unweighted scenario grid; not an empirical uncertainty distribution or decision recommendation'}
Path('results/decision_brief.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
