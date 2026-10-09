"""Verify SHA256 of original forecast bytes and independently recompute all fields.

Last-bit floating deviations may appear on different runners; archived bytes
never change. Numerical comparisons have 1e-12 tolerance, not blind rounding.
"""
from hashlib import sha256
from math import isclose,isfinite
from pathlib import Path
import json
from src.model import Scenario
from src.prospective import build_forecast

FORECAST_SHA256={
    "reference":"fc9d0e290adef51459b86c8ad4a1a6ddc03ea087163e48da6e59f6d106f82d1f",
    "historical_all":"ab84b1e4f60657779413a315b2dca98cff4bfc20604daaa70001db5568fd7cd3",
    "jeffreys_reference":"97cd41ab8efe77fa7b17b7b6b3f20ab353523a66a06533e0e215ffab2e43c19e",
    "shared_shock":"1abb6b5d4eef66e1e03efe41b276222245571d4707527ed622979dc0051a029c",
    "unknown_revisions":"11888bbdd0e2dc7e4d570f05bb60e8f31bdd8abc6126d35ac91c1c0b1e25ec74"
}
CASES={
    "reference":Scenario(),
    "historical_all":Scenario(revision_pair=(1.,0.,0.,0.)),
    "jeffreys_reference":Scenario(prior="jeffreys"),
    "shared_shock":Scenario(rho=.25),
    "unknown_revisions":Scenario(revision_pair=(.25,.25,.25,.25))
}

def check_nested(stored,recreated,path="$"):
    if isinstance(stored,dict) and isinstance(recreated,dict):
        if stored.keys()!=recreated.keys(): raise AssertionError(f"Changed keys at {path}")
        for key in stored: check_nested(stored[key],recreated[key],f"{path}.{key}")
    elif isinstance(stored,list) and isinstance(recreated,(list,tuple)):
        if len(stored)!=len(recreated): raise AssertionError(f"Changed length at {path}")
        for i,(a,b) in enumerate(zip(stored,recreated)): check_nested(a,b,f"{path}[{i}]")
    elif type(stored) is bool or type(recreated) is bool:
        if stored is not recreated: raise AssertionError(f"Changed boolean at {path}")
    elif isinstance(stored,(int,float)) and isinstance(recreated,(int,float)):
        if not (isfinite(stored) and isfinite(recreated) and
                isclose(stored,recreated,rel_tol=1e-12,abs_tol=1e-12)):
            raise AssertionError(f"Changed value at {path}: {stored} vs {recreated}")
    elif type(stored) is not type(recreated) or stored!=recreated:
        raise AssertionError(f"Changed metadata at {path}: {stored!r} vs {recreated!r}")

def verify():
    for name,scenario in CASES.items():
        path=Path("forecast")/(name+".json")
        raw=path.read_bytes()
        if sha256(raw).hexdigest()!=FORECAST_SHA256[name]:
            raise AssertionError(f"Original frozen forecast bytes changed: {path}")
        expected=json.loads(raw)
        computed=build_forecast(scenario)
        computed["forecast_series_name"]=name
        check_nested(expected,computed)
        print(f"PASS {path}: SHA256 preserved and all recomputed values within 1e-12")
    return True

if __name__=="__main__":
    verify()
