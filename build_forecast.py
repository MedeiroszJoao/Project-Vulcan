"""Create/check deterministic candidate without ever claiming public registration."""
import argparse
import json
from pathlib import Path
from dataclasses import replace
from src.model import Scenario
from src.prospective import build_forecast

def dump(data): return (json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='fail if files differ instead of overwriting')
    args=ap.parse_args()
    root=Path('forecast');root.mkdir(exist_ok=True)
    candidates={
      'reference':Scenario(),
      'unknown_revisions':Scenario(revision_pair=(.25,.25,.25,.25)),
      'historical_all':Scenario(revision_pair=(1.,0.,0.,0.)),
      'jeffreys_reference':Scenario(prior='jeffreys'),
      'shared_shock':Scenario(rho=.25),
    }
    for name,s in candidates.items():
        data=build_forecast(s)
        data['forecast_series_name']=name
        p=root/(name+'.json')
        output=dump(data)
        if args.check:
            if not p.is_file() or p.read_bytes()!=output:
                raise SystemExit(f'PRE-FREEZE forecast changed/missing: {p}')
            print(f'CHECK OK {p}')
        else:
            p.write_bytes(output);print(f'WROTE {p}')
