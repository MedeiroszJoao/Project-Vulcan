"""Release candidate reproducibility sanity check (NOT a public time stamp)."""
import csv, json, math, hashlib
from pathlib import Path
from src.model import Scenario,joint_distribution,decision
from src.prospective import build_forecast
root=Path('.')
assert (root/'forecast/reference.json').is_file()
saved=json.loads((root/'forecast/reference.json').read_text())
current=build_forecast(Scenario())
for k in ['public_report_signal_pmf','latent_physical_anomaly_count_pmf',
          'hypothetical_disclosed_count_pmf']:
    assert len(saved[k])==len(current[k]),k
    assert all(math.isclose(a,b,abs_tol=1e-12,rel_tol=1e-12) for a,b in zip(saved[k],current[k])),k
assert saved['status']=='freeze_candidate_UNPUBLISHED'
r=decision(joint_distribution(Scenario()),delay_cost=10)
assert abs(r['net_wait_gain']-(-8.72099915780434)) < 1e-8
with (root/'results/structural_sensitivity.csv').open() as f:
    rows=list(csv.DictReader(f))
assert len(rows)==360
assert sum(x['preferred']=='wait' for x in rows)==1
print('PASS forecast reference PMFs match recomputation within 1e-12')
print('PASS reference decision and 360 structural scenario rows')
print('SHA256(forecast/reference.json):',hashlib.sha256((root/'forecast/reference.json').read_bytes()).hexdigest())
print('NOTE: no repository, released tag, DOI or public timestamp established by this command.')
