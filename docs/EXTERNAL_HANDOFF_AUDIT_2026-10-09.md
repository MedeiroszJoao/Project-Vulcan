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

## H. Claude's second independent CI review and NASA subgroup findings

A subsequent independent review obtained actual CI artifacts and identified three further issues. This dated note is **post hoc**, not a new blind benchmark.

1. **GitHub PR synthetic merge checkout:** PR #3 Actions [run 37994363590](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/37994363590) reports the proposed PR head `5baa0edd043603d5c9ba5fa83cd87dfe5daaea72` in API metadata, but the job's `actions/checkout` actually checked out `refs/pull/3/merge` at **`62f51ec34c03636a8399e62405fb34d689613e7a`**, the synthetic merge of PR head into main `5b676fb8bf5e880f8d80f05ff6324753a507cf2b`. PR #2 Actions run 37988520245 and PR #4 Actions run 37995095971 directly checked out their branch head commits, respectively `80304b4d...` and `7f713020...`. Therefore prior statements that *all three* CI runs checked out *exact head SHA* were overly broad. Both merge checkout and head SHA must appear in the evidence ledger.
2. **Not all longer series are ordinary monotonic aging curves.** Real PR #4 `report.json` shows B0033 first-to-last capacity `0.06843→1.31528Ah`, B0034 `0.74593→1.28026Ah` and B0036 `1.00198→1.55911Ah`; the three contribute `237/349=67.91%` of held-out points. An endpoint increase does **not by itself prove** no degradation within the interior cycles. The precise cause remains undetermined pending inspection of original NASA cycle timestamps, voltage profiles and loading. A dedicated read-only raw-data diagnostic has been added to PR #4 branch, separate from its original benchmarks. Do not exclude any of the three from the *original* 11-device post-hoc results; instead clearly disaggregate.
3. **PR #3 proper log density reverses MAE preference:** over 257 serially dependent held-out cycles, cycle-weighted mean negative log density is **−0.960234** for the last-value/random-walk baseline, **−0.441924** for the linear Student-t alternative (**lower better**), even though linear wins MAE (0.059621 vs 0.097907 Ah). The sign can be negative for continuous *densities*; it is not a negative discrete-event log loss. This comparison, including all four devices separately, is now documented directly in PR #3's benchmark document.
4. **AR(1) implementation is not posterior predictive:** plug-in Gaussian AR(1) paths fix estimated trend coefficients, `phi` and `sigma`; omit parameter uncertainty and model discrepancy. Random-walk bootstrap increments can produce wide uncertainty. Neither observation supports a universal ranking; 1.4Ah threshold Brier on 11 heterogeneous devices is weak evidence.

**Actions taken without changing main:** edited post-hoc research documents in PR #3 and PR #4, retained all original `report.json` outputs and CI run artifacts, added a separately scheduled raw NASA measurement diagnostic in PR #4. No original prospective `forecast/*.json` was edited. Formal release/DOI, author, and license require the owner's decision.


## I. Original NASA MAT raw-waveform audit corrects the apparent absence of degradation

A successful [raw measurement diagnostic run 38001072638](https://github.com/MedeiroszJoao/Project-Vulcan/actions/runs/38001072638), on the original NASA battery MAT archive, **falsifies the overbroad inference** `B0033/B0034/B0036 are not degradation data`. Their *first* discharge measurement is unusually low (0.0684/0.7459/1.0020Ah), and it has an initial measured voltage of ~3.68/3.85/3.85V versus ~4.18–4.19V on the **second** cycle. The first recorded discharge lasts ~1,819 seconds, versus ~3,261 seconds for the second. This suggests, but does **not establish**, atypical initial conditions, possible initial partial charge, or truncated first discharge.

The diagnostic compared capacity distributions in the first, middle and last twenty discharge observations. Medians **decline**, respectively B0033 `1.58837→1.43407→1.32946Ah`, B0034 `1.45970→1.34416→1.28546Ah` and B0036 `1.78485→1.69399→1.59532Ah`. Therefore the trajectories contain evidence of *battery capacity fade despite misleading low first-cycle endpoints*. This does not fix the cohort-weighted comparison, heterogeneous cutoff/current conditions, AR1 parameter uncertainty or weak event scoring.

**Adjudication of Claude's note:** `three dominant cells are not degradation data` is **not supported**; `some initial measurement conditions or labeling may be atypical and distort an unnormalized benchmark` is **supported**. Do not delete the three from the originally scored 11-cell experiment. The original numerical predictions and scores remain unmodified. A future, explicitly post-hoc sensitivity analysis can compare alternate initial-condition filters, with all deviations labeled.
