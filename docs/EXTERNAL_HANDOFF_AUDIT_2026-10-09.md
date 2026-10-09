# External handoff audit adjudication — 2026-10-09

**Classification: EX-POST AUDIT NOTE.** This file was created *after* the main prospective forecast files. It **does not alter** any of the five `forecast/*.json` predictions, their UTC scoring protocol, the main research prior, or the external forecast status. It is neither an independent expert review nor a physical validation of Vulcan GEM 63XL.

## A. Forecast public provenance: evidence verified from GitHub

A separate auditor lacked GitHub access and stated that no **independent public timestamp** had yet been established. That is partly superseded by **server-side GitHub records**:

| Source | Recorded UTC timestamp | URL |
|---|---|---|
| Public repository `created_at` | 2026-10-09 18:01:16 | https://github.com/MedeiroszJoao/Project-Vulcan |
| Earliest commit that adds `forecast/reference.json` | Git *committer date* 2026-10-09 18:04:14 | https://github.com/MedeiroszJoao/Project-Vulcan/commit/6d5c79405dad635af6999801e6c2534c91632922 |
| Current main `5b676fb8bf5e880f8d80f05ff6324753a507cf2b` | Git *committer date* 2026-10-09 18:05:50 | https://github.com/MedeiroszJoao/Project-Vulcan/commit/5b676fb8bf5e880f8d80f05ff6324753a507cf2b |
| Public GitHub Actions run on exactly that main commit | GitHub server `created_at` 2026-10-09 18:05:52, `conclusion=success` | https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37970901023 |

Crucial distinction: Git commit author/committer dates are embedded in client-authored Git objects and **do not alone independently establish publication time**. Public repository creation time and especially the **GitHub Actions server-created run**, which reports `head_sha=5b676fb8...`, supply separate service-side evidence that the repo and forecast hash were available by that server timestamp. Check the workflow logs and artifact attachment for preserved bytes.

As of this audit, `GET /releases` returned `[]`, and there is **no version release, repository DOI, or long-term archival guarantee**. Provenance is therefore public-GitHub-timestamp supported, **not** Zenodo/DOI-archived and not an independently notarized version package. **Do not backfill release metadata in a frozen forecast JSON.**

Primary frozen reference SHA-256: `fc9d0e290adef51459b86c8ad4a1a6ddc03ea087163e48da6e59f6d106f82d1f`.

## B. Current launch status and config uncertainty

On 2026-10-09, trackers list Amazon Leo LV-01, six-booster Vulcan VC6L, as **not yet launched**, with **tentative NET 2026-10-29** and **no ULA-operator-confirmed liftoff clock time**. Compare https://spacelaunchlive.com/launches/vulcan-vc6l-amazon-leo-lv-01/ and https://api.nextspaceflight.com/launches/details/7425 . These are **independent aggregators**, not primary ULA statements. Schedule changes are allowed by `docs/FORECAST_PROTOCOL.md`; uncertainty about booster revision remains. A change in internal GEM63XL revision with six boosters and VC6L nominally unchanged may invalidate reference transfer assumptions **without triggering** the predeclared objective VOID criterion. Record this as a model discrepancy **not** a justification for retrospective VOID or restating the prior.

## C. Public-report observation mismatch / what is actually shown

`src/model.py:outcomes_given_p` currently does the following for each latent mission consequence `Z`: `P(Y=loss_or_degraded_report)=disclosure*P(Z=loss/degraded)` and `P(Y=inconclusive)=1-disclosure` with baseline `disclosure=0.9`. The public protocol instead says **if a loss/degraded delivery is sufficiently confirmed before the cutoff, code it as a loss** without requiring attribution to the booster. The protocol DOES NOT assert that every physical loss is invariably known or publicly announced by the cutoff. The numerical discrepancy is therefore a **conditional observation-model assumption requiring evidence**, not an automatic logical proof that the frozen forecast is invalid.

Under the *new hypothetical stronger assumption* of perfect, timely reporting for all loss/degradation, while retaining 90% reporting conditional on successful delivery, the diagnostic counterfactual public-signal PMF is:

| Outcome | Frozen original | Hypothetical loss always reported |
|---|---:|---:|
| clean_report | 0.5973632855118782 | 0.5973632855118782 |
| anomaly_report | 0.2072166863854239 | 0.2072166863854239 |
| loss_or_degraded_report | 0.09542002810269795 | 0.10602225344744216 |
| inconclusive | 0.09999999999999995 | 0.08939777465525574 |

The alternative follows from `P(Z=loss/degraded)=0.09542002810269795/0.9` and preserving the successful-delivery signal mechanism. Independently recalculated symbolically/numerically with Wolfram Language. **This is a sensitivity counterfactual only, NOT a revised forecast or primary score.** Do not replace the frozen PMF.

## D. Battery Monte Carlo: micro-average cohort-composition artifact

