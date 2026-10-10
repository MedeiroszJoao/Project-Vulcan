"""Generate hypothetical comparator scores; never records an observed flight."""
import json
from pathlib import Path
from src.prospective import categorical_score


def build():
    data=json.loads(Path("baselines/public_report.json").read_text())
    return {"status":"HYPOTHETICAL_OUTCOMES_ONLY_NOT_OBSERVED", "scores":{
        name:[{"outcome":y, **categorical_score(p,i)} for i,y in enumerate(data["categories"])]
        for name,p in data["probabilities"].items()}}


if __name__ == "__main__":
    Path("results/baseline_score_lookup.json").write_text(json.dumps(build(),indent=2,allow_nan=False)+"\n")
    print("WROTE hypothetical scores for all three baselines; no observed outcome")
