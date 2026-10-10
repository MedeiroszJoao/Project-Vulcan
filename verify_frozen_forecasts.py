"""Verify archived forecast integrity and independently check numerical consistency.

This separates two different requirements:
- Stored, historically recorded bytes must match their exact SHA-256 digests.
- Recomputed floating-point values may differ at machine precision, but
  parameters, keys, categories, and substantive numbers must not change.

This module never rewrites source artifacts.
"""
from __future__ import annotations

import json
from hashlib import sha256
from math import isclose, isfinite
from pathlib import Path

from src.model import Scenario
from src.prospective import build_forecast

ROOT = Path(__file__).resolve().parent

# Digests belong to the original five forecast objects, not regenerated files.
ARCHIVED_SHA256 = {
    "reference": "fc9d0e290adef51459b86c8ad4a1a6ddc03ea087163e48da6e59f6d106f82d1f",
    "historical_all": "ab84b1e4f60657779413a315b2dca98cff4bfc20604daaa70001db5568fd7cd3",
    "jeffreys_reference": "97cd41ab8efe77fa7b17b7b6b3f20ab353523a66a06533e0e215ffab2e43c19e",
    "shared_shock": "1abb6b5d4eef66e1e03efe41b276222245571d4707527ed622979dc0051a029c",
    "unknown_revisions": "11888bbdd0e2dc7e4d570f05bb60e8f31bdd8abc6126d35ac91c1c0b1e25ec74",
}

SCENARIOS = {
    "reference": Scenario(),
    "historical_all": Scenario(revision_pair=(1.0, 0.0, 0.0, 0.0)),
    "jeffreys_reference": Scenario(prior="jeffreys"),
    "shared_shock": Scenario(rho=0.25),
    "unknown_revisions": Scenario(revision_pair=(0.25, 0.25, 0.25, 0.25)),
}


def compare_nested(stored, computed, path="$"):
    """Recursively compare structure exactly and finite floats to 1e-12."""
    if isinstance(stored, dict) and isinstance(computed, dict):
        if stored.keys() != computed.keys():
            raise AssertionError(f"Different object keys at {path}")
        for key in stored:
            compare_nested(stored[key], computed[key], f"{path}.{key}")
    elif isinstance(stored, list) and isinstance(computed, (list, tuple)):
        if len(stored) != len(computed):
            raise AssertionError(f"Different array lengths at {path}")
        for index, (expected, actual) in enumerate(zip(stored, computed)):
            compare_nested(expected, actual, f"{path}[{index}]")
    elif isinstance(stored, bool) or isinstance(computed, bool):
        if stored is not computed:
            raise AssertionError(f"Different boolean at {path}")
    elif isinstance(stored, (int, float)) and isinstance(computed, (int, float)):
        if not (isfinite(stored) and isfinite(computed)):
            raise AssertionError(f"Non-finite number at {path}")
        if not isclose(stored, computed, rel_tol=1e-12, abs_tol=1e-12):
            raise AssertionError(f"Different numeric result at {path}: {stored} vs {computed}")
    elif type(stored) is not type(computed) or stored != computed:
        raise AssertionError(f"Different metadata at {path}: {stored!r} vs {computed!r}")


def verify():
    """Return True if all original archived bytes and rerun values match."""
    for name, scenario in SCENARIOS.items():
        path = ROOT / "forecast" / f"{name}.json"
        raw = path.read_bytes()
        actual_hash = sha256(raw).hexdigest()
        if actual_hash != ARCHIVED_SHA256[name]:
            raise AssertionError(
                f"Forecast archive integrity failure: {path.relative_to(ROOT)} "
                f"({actual_hash} != {ARCHIVED_SHA256[name]})"
            )
        stored = json.loads(raw)
        recomputed = build_forecast(scenario)
        recomputed["forecast_series_name"] = name
        compare_nested(stored, recomputed)
        print(f"PASS forecast/{name}.json: SHA-256 and independent recomputation")
    return True


if __name__ == "__main__":
    verify()
