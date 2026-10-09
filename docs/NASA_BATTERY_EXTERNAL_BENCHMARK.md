# External measured-data evaluation: NASA PCoE battery aging

**Research-extension status:** *external held-out benchmark only; NOT physical validation of Vulcan GEM 63XL, launch reliability, guidance compensability or mission success.* Independent from the original LV-01 prospective forecast. **No release or DOI implied.**

## Original and processed data provenance
- NASA Ames PCoE primary battery research archive: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
- Citation: B. Saha and K. Goebel (2007), *Battery Data Set*, NASA Ames Prognostics Data Repository.
- This first executable benchmark uses [a **third-party extracted** CSV](https://github.com/amirhossein-sadeghi2003/battery-health-forecasting-baselines/blob/e414d2e00ecc369d042637df6a6147a948718649/data/processed/discharge_capacity.csv), not the raw NASA .mat bytes.
- Data commit `e414d2e00ecc369d042637df6a6147a948718649`; Git blob SHA-1 `adc395fdf25c6fa1b911535dc0ffc1c2a10e589e`. The script **refuses** data with a different Git blob hash.
- Four cells B0005, B0006, B0007 (168 discharge observations each) and B0018 (132), 636 cycles in total. Independent raw-NASA-versus-third-party data comparisons are **pending**. Do not use this derived table to assert raw-data provenance has been proven.

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

## Interpretation gate

This is a study of how forecast algorithms transfer to a real measurement process. It is **not** evidence that booster anomaly probabilities are calibrated, that the sample addresses the identifiability of physical failures versus public detection on rockets, or that a launch option is safe. A robust future extension should audit the third-party extraction against the original NASA .mat data, account for correlated measurements/heterogeneity, use multiple independent pieces of equipment and test calibrated predictive uncertainty against transparent decision costs.
