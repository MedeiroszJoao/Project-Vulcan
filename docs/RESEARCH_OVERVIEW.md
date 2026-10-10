# Research overview

## The decision problem

A hypothetical satellite operator has two options: procure a backup launcher now, or wait to observe a public report about another Vulcan mission and then act. The model quantifies an information benefit together with waiting costs, availability, approval and loss consequences. It intentionally does not claim access to private launch telemetry, certification decisions or contract terms.

The baseline study models historical publicly reported booster anomalies using uncertain rates, revision hypotheses, partial reporting and a synthetic dependence stress parameter. Mission-consequence conditional-probability tables (CPTs) and economic valuations are scenario assumptions, not estimates recovered from booster reports.

## Three distinct research tracks

| Track | Repository location | Status | Principal result |
| --- | --- | --- | --- |
| Decision and prospective protocol | `main`, `src/`, `forecast/`, `docs/FORECAST_PROTOCOL.md` | Implemented baseline; no verified archival DOI | Conditional decision and public-report forecast |
| Identifiability and decision bounds | [PR #2](https://github.com/MedeiroszJoao/Project-Vulcan/pull/2) | Draft, unmerged | Two consequence worlds with identical historical and public-report likelihoods change the preferred action |
| Experimental forecasting methods | [PR #3](https://github.com/MedeiroszJoao/Project-Vulcan/pull/3), [PR #4](https://github.com/MedeiroszJoao/Project-Vulcan/pull/4) | Draft, unmerged | Point accuracy, interval coverage and aggregation rankings can disagree |
| External audit adjudication | [PR #5](https://github.com/MedeiroszJoao/Project-Vulcan/pull/5) | Draft, unmerged | Independent numerical/CI evidence, diagnostic corrections and provenance scope |

These tracks are **not** merged into one validated physical model. Benchmarks of battery-capacity forecasting evaluate statistical methods on those batteries, not GEM 63XL or Vulcan mission safety.

## Quantitative interpretation

For a hypothetical waiting cost of $10 million, the fixed-slot reference calculates an immediate-reallocation expected cost of $35.750 million and an expected wait cost of $44.471 million. This $8.721 million negative gain to waiting is **not** a universal result: alternative consequence assumptions can reverse its sign. The reference also differs from later operational sensitivity scenarios with explicit reservation, launch windows and integration lead times.

In PR #2, changing the future-mission consequence CPT while keeping the historical likelihood and LV public-report distribution fixed produces exact model-specific bounds on the benefit of waiting. The result is **non-identification under specified structural restrictions**; it neither estimates actual aerospace failure probabilities nor proves no useful future engineering data could identify them.

PR #3 assesses four NASA lithium-ion battery cells (257 chronological held-out observations). A linear model improves aggregate point error but achieves 60.3% empirical coverage for nominal 90% intervals. PR #4 extends the stress test to 11 different cells and heterogeneous protocols. The 349 held-out cycles are correlated within only 11 experimental systems; three long-series devices account for 237 cycles. Do not treat 349 cycles as independent devices or infer cross-population calibration.

## Prospective evidence and research chronology

Original `forecast/*.json` bytes and protocol definitions are preserved; numerical re-derivation tolerates machine-level floating-point differences, while committed hashes remain exact. The repository contains GitHub-side timestamps and successful CI records, but those do not establish a Zenodo archive, scientific peer review or validated flight-safety prediction. External release validation remains separate.

New analyses prompted by the observed NASA outcomes are explicitly *post hoc* and need fresh, untouched cohorts before being described as new out-of-sample generalization tests.

## Read further

- [Scientific limitations](SCIENTIFIC_LIMITATIONS.md)
- [Software architecture](SOFTWARE_ARCHITECTURE.md)
- [Reproducibility and CI](REPRODUCIBILITY.md)
- [Data provenance](DATA_PROVENANCE.md)
- [Original specification](../SPEC.md) and [technical note](TECHNICAL_NOTE.md), retained unchanged as archival research history
