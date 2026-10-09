# Post-hoc Bayesian-decision transfer benchmark audit (2026-10-09)

**Status: EX-POST METHOD AUDIT.** This file was written **after** PR #3 and PR #4's held-out measurements were scored. It is not a registered outcome-blind model improvement or a future generalization result. The rocket LV-01 public forecast files and protocol remain untouched.

## Traceable real-data calculations and logs

- PR #3 final SHA: `5baa0edd043603d5c9ba5fa83cd87dfe5daaea72`; [real-data CI run 37994363590](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37994363590), artifact `nasa-battery-external-benchmark` with original `report.json` and four cell plots, seven tests successful.
- Original NASA-source independent capacity check: [run 37994245909](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37994245909) on intermediate commit `c4cce156b7e7aa4d0ca1cd957dfe7e9c63088c9b`: all **636/636** discharge-capacity values match the source MATLAB files exactly; this only verifies that measured column, not full metadata.
- PR #4 final SHA: `7f71302063582d7888f28b371004fad40e79d106`; [Monte Carlo CI run 37995095971](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37995095971), original `report.json`, plots and seven successful tests.
- [Main baseline CI for the PR #4 commit](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37995096041): 42 baseline tests and five original forecast SHA256 checks succeeded. Another run on this same SHA can fail from strict float serialization; see PR #2's integrity fix.
- Original PR-specific CI job logs were exported on [audit run 38000113160](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/38000113160), artifact name `vulcan-external-audit-original-ci-job-logs`.

## PR #3, four physical cells and 257 correlated held-out cycles

| Cell | Random walk MAE (Ah) | Linear MAE (Ah) | Linear nominal 90% coverage |
|---|---:|---:|---:|
| B0005 | 0.11191 | 0.02271 | 98.5% |
| B0006 | 0.12504 | 0.13513 | 16.2% |
| B0007 | 0.08896 | 0.02763 | 73.5% |
| B0018 | 0.05661 | 0.05115 | 50.9% |

Overall linear coverage **60.31%** despite nominal 90%; no independent-systems calibration conclusion is supportable from only four cells.

## PR #4, eleven physical cells and 349 correlated cycles

| Method | MAE cycle weighted (Ah) | MAE equally weighted across 11 cells (Ah) | Nominal 90% coverage | Mean interval width (Ah) |
|---|---:|---:|---:|---:|
| Driftless random walk | 0.059094 | 0.039801 | 96.56% | 1.64077 |
| Linear Student-t | 0.077134 | 0.041339 | 94.56% | 0.35350 |
| Linear trend + AR(1) Gaussian Monte Carlo | 0.076651 | 0.041191 | 84.81% | 0.20063 |

The **three** long-series cells B0033/34/36 contribute **237/349=67.91%** of held-out cycles. On the other **eight short-series cells, 112 cycles**, linear (MAE 0.018080 Ah) and AR(1) (0.018169 Ah) beat random walk (0.028608 Ah). Therefore neither overall micro-average nor macro-average licenses universal superiority.

An ex-post **device-bootstrap diagnostic** for the equal-cell paired difference (linear minus RW MAE, a positive value favors RW) gives estimated difference **+0.001538 Ah** and 50,000-resample percentile interval **[-0.010716,+0.017018] Ah** with RNG seed 20261009. It straddles zero. This is *descriptive, post-hoc, and lacks valid population-generalization guarantees*: devices may be correlated within campaigns, cohorts and discharge protocols are nonexchangeable, and just 11 devices are represented.

## What the models do and do not prove

1. **AR(1):** The implementation estimates linear coefficients, AR(1) phi and noise sigma, then holds them fixed in the Monte Carlo rollout. Estimated-parameter uncertainty, drift in physical regimes and model discrepancy are omitted. The observed 84.81% coverage is about **this plug-in implementation**, not an impossibility theorem for AR(1).
2. **Random walk:** Centered training increments are resampled into a driftless random walk. Spreading interval width with future horizon is a modeling assumption; its apparently high coverage (96.56%) is not necessarily decision-informative at **1.64 Ah mean interval width**.
3. **Brier score:** The final-cycle capacity event threshold 1.4Ah yields **one Bernoulli outcome per physical cell**; with only 11 independent-unit candidates and different discharge cutoffs it does not rank robust probability models.
4. **Correct next comparison:** A **proper interval score** (such as Winkler) or CRPS assessed on *new* held-out devices/flight cases, with explicit costs, is more meaningful than raw interval coverage or artificially wide intervals. Re-scoring the already-seen outcomes is descriptive only.
5. **NASA data cannot validate Vulcan rocket propulsion CPTs.** Transferable statistical forecasting technique is the only thing being tested. No claim of physical booster failure risk, launch certification, or operational recommendation.

**No raw NASA .mat files are redistributed here; verified CI runs have the source archive checksums.**
