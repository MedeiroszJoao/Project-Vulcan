# Project Vulcan — Reproduced Decision Analysis

Independent public-data decision-analysis exercise. The engineering consequence
CPTs below are **illustrative assumptions**, not validated Vulcan reliability estimates.
Status: reference model reproduced; public forecast registration and independent
scientific review must be verified separately.

## Reference counterfactual

M*: hypothetical 3,000 kg communications payload, direct GEO delivery, original
November 15–December 15, 2026 scenario window. This is the historical baseline,
**not** the later January–March 2027 operational planning sensitivity.
Assumed MM hardware revisions are not confirmed manufacturer configurations.
Uniform prior; no quantitative Atlas heritage; six SRBs on the observed LV mission
and four SRBs on target M*; regime weights P(Θ) = (0.2, 0.6, 0.2).
Hypothetical mission loss: USD 1,000 million; waiting cost: USD 10 million.

| Metric | USD million |
| --- | ---: |
| Pure EVSI, fixed counterfactual action set | 3.989851 |
| Expected cost, reallocate immediately | 35.750000 |
| Expected cost, wait for report and approval | 44.470999 |
| Net gain from waiting | -8.720999 |

Conditional preferred action: **realocate_now**.
This is **not** an actual launch or procurement recommendation.

## Generated outputs

- `decision_map.png` / `decision_map.csv`: net benefit and agreement under two priors, with other assumptions fixed.
- `evsi_surface.png` / `evsi_surface.csv`: assumed correction-regime weight and relevance in a fixed action set.
- `policy.csv`: public-signal categories and hypothetical approval-dependent actions.
- `structural_sensitivity.csv`: 360 scenarios; no probabilistic aggregation over the grid.
- `heritage_sensitivity.csv`: separate, highly conditional heritage control.
- `controls.csv`: technical severity, correction effectiveness, observability and approval controls.

Agreement between two priors is not universal robustness. Loss CPTs, calendar
constraints, model transfer and governance are hypothetical. The same reported
anomaly count can imply different consequences. The pgmpy consistency test
checks inference over the supplied CPTs, **not** the underlying aerospace physics.

## Original independent-audit response

Main figure: `structural_envelope.png` records 2,775 reallocate-in-all cells, 336 model-disagreement cells, and no wait-in-all cells across the specified 360 scenarios. The previously submitted numerical envelope is reproduced.

Extensions: 432 operational scenarios and 12 separately varied physics/observation controls. The newer M* planning window spans January 15–March 15, 2027; the fixed reference above retains its earlier assumptions for regression checks. These should not be conflated.

The original independent review logged 42 passing tests, including pgmpy. That is a historical claim, not a current CI test count. An independently submitted adaptive quadrature checker is available at `independent_numeric_check.py`. See `docs/AUDIT_RESPONSE.md` for limits and corrections. No archived DOI is claimed.
