# Response to the Independent Audit — October 9, 2026

*English translation of the dated response; archival/publication status reflects the original review date.*

This is a public-data conditional decision exercise, **not** a validated launcher safety model or operational launch recommendation.

## Research position

We distinguish numerically correct calculations from physically justified assumptions. The original fixed-slot scenario remains a regression case. The principal contribution is to expose decision sensitivity to model structure, uncertainty, and available actions.

| Finding | Implemented response | Remaining limitation |
| --- | --- | --- |
| F01 — historic revisions | Beta reference restricted to a homogeneous submodel; flight-specific risk and detection stress | Revision identity unobserved; correction effectiveness not measured |
| F02 — private information in approval G | Joint P(Y,G,Z), decisions conditioned on G and latent-risk-dependent gate | Reduced, non-telemetry model; incomplete revision information |
| F03 — guaranteed alternative | Stochastic capacity, paid reservation, integration, deferral | Abstract contracts/costs; main grid still assumes a viable immediate alternative |
| F04 — short deadline | Jan–Mar 2027 planning window; earlier window a separate stress; T+14 signal and lead time | No provider commitment established |
| F05 — limited sensitivity map | Original 360-scenario envelope reproduced as primary map | No full cross-product with new controls |
| F06 — multiple SRB anomalies | M* K≥2 loss P in {0.1,0.3,0.55,0.8}; fixed degraded P=0.2 | Uncalibrated sensitivities |
| F07 — Atlas | Separate 2025–26 extension with UTC corrections | Excluded from baseline posterior |
| F08 — lambda | Explicit epistemic dependence mixture | Not a physical failure-correlation estimate |
| F09 — feasibility | Zero-boosters excluded; 3,000 kg direct GEO hypothetical | Vehicle-to-payload compatibility unverified |
| F10 — reporting | State-dependent disclosure and per-flight detection | Other censorship processes remain |
| F11 — schedule | Tentative secondary NET is not confirmed ULA liftoff | Revalidate before prospective release |
| F12 — provenance | Build records/checksums and scope declared | At cutoff, author/license/release/DOI pending |
| F13 — tests | 21 historic tests run with pgmpy | Later code needs fresh third-party review |
| F14 — arithmetic | Submitted adaptive integration independently rerun | Verifies calculation, not physical CPTs |

## Reproduced results

The 3,111-cell envelope across 360 scenarios contains **2,775 reallocate-in-all, 336 disagreement, and zero wait-in-all** cells. Every min/max and classification matched the supplied CSV within 1e-10 USD million. The scenario list has no assigned probability distribution.

Fixed reference: pure EVSI USD 3.989851 million; immediate reallocation USD 35.750000 million; waiting USD 44.470999 million; net benefit of waiting −USD 8.720999 million. These reference results do not carry over unchanged to the operational scenario extension.

Added **432 operational scenarios** and **12 distinct physics/observation controls**. They are not a single joint uncertainty envelope. Reservation is paid before seeing a signal, not selected freely after observing it. Explicit deferral has its own hypothetical loss.

## Corrected UTC dates in the received audit

| Mission | Original received date | Correct UTC date/time | Source |
| --- | --- | --- | --- |
| ViaSat-3 F2 | 2025-11-13 | 2025-11-14 03:04 | https://www.ulalaunch.com/missions/next-launch/atlas-v-viasat-3-f2 |
| Amazon Leo 6 | 2026-04-27 | 2026-04-28 00:53:30 | https://www.ulalaunch.com/missions/next-launch/atlas-v-amazon-leo-6 |

Total exposure count was not affected. The original attachment remains in history; only the research-table integration was corrected. Opening nine ULA pages and reading success reports does not prove physical anomaly-free exposures. GEM 63 identification: https://blog.ulalaunch.com/blog/kuiper-2-atlas-v-to-launch-amazons-next-step-in-journey

## Non-self-referential artifact records

`SHA256SUMS` intentionally excludes its own hash and Git internals. `BUILD_RECORD.json` describes the base commit/build procedure, not the hash of its own containing commit. Find the actual delivery commit through `git rev-parse HEAD`.

## Conditions for a defensible publication

The conditional decision argument establishes that information can matter in modeled circumstances, **not** that a real operator should wait. Human review of assumptions, identity, licensing, and a genuinely published, independently verifiable release remained necessary. Previous conditional acceptance did not amount to external review of the new extensions.
