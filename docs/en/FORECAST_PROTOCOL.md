# LV-01 prospective observation and scoring protocol — English reader version

**Status:** English reference translation prepared after the original 9 October 2026 research draft. The [full English translation of the original dated protocol](../FORECAST_PROTOCOL.md) is authoritative for reproducing the historical coding rules. This shorter guide and the full translation do not alter any frozen candidate forecast JSON or retroactively establish a publication or pre-registration timestamp.

## Episode and validity

The episode targets the first flight publicly identified as Amazon Leo LV-01 on nominal Vulcan **VC6L with six solid boosters**, provided an independently verifiable public forecast registration occurs before liftoff. The episode's fixed validity ends **2027-01-01 00:00:00 UTC exclusive**. This administrative limit is not a prediction of the launch date.

A delay *within* the validity period does not expire the primary prediction. If no eligible launch occurs before expiration, disposition is `NOT_LAUNCHED`, with documentary confirmation collected after the window and **no numerical score**. A later launch is a different prospective episode. A material mismatch in the nominal six-booster VC6L configuration is recorded as `VOID_CONFIGURATION` without a score, supported by documentation. Do not relabel the episode only after observing an unfavorable outcome.

The internal modified-hardware MM revision is explicitly an **unverified scenario assumption**, not a confirmed part configuration. Later news about internal revision changes does not authorize rewriting the archived primary prediction.

## Exclusive UTC observation cutoff

Let `T0` be actual liftoff in UTC. The primary evidence cutoff is **00:00:00 UTC at the start of the UTC calendar date 15 days after the UTC liftoff date**. It includes the entire fourteenth UTC date following the liftoff date. For an October 29 liftoff date, the cutoff is **November 13, 00:00 UTC**. This is **not** necessarily exactly 336 elapsed hours after ignition.

Evidence can be coded later, but only information proven public *strictly before this cutoff* determines the primary categorical outcome. A 72-hour note is preliminary, never a forecast revision.

## Four mutually exclusive public outcomes

1. `inconclusive` — public evidence is insufficient or contradictory to determine delivery/reporting status. Incomplete research is not the same as no reports.
2. `loss_or_degraded_report` — qualified public evidence confirms lost or degraded mission delivery, whether or not a solid booster caused it.
3. `anomaly_report` — delivered successfully, but qualified public reporting attributes at least one anomaly to solid-booster hardware, nozzle or performance.
4. `clean_report` — delivered successfully, with no qualifying booster-anomaly report discovered under the specified search protocol. **This does not establish that no physical anomaly occurred.**

Qualified sources are launch provider ULA, Northrop Grumman, payload owner/operator or relevant mission authority statements. Journalistic reporting may direct the search toward an attributable statement; unattributed speculation or visual inference alone does not suffice. Delivery success requires a publicly confirmed designated orbital delivery, not merely an intact spacecraft.

A clean classification requires both a delivery-success record and documented searches across the qualified public channels through the cutoff, including terms such as LV-01, Amazon Leo, Vulcan, booster, anomaly and nozzle. Missing accessible archival evidence can require `inconclusive`. Independent double coding is preferred; unresolved documented disagreements remain inconclusive.

Reference modeling uses an independent public-disclosure missingness assumption. Actual state-dependent reporting may violate it and must be recorded as model discrepancy, not silently patched after seeing the outcome.

## Archived prediction and proper scoring

`forecast/reference.json` is the original reference, conditional on an eligible liftoff and specified assumed parameters. The other four `forecast/*.json` objects are pre-specified sensitivity forecasts. None may substitute for the reference after observing the event.

The primary forecast scores the four-category public report with:

- **Multiclass Brier sum:** \(\sum_i(p_i-\mathbf{1}_{i=y})^2\), in \([0,2]\).
- **Log loss:** \(-\log(p_y)\) in natural units (nats).

Lower is better. If a realized outcome has zero assigned probability, the mathematical log loss is infinite; the code represents it as JSON `null` accompanied by `zero_probability_observed=true`, rather than silently clipping the probability. One observed categorical event can be scored but cannot establish probability calibration.

The model also yields a hypothetical physical anomaly-count distribution, but this is **not scored** absent an independently established counting/ascertainment protocol. Lack of a public anomaly report does not supply a measured count of zero.

## Documentary score record

The scoring command accepts a JSON record documenting the actual frozen public object, its registered hash and URL, UTC timestamps, eligible flight, observed classification and timestamped evidence:

```bash
python score_episode.py --forecast forecast/reference.json \
  --record scoring/evidence_record.json \
  --output scoring/episode_01_T14.json
```

Expected fields: `registered_forecast_sha256`, `freeze_url`, `commit_sha`, `registered_at_utc`, `coded_at_utc`, `flight_at_utc` when applicable, `configuration_matches`, `outcome`, and one or more `evidence` records containing `url`, `first_public_at_utc`, `snapshot_file` and `snapshot_sha256`.

The offline program checks field consistency, hashes, outcome class, chronology, the publication window and overwrite safety. It **cannot independently authenticate** a GitHub release, publication timestamp, external URL, official launch claim or source bytes it has not received. Those must be independently opened and checked.

For scored outcomes or `VOID_CONFIGURATION`, documentary evidence must include a qualifying record published after liftoff but before T+14 cutoff; a preflight schedule is not a mission-result source.

For `NOT_LAUNCHED`, omit liftoff time, code only after the expiry and include post-expiry documentary evidence confirming no eligible launch during the prior observation window. These special later records verify a negative historical fact; they do not reopen prediction-scoring observations.

For `VOID_CONFIGURATION`, require `configuration_matches=false`, a concrete `configuration_change_description`, a qualifying flight time and verifiable evidence of objective six-booster/VC6L mismatch.

## Independent public registration

Before the flight, publish and independently verify **exact bytes**, SHA-256 digests, code commit and scoring protocol. The timing of public release must be checked externally. A version DOI is desirable only when issued and verified; neither Git commit metadata alone nor a placeholder DOI proves an independently archived prospective forecast.

Do not retroactively add DOI, outcome or publication information to a historical forecast JSON. Record publication details separately.

Methodological source: Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf.
