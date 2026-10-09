"""Separate scientific extension; does not edit original prospective forecasts."""
import json
from pathlib import Path
from src.identifiability import assess_worlds, exact_simplex_bounds

out=Path("results/scientific_upgrade")
out.mkdir(parents=True,exist_ok=True)
report=assess_worlds()
report["full_simplex_structural_bounds"]=exact_simplex_bounds()
p=out/"identifiability_witness.json"
p.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"output":str(p),
                  "decision_changes_sign":report["decision_changes_sign"],
                  "bounds":report["full_simplex_structural_bounds"]},indent=2))
