# Integration Review of the Prospective Forecast Candidate — October 9, 2026

*Dated technical review, translated into English. Statements about unavailability of a GitHub repository refer to that particular earlier review session.*

**Historical result: candidate numerically reproduced; independent public forecast registration pending.**

The submitted package introduced the scoreable probabilistic prediction. Its decision core predated the operational audit corrections. The integration preserved both contributions and retained the submitted originals as evidence.

## Findings and checks

| Item | Review result |
| --- | --- |
| Economic break-even point | USD 1.279001 million, reproduced only for the old fixed-slot reference |
| Maximum regret in original grid | Reallocate: USD 0.744 million; wait: USD 15 million; no claim outside the grid |
| Y forecast | Four-state reference PMF reproduced; MM revision remains hypothetical |
| Latent physical K | Published as unobserved, deliberately **unscored** |
| Proper scoring | Multiclass Brier sum [0,2], log loss in nats, zero-probability outcomes without clipping |
| Episode eligibility | First qualifying nominal LV-01 after independent publication, before 2027-01-01 UTC |
| Delays | Keep original primary prediction within validity; never substitute retrospectively |
| Evidence cutoff | End of the 14th subsequent UTC date; code later only against earlier evidence |
| Integrity | Stored forecast and snapshot hashes checked locally; external publication not authenticated offline |
| Historical tests | 37 passing after installing pgmpy; complete reproduction reported |
| Operational extensions | Informative approval G, slot uncertainty, reservation, integration, fallback and 2027 planning window |
| Documents | SPEC, summary, technical note and protocol harmonized; license remained a proposal |

## Correct interpretation

The reference is a conditional probabilistic candidate and a decision under assumed economic and physical CPTs, not empirical evidence of its accuracy. A single subsequent proper score cannot establish calibration, and a low-probability event with positive assigned probability does not logically invalidate the distribution.

Primary Y PMF: `[0.5973632855, 0.2072166864, 0.0954200281, 0.1]` for clean, delivered-with-reported-anomaly, loss/degraded, and inconclusive. The original economic threshold assumed guaranteed backup availability and must not be presented as a result of the later operational planning scenarios.

The 360 structural, 432 operational and 12 physical-control scenarios are **separate experiments**, not a probability distribution over all models. A reduced informative-approval model affects both what is learned and the approval rate; it does not identify the value of real private telemetry.

## References consulted during the review

- Gneiting & Raftery (2007): https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf
- NASA-STD-7009B (2024-03-05): https://standards.nasa.gov/standard/NASA/NASA-STD-7009
- NASA-HDBK-7009B (2026-02-03): https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009

They provide terminology and model-credibility practices, not NASA certification.

## Outstanding at that date

Human coding/CPT review; verified author and license; publicly authenticated version/timestamp and any actual DOI. `CITATION.cff` was then a draft. No messages to reviewers were sent. EVPPI, hierarchical pooling and hindcasting remained proposals, not delivered work.

## Adversarial patch closure — October 9, 2026

The submitted patch was applied to the original Git checkout and full reproduction passed 42/42 tests, including pgmpy. All five prediction files matched the earlier Git commit and submitted archive byte for byte. `VOID_CONFIGURATION` became an unscored disposition; `NOT_LAUNCHED` required post-expiry documentary checks, and scored results needed post-liftoff sources. The Atlas path was corrected.

This only validates consistency checks, not the reliability of external evidence or each VOID determination. The review session's GitHub connection identified the account but reported no accessible repositories; that is **historical context**, not an assertion about present GitHub or CI status.
