"""Precompute prospective scores for EACH possible observation; not real flight result."""
import csv,json
from pathlib import Path
from src.prospective import categorical_score
forecast=json.loads(Path('forecast/reference.json').read_text())
rows=[]
for i,y in enumerate(forecast['report_signal_categories']):
    s=categorical_score(forecast['public_report_signal_pmf'],i)
    rows.append({'hypothetical_observation_ONLY_NOT_ACTUAL':y,
                 'probability_preflight':forecast['public_report_signal_pmf'][i],
                 **s})
with open('results/hypothetical_score_lookup.csv','w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
print('WROTE score lookup for 4 hypothetical outcomes (NOT flight result)')