[Draft PR #4](https://github.com/MedeiroszJoao/Project-Vulcan/pull/4) reports results from NASA PCoE measured battery capacities of **11 physical battery cells** and 349 held-out discharge cycles, with three nominal protocol groups. Only 3 cells contribute 237/349 = **67.9083%** of pooled observations. Recomputed with Wolfram Language:

| MAE (Ah) | Driftless random walk | Linear Student-t | Trend + AR1 MC |
|---|---:|---:|---:|
| ALL 349 held-out measurements | 0.05909360 | 0.07713399 | 0.07665141 |
| **Other 8 cells**, 112 held-out measurements | 0.02860834 | 0.01808031 | 0.01816933 |

Therefore the claim `random walk wins overall` is **sample-composition dependent**, not cross-device model superiority. The baseline's near-nominal/high coverage must also be reported alongside **1.6408 Ah average nominal 90% interval width** — very broad for these ~2Ah cells. The pooled AR1 model is also under-covered: 84.81% at nominal 90%.

All metrics reflect **serially dependent within-device measurements**, not 349 independent samples. The bootstrap choice, threshold, model parameters and split were historical/offline; they were prespecified within that research commit before its *specific* held-out outcome inspection but not in an independent prospective registry. Inferences across batteries/campaigns are weak with 11 devices, different thermal/current/cutoff protocols, and no mechanistic normalization. The work is **forecast-method stress testing**, NEVER booster physical-risk calibration.

Primary successful runs: https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37995095971 and https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37994245909 (636/636 raw NASA battery discharge capacities matched independent reference extract).

## E. Main CI and reproducibility are intermittently sensitive to last-bit floating rounding

Runs `37995096041` and `37995178307` target the **same PR #4 commit** `7f7130206...`; one succeeds and one fails after all **42 baseline tests completed successfully** because the main workflow runs the byte-strict `build_forecast.py --check` numerical recomputation. This is last-bit floating-point string variability and does **not** imply that the committed forecast bytes themselves changed.

Draft PR #2 contains `verify_frozen_forecasts.py` with:
1. Exact fixed SHA-256 bytes for each of the **five committed forecast JSON files** (no tolerance).
2. Independent fresh numerical re-derivation with `1e-12` float tolerance and exact metadata/categories comparison.

Do **not** merely relax file-integrity checks or rewrite the published JSON. Keep strict byte integrity + numeric tolerance as **two separate gates**. See https://github.com/MedeiroszJoao/Project-Vulcan/pull/2 and https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37988520245 .

## F. Evidence-backed priority actions and standing limitations

1. **Do not modify main, archived forecast JSON or scoring protocol.** Record these external audit findings dated 2026-10-09 and their URLs.
2. Keep PR #2, PR #3 and PR #4 as **three separate draft research streams**. They are accessible through the linked GitHub refs; a local ZIP of metadata is not equivalent to hydrated branch source.
3. Add per-cell, per-cohort, device-level uncertainty and proper interval/CRPS scores in a **future clearly post-hoc** analysis. Do not retrospectively change predeclared scoring protocols or claim untouched holdouts after selecting models by observed outcomes.
4. Analyze physically justified CPT and cost break-even contours; sampled 360-scenario frequencies are **not** posterior probabilities.
5. Main `CITATION.cff` and `LICENSE` contain placeholders; do not authorize a specific identity or license without explicit consent. Only after that consider a tagged GitHub release and Zenodo archive.
6. Source the next rocket forecast against operator-issued primary confirmation, including revision/lot if available. Do not infer hardware repair quality from public media.
7. Physical validity, independent safety review, calibrated booster reliability and any operational flight recommendation remain **NOT ACHIEVED**.

**Audit scope:** independent source and mathematical consistency check with GitHub server data and Wolfram; not peer review or assurance certification. No third-party publication credentials implied.

## G. Correction to the external audit's dependency claim

The external audit says that **`requirements.txt` pins 100+ packages including CadQuery and VTK**. Direct GitHub inspection **refutes this statement**. Current `main` [`requirements.txt`](https://github.com/MedeiroszJoao/Project-Vulcan/blob/main/requirements.txt) contains exactly **four** direct pins: `numpy==2.3.5`, `scipy==1.17.0`, `matplotlib==3.10.8`, and `pgmpy==1.1.2`. The longer [`environment.txt`](https://github.com/MedeiroszJoao/Project-Vulcan/blob/main/environment.txt) is a snapshot of the broader original preinstalled runtime, including CadQuery, CasADi, VTK and unrelated packages; it is **not** the declared application installation requirements. Note that four direct pins still do not fully lock the transitive dependency graph; discuss reproducibility of transitives separately rather than inventing direct dependencies.

This correction is independent of whether the program actually uses some installed package; deployment requirements must be inferred from imports and declared dependencies, not from every item in a `pip freeze` snapshot.
