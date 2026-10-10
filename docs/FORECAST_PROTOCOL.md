# LV-01 Prospective Observation and Scoring Protocol

*English translation of the original protocol dated October 9, 2026. This translation does **not** establish a new prediction, ex-ante registry event, or DOI. The original Portuguese text is preserved in earlier Git commits.*

**Historical status: unpublished candidate as of October 9, 2026.** This is a scenario-based exercise, not physically calibrated. No local file by itself establishes independent prospective registration. At the original cutoff this protocol superseded the previously submitted draft prior to public freeze.

## Episode and eligibility

Target: the first launch publicly identified as **Amazon Leo LV-01 on Vulcan VC6L with six solid boosters**, provided an externally verifiable registration predates launch, and actual liftoff occurs before **2027-01-01 00:00:00 UTC**, exclusive. This 2026 expiry is an administrative choice, **not** a forecast of launch date.

A material mismatch in nominal vehicle configuration invalidates this episode: record `VOID_CONFIGURATION` with supporting evidence, **without** a numerical score, and do not reuse a forecast selectively. The MM internal-revision state remains an unverified hypothesis; a later disclosure about actual revisions does not permit swapping an already published primary forecast.

Delays within the validity period **do not** expire the primary prediction or justify replacing it. Publish updates separately if appropriate, always retaining and eventually scoring the primary. If no eligible flight occurs before expiry, record `NOT_LAUNCHED` without score, supported by documentary verification published *after* expiry. A later flight requires a new prospective episode. This forecast is **conditional on a flight**, and does not predict launch date.

## Exact UTC cutoff

T0 is actual liftoff UTC. The primary evidence window closes at **00:00:00 UTC at the start of the UTC calendar day 15 days after the UTC liftoff date**, exclusive. Thus the full fourteenth UTC calendar date after liftoff is included. For liftoff on October 29, cutoff is November 13, 00:00:00 UTC. This is not generally the same as exactly 336 elapsed hours after ignition. The T+72-hour digest is preliminary and cannot revise the primary forecast.

The outcome may be coded or published after cutoff **only** from information demonstrably public before it. Record each source's `first_public_at_utc`, archived bytes and SHA-256. An online page edited after cutoff does not by itself establish what that page said earlier: use preserved captures, version histories or independently timestamped records. If publication timing cannot be resolved to the allowed window, do not use that item to choose the category; document the uncertainty. Later news never rewrites the primary endpoint.

## Coding four mutually exclusive Y outcomes

1. `inconclusive`: public information is insufficient to determine mission delivery/reporting status, or contradictory qualified statements cannot be resolved by cutoff. Failure to conduct a search is **not** evidence that nothing was reported.
2. `loss_or_degraded_report`: adequate qualified confirmation of lost or degraded delivery, regardless of whether a solid booster was causal. Do not require motor details before classifying a known delivery failure.
3. `anomaly_report`: delivery succeeded **and** a qualified source explicitly attributes one or more anomalies to solid-booster hardware, nozzle or performance.
4. `clean_report`: successful delivery confirmed **and** no qualifying booster anomaly discovered within the pre-specified public-source search. This does **not** imply physical K=0.

Qualified sources include statements or updates attributable to ULA, Northrop Grumman, Amazon/payload operator or applicable mission authority. A news report may locate an attributable statement, but archive the content and its actual attribution. Unattributed images/speculation alone are insufficient. Success means delivery to the intended orbit as declared by operator or launcher, not simply spacecraft survival. Later satellite anomalies unrelated to delivery are outside this endpoint. Unresolved cases remain inconclusive.

A clean classification requires evidence of delivery success **and** an archived search log of the relevant public channels of ULA, Northrop, the operator and any applicable authority through cutoff. Include LV-01, Amazon Leo, Vulcan and anomaly/booster/nozzle search terms. Record inaccessible pages. If the minimum search cannot be documented with temporally valid evidence, classify inconclusive. Ideally use two independent coders; any unresolved documentary disagreement at cutoff remains inconclusive. Such controls limit but do not remove classification subjectivity.

The reference model uses **state-independent missingness** to produce inconclusive reports; real reporting conflicts or inaccessible information can violate that assumption. Record a model discrepancy rather than redefining the category after observing results.

