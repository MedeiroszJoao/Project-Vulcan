# Prospective-style hold-out Monte Carlo simulation — NASA battery campaigns

**Protocol declared on 2026-10-09 before the code inspected the new target measurements.**
**Scientific status:** independent *offline* empirical stress test in physical battery experiments, **not** the rocket launch's physical risk validation, not a live preregistered NASA study, and not a real-time forecast. All datasets are historical public data, but these 11 additional cells are outside the earlier B0005/B0006/B0007/B0018 benchmark. Any improvements attempted after examining scores will require other untouched cells.

## Source and traceability
Primary download: [NASA Ames Prognostics Data Repository — Battery Data Set](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/). Raw ZIP: https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip, previously independently observed and SHA256-verified `82302a7db4fc1b34e0b6676326610438d43b816bdf11a69d1d012a464ef2f92e`. Stop if digest differs. The code reads raw MATLAB files, **not** a third-party derived CSV, and never writes original raw files into Git. Source references describe conditions of individual cohorts; cells may have different discharge cutoff thresholds, currents and temperatures. Raw capacity values under different discharge protocols are **not interchangeable measures of standardized cell health**.

## Predeclared measurement groups
1. **B0025–B0028** — approximately 24°C, pulsed 4A discharge; varying cutoff voltages.
2. **B0029–B0032** — approximately 43°C, pulsed discharge; different thermal conditions from first cohort.
3. **B0033, B0034, B0036** — additional protocols at approximately 24°C; B0036 may differ in discharge current. Do not pool them as if they were physically identical.

These cells were selected *from published metadata identifying test conditions*, **before looking at their discharge capacities or selecting results**. We explicitly include *every cell listed above*, and do not exclude cells with unfavorable errors.

## Strict retrospective chronological protocol

For every cell separately:
- Let n = number of recorded discharge cycles; fit to first `floor(0.60*n)`.
- Hold back *every later cycle* solely for scoring; no rolling correction, no fitting on held-out data.
- Fit three models using only initial data:
  - **Driftless random walk**, innovation bootstrap on mean-centered first differences; 4,000 seeded Monte Carlo future paths.
  - **OLS linear trend** with Gaussian/Student-t nominal predictive intervals; conditional Gaussian independent-regression error hypothesis.
  - **Linear trend + AR(1) residual**, stationary `phi` truncated to [-0.97,0.97] and Gaussian innovations fitted to residuals; 4,000 seeded Monte Carlo paths. This is a temporal-dependence hypothesis, not an asserted physical stochastic degradation law.
- Training period and number of future steps are retrospectively determined by total series length, making this an **offline historical test**, not real-time horizon planning.
- Compare MAE, RMSE, mean signed error, empirical 90% interval coverage and average interval width, grouped by the **number of actual cycles**. Within-battery cycles are dependent; 11 devices is the relevant independent-unit scale.
- Secondary **illustrative**, fixed 1.4Ah final-cycle event and its Brier score, averaged by device. Different end voltages limit interpretation of a common capacity cutoff.
- Fix RNG seed to 20261009, simulation count to 4,000 and all method choices *before examining targets*; do not rank/search models after reading the held-out observations.

## What would falsify the methodological benefit?
- The AR(1) model predicts future capacities no better than linear or random-walk benchmarks across cohorts.
- An AR(1) nominal 90% band exhibits undercoverage compared with the simple baselines; smooth-looking Monte Carlo visualizations do not guarantee trustworthy uncertainty.
- Different discharge regimens/temperature cause poor transferability even when within-sample fits look strong.
- Apparent gains disappear when one cohort or cell is omitted from qualitative interpretation.

## How to reproduce
```bash
python -m pip install -r requirements.txt
python research_nasa_monte_carlo.py --self-test
python research_nasa_monte_carlo.py
```
Output: `results/nasa_monte_carlo/report.json` plus physical-measurement-vs-simulated-capacity plots for representative *predeclared* cells (B0025/B0029/B0033/B0036), and a by-cohort score chart. GitHub Actions archives the outputs. The five original Vulcan LV-01 forecast JSON files are **not edited**.

