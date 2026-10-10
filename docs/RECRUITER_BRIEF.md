# Project Vulcan — Technical portfolio note

**Domains:** probabilistic modeling · model validation · scientific Python · research software · decision analysis

## Problem and implementation

Project Vulcan investigates whether the information obtained from a further observed launch could change a hypothetical mission procurement decision. A Bayesian model represents reported component anomalies, observation gaps and assumptions about hardware revisions; conditional probability tables represent illustrative mission outcomes, and value-of-information calculations compare waiting with immediate reallocation.

Code: Python 3.12, NumPy, SciPy, pgmpy, Matplotlib, unit tests and GitHub Actions. Outputs: decision maps, conditional scenarios, forecast probabilities, model diagnostics, adversarial sensitivity analyses and a separate interactive Three.js educational viewer.

## What an interviewer can inspect

1. `src/model.py` and `src/prospective.py`: probabilistic inference, scenario conditioning and separation of latent events from public reporting.
2. `src/operations.py`: explicit feasibility and decision costs.
3. `tests/`, `verify_frozen_forecasts.py` and the Actions workflow: regression checks, exact SHA-256 artifact integrity and numerical tolerance.
4. [Draft PR #2](https://github.com/MedeiroszJoao/Project-Vulcan/pull/2): structural non-identifiability witnesses and conditional decision bounds.
5. [Draft PRs #3–4](https://github.com/MedeiroszJoao/Project-Vulcan/pulls): held-out laboratory prediction benchmarks, calibration failures and critical examination of aggregation.

## Constraints and appropriate claims

This project illustrates scientific software engineering and uncertainty reasoning. It does **not** establish a calibrated rocket failure rate, implement actual flight control or prove that a particular rocket is safe. The NASA experiment uses real measured *battery* capacity data, not turbofan or rocket telemetry. The interactive vehicle geometry is explanatory, not engineering CAD.

A technical review should evaluate transparent decisions, tests, verifiable numerical work, data/assumption boundaries and the maintainer's ability to explain or defend the code—not aesthetics or a claim of affiliation with a manufacturer.