## Prediction and proper scores

Primary object: `forecast/reference.json`, nominal MM scenario with correction-regime weights (0.2,0.6,0.2). Four alternative scenario files are predeclared sensitivity forecasts, not post-hoc substitutes for the primary. All exact parameters and probability vectors are stored in the original five JSON files.

Y is the observable public report. K=0..6 denotes the **latent physical motor anomaly count**, which is **not scored** for this episode because no independently frozen and validated physical ascertainment protocol exists. The exploratory count-report signal is likewise not a primary endpoint. Lack of a public anomaly report is not a physically measured zero.

Multiclass **Brier sum**: B = sum_i (p_i - 1{i=j})², range [0,2]. **Log loss**: −ln(p_j), in nats. Lower is better. A realized zero-probability outcome has infinite mathematical log loss, represented in JSON by `null` and `zero_probability_observed=true`, without silently clipping. One flight allows evaluation of a score but not establishment of calibration. A low-probability observed event does not logically refute a distribution assigning positive support; it incurs the predeclared score.

## Postflight scoring record

Prepare a documentary JSON (the illustrative placeholder fields below are deliberately invalid, and are neither actual results nor proof of registration):

~~~json
{
  "registered_forecast_sha256": "SHA256_OF_ACTUAL_REGISTERED_BYTES",
  "freeze_url": "https://PUBLIC_REGISTRY_URL_TO_VERIFY",
  "commit_sha": "REAL_40_CHARACTER_COMMIT_SHA",
  "registered_at_utc": "VERIFIED_UTC_INSTANT_BEFORE_LIFTOFF",
  "coded_at_utc": "CODING_TIME_AFTER_EVIDENCE_CUTOFF",
  "flight_at_utc": "ACTUAL_LIFTOFF_UTC",
  "configuration_matches": true,
  "outcome": "DOCUMENTED_CATEGORY",
  "evidence": [{
    "url": "https://SOURCE_URL",
    "first_public_at_utc": "VERIFIED_UTC_INSTANT_BEFORE_CUTOFF",
    "snapshot_file": "PATH_RELATIVE_TO_SCORE_RECORD",
    "snapshot_sha256": "ARCHIVED_SOURCE_BYTES_SHA256"
  }]
}
~~~

Run:

~~~bash
python score_episode.py --forecast forecast/reference.json \
  --record scoring/evidence_record.json \
  --output scoring/episode_01_T14.json
~~~

The scorer verifies stored snapshot hashes, forecast hash, category order, UTC chronology, episode validity, evidence cutoff, identifier syntax, and refuses to overwrite an existing output.

For scored outcomes and `VOID_CONFIGURATION`, at least one qualifying source must be published **after liftoff and before T+14 cutoff**; a preflight schedule cannot prove a completed outcome. For `NOT_LAUNCHED`, omit `flight_at_utc`, code **after** expiry, and include a documentary nonlaunch check published at or after expiry but no later than the coding time. No-launch receives **no score**. The exceptional post-expiry check verifies that an eligible historical launch did not occur; it does not reopen the primary forecast observation window.

For `VOID_CONFIGURATION`, provide `outcome=VOID_CONFIGURATION`, `configuration_matches=false`, an actual `flight_at_utc`, a concrete `configuration_change_description`, and verifiable evidence that physical configuration differed from six boosters and nominal VC6L. Changing providers or configurations cannot be invoked selectively after viewing mission performance.

**External verification limit:** This is an offline consistency checker. It cannot authenticate that a submitted URL, hash, timestamp or operator statement is truthful or was publicly available at the claimed time. Independently open the release/registry and compare the exact bytes. The program declares this limitation. A fabricated JSON record is not prospective registration.

## Public registration

Before flight: publish exact forecast bytes, hashes, protocol and commit; independently verify the public release URL and its time. A version DOI is desirable **only after** it has actually been issued and verified. Never retrospectively insert it into the preserved forecast JSON. Document external registration metadata separately. Individual authorship and licensing were still pending at the original review cutoff.

Methodological reference: Gneiting & Raftery (2007), https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf .
