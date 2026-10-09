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

## Explicit interpretational boundaries
NASA battery data assess transferable *uncertainty forecasting and validation methodology*, not the actual GEM 63XL nozzle behavior, a launch vehicle's safety, or ULA decisions. The event threshold below 1.4Ah is illustrative and cannot be ported to rockets. These methods are standard predictive-model tools and are **not claimed as novel theory**. A real engineering-risk product would require mechanism-specific data, credible safety constraints, and external domain review.
