# Two independent checks: forecast integrity and numerical reproduction

**Finding on 2026-10-09:** multiple public GitHub Actions runs on the SAME source commit sometimes reproduced the forecast JSON numerically, but differed in the last binary floating-point digits (~10^-17). The pre-existing `build_forecast.py --check` demands exact re-rendered UTF-8 bytes and therefore intermittently failed even though the archived files had not changed. See `inspect_forecast_repro.py` and recorded Actions logs.

**Fix:** `verify_frozen_forecasts.py` executes two separate, stronger-in-combination invariants:

1. **No changes to primary forecast:** compare exact SHA-256 digests for each of the five checked-in original `forecast/*.json` files against original predeclared SHA-256 values. This is a *zero-tolerance* byte-integrity check.
2. **Scientific computation reproducibility:** recalculate *every* field of each forecast from its specified original `Scenario`, compare JSON structure, text, booleans and shapes exactly, and compare numeric values within 1e-12 relative and absolute tolerance. This does not use the observed outcome or rewrite any frozen bytes.

In a separate test module, deliberate 1e-5 probability changes and edited metadata are rejected. Numeric last-digit drift is accepted. The original byte-strict command still exists as an optional platform-specific diagnostic, but the new checker is used for cross-platform CI.

This change does **not** backdate or modify any LV-01 probability, metadata, dates or original forecast SHA-256. It corrects the verification policy and is presented as a separate draft research PR, **not** a release or DOI.