## Mandatory post-hoc audit: anomalous initial-to-final trajectories and cohort domination

**This addendum was written after the hold-out measurements and scores were inspected. It is not outcome-blind, prospective, or a predeclared exclusion rule.** Preserve the original 11-device scores and report their limits, not a retroactively altered primary benchmark.

The three long-run cells dominate the aggregate at **237 / 349 = 67.91% of held-out cycle observations**, but their reported first-to-last *measured discharge capacities increase*, in tension with their naive description as typical monotonic battery aging curves:

| Device | First recorded discharge capacity (Ah) | Last recorded (Ah) | Observations / test cycles | Illustrative 1.4Ah final-event interpretation |
|---|---:|---:|---:|---|
| B0033 | 0.06843 | 1.31528 | 197 / 79 | Below threshold, despite increasing endpoint |
| B0034 | 0.74593 | 1.28026 | 197 / 79 | Below threshold, despite increasing endpoint |
| B0036 | 1.00198 | 1.55911 | 197 / 79 | Above threshold, despite increasing endpoint |

**Important epistemic caveat:** a first-to-last increase alone does **not** establish monotonic rise or identify its cause. We have not yet independently diagnosed whether initial partial-discharge cycles, startup transients, dataset interpretation, protocol differences, equipment initialization, discharge numbering, or another mechanism explains the increase. The original NASA notes say these cells were tested under different cutoff voltages and currents; that does *not* itself explain the observed 0.068Ah first measurement. The arrays, raw acquisition timestamps and discharge-voltage/current profiles need inspection before asserting "non-aging data" as a physical fact.

The simple interpretation `P(capacity<1.4Ah)` as end-of-life risk is **not justified** for these experiments under these conditions. The probability is only an illustrative threshold event in this dataset, not a battery-health classification or a rocket risk surrogate.

Compare *separately* with B0025–B0032 (8 short-series cells, **112** held-out cycles), which have much smaller initial-to-final capacity changes. Those eight cells yield MAE **0.028608 Ah** (driftless RW), **0.018080 Ah** (linear) and **0.018169 Ah** (AR1). The whole 11-cell micro-average instead yields **0.059094 / 0.077134 / 0.076651 Ah**, respectively. This is a post-hoc subgroup analysis, not a replacement for the original report. Different windows and protocols complicate pooling.

AR(1) uncertainty simulation fixes fitted trend coefficients, residual correlation `phi` and noise `sigma` at point estimates; it omits parameter-estimation uncertainty. The observed undercoverage should be attributed to **this implementation plus its model mismatch**, not asserted as an inevitable property of AR(1) forecasting. The driftless random-walk simulation resamples centered training increments into paths and produces extremely wide nominal 90% bands (pooled mean **1.6408 Ah**, about 2.25 Ah in these three long-run cells). Observed coverage without interval sharpness and an interval/CRPS score is not an engineering validation metric by itself.

This research is **post-hoc relative to PR #3** (its benchmark had already been observed). It did use additional previously untested device identifiers and freeze-like rules *within the subsequent experiment*; this does not make the work a registered independent prospective trial. Its final-cycle event Brier uses just **one binary event per device** (11), with heterogeneous cutoff protocols, so it cannot establish reliable relative event calibration.

**Follow-up before making further physical claims:** examine original per-cycle discharge capacity, timestamps, cutoff voltages and load current of B0033, B0034 and B0036; investigate measurement-ordering and partial-discharge mechanisms, and designate future new cells as untouched holdouts for any new model. Do not discard the three from this already-published evaluation to artificially improve results.

Original primary source: [NASA PCoE Battery Dataset](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/); published descriptive [operating-protocol comparison](https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2022.1032660/full).

## Explicit interpretational boundaries
NASA battery data assess transferable *uncertainty forecasting and validation methodology*, not the actual GEM 63XL nozzle behavior, a launch vehicle's safety, or ULA decisions. The event threshold below 1.4Ah is illustrative and cannot be ported to rockets. These methods are standard predictive-model tools and are **not claimed as novel theory**. A real engineering-risk product would require mechanism-specific data, credible safety constraints, and external domain review.
