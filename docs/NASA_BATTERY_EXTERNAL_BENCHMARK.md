# External measured-data evaluation: NASA PCoE battery aging

**Research-extension status:** *external held-out benchmark only; NOT physical validation of Vulcan GEM 63XL, launch reliability, guidance compensability or mission success.* Independent from the original LV-01 prospective forecast. **No release or DOI implied.**

## Original and processed data provenance
- NASA Ames PCoE primary battery research archive: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
- Citation: B. Saha and K. Goebel (2007), *Battery Data Set*, NASA Ames Prognostics Data Repository.
- This first executable benchmark uses [a **third-party extracted** CSV](https://github.com/amirhossein-sadeghi2003/battery-health-forecasting-baselines/blob/e414d2e00ecc369d042637df6a6147a948718649/data/processed/discharge_capacity.csv), not the raw NASA .mat bytes.
- Data commit `e414d2e00ecc369d042637df6a6147a948718649`; Git blob SHA-1 `adc395fdf25c6fa1b911535dc0ffc1c2a10e589e`. The script **refuses** data with a different Git blob hash.
- Four cells B0005, B0006, B0007 (168 discharge observations each) and B0018 (132), 636 cycles in total. The discharge-capacity fields were subsequently verified against original NASA MAT archives by an independent audit; see the successful run and checksums below.


## Independent original-NASA origin audit (completed 2026-10-09)

After the initial research CI run, a **separate** GitHub Actions workflow downloaded the [NASA official 209,708,670-byte ZIP](https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip), extracted the FY08Q4 cohort, and compared **every one of the 636 discharge-capacity values** against the pinned third-party CSV. **All 636 matched exactly (maximum absolute difference 0 Ah)**. This proves the *capacity values used in this benchmark* are faithfully extracted from the downloaded NASA archive, not that all other extracted fields or physical-world labels were validated.

- Original NASA archive SHA-256: `82302a7db4fc1b34e0b6676326610438d43b816bdf11a69d1d012a464ef2f92e`.
- Original `B0005.mat` SHA-256: `0eae4585baf3f200c09fe24c5ab884f1889679fc75206ca1aa19da704104f0b0`.
- Original `B0006.mat` SHA-256: `fa818ab4db5db8ab21e910b6dd6c3e20d3761bb9672089e1a4de8f96074616c5`.
- Original `B0007.mat` SHA-256: `d022afa086efaf54ab5b63f05220f5be178c8027e2fa8d68589db0e85a441a3b`.
- Original `B0018.mat` SHA-256: `d1e6c923a43ea1c9666b3a90bbb521757a067fd60b4d17dbfaa49c50b179da69`.
- [Public raw-data audit run 37994245909 — success](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37994245909).

The audited original raw data are downloaded only into the ephemeral CI environment; the third-party raw `.mat` files are not committed or redistributed in this repository.

## Frozen, adversarial evaluation protocol
For **each cell separately**, fit on its first `floor(0.60 * n)` discharge observations. Forecast the entire remaining period **once**, without using any subsequent measurement, rolling updates or test data for model tuning.

| Battery | Training discharges | Held-out discharges |
|---|---:|---:|
| B0005 | 100 | 68 |
| B0006 | 100 | 68 |
| B0007 | 100 | 68 |
| B0018 | 79 | 53 |
| **Total** | **379** | **257** |

Competing models: a *last-observed/random-walk* baseline with variance scaling by future horizon; linear least-squares trend with a nominal 90% predictive Student-t interval under a Gaussian linear model with a reference prior; and quadratic polynomial extrapolation (point only). Evaluate MAE, RMSE, signed bias, and when meaningful mean negative log density and interval coverage on **real held-out values**. No cross-cell or temporal leakage. The observed cycles within one battery are correlated; 257 future cycles do not represent 257 statistically independent systems.

## Preliminary independent cross-check
A separate simple JavaScript implementation reading the GitHub connector version of this CSV confirmed that linear extrapolation has held-out MAE values:

| Battery | Last observed MAE (Ah) | Linear MAE (Ah) |
|---|---:|---:|
| B0005 | 0.111910 | 0.022708 |
| B0006 | 0.125036 | 0.135129 |
| B0007 | 0.088963 | 0.027628 |
| B0018 | 0.056609 | 0.051148 |

This is deliberately NOT a uniform model victory. B0006 is worse under linear extrapolation. No variance-calibration conclusion follows from MAE.

## Reproduce and tests

```bash
python -m pip install -r requirements.txt
python research_battery_benchmark.py --self-test
python research_battery_benchmark.py
```

The data download is explicit; there is **no synthetic fallback** if the real download fails, the source hash changes, or columns/counts change. Unit tests use synthetic fixtures only for plumbing/leakage; scientific scores are produced only from the pinned external measured-data table.

GitHub Actions uploads `results/battery_external/report.json` and per-cell plots. All `forecast/*.json` files and the original launch scoring protocol are preserved, and CI separately verifies the primary forecast byte SHA-256. Independent technical validation, raw-NASA data validation, and external review remain open.

## Post-hoc scientific audit addendum (2026-10-09; not part of the original protocol)

These observed values come from the actual successful GitHub Actions [PR #3 benchmark run](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37994363590) on GitHub's synthetic pull-request **merge checkout `62f51ec34c03636a8399e62405fb34d689613e7a`** (`5baa0edd043603d5c9ba5fa83cd87dfe5daaea72` merged into `main` at `5b676fb8bf5e880f8d80f05ff6324753a507cf2b`), not a direct checkout of the PR head alone. The archived benchmark code and output were generated with the merge checkout. Thus the PR-head SHA describes the proposed source change but is not the exact executed Git checkout SHA.

**Scores are not interchangeable.** The continuous predictive **mean negative log density** (lower is better) reverses the pooled MAE ordering; negative numerical values are valid because probability *densities* can exceed one, unlike discrete probability masses. The reported log score has units relative to Ah and assumes each predictive density as implemented.

| Cell | Last/random-walk MAE (Ah) | Linear MAE (Ah) | Last/random-walk mean negative log density | Linear mean negative log density | Linear 90% interval coverage |
|---|---:|---:|---:|---:|---:|
| B0005 | 0.11191 | **0.02271** | −0.82215 | **−2.16826** | 98.53% |
| B0006 | **0.12504** | 0.13513 | **−0.72537** | 2.85008 | 16.18% |
| B0007 | 0.08896 | **0.02763** | −1.12820 | **−1.88950** | 73.53% |
| B0018 | 0.05661 | **0.05115** | **−1.22323** | −0.59343 | 50.94% |
| **Cycle-weighted across all four** | 0.09791 | **0.05962** | **−0.96023** | −0.44192 | 60.31% |

**Interpretation:** linear wins pooled MAE, last/random-walk wins pooled mean negative log density; outcomes split by cell. This is a descriptive result from **four physically distinct battery devices**, not reliable cross-system calibration. The scores were computed before this addendum; it does not change training, split, model fits, predictions, the raw source, or NASA source-verification hashes. Nominal 90% linear coverage of 60.31% is insufficient calibration for engineering use. The last/random-walk's broad predictive densities improve log score in this sample but may be poorly decision-informative.

**Terminology:** the NASA-derived `capacity_ah` series are repeated measured discharge capacities. Different cutoff voltages, temperatures and rates complicate comparison. The cutoff defined as 1.4Ah on a different experiment is not a universal physically equivalent threshold.

## Interpretation gate

This is a study of how forecast algorithms transfer to a real measurement process. It is **not** evidence that booster anomaly probabilities are calibrated, that the sample addresses the identifiability of physical failures versus public detection on rockets, or that a launch option is safe. A robust future extension should audit the third-party extraction against the original NASA .mat data, account for correlated measurements/heterogeneity, use multiple independent pieces of equipment and test calibrated predictive uncertainty against transparent decision costs.
