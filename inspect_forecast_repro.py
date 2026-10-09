"""Diagnose cross-run drift without overwriting the preflight forecast bytes."""
import difflib
import json
from pathlib import Path
from src.model import Scenario
from src.prospective import build_forecast

s=build_forecast(Scenario())
s["forecast_series_name"]="reference"
expected=Path("forecast/reference.json").read_text()
actual=json.dumps(s,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
print("Exact byte reproduction:",expected==actual)
if expected!=actual:
    differences=list(difflib.unified_diff(expected.splitlines(),actual.splitlines(),
                fromfile="published",tofile="recomputed",lineterm=""))
    print("\n".join(differences[:100]))
