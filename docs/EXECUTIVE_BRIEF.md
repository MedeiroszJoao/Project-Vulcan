# VULCAN | When is waiting worth the information?

**Independent quantitative aerospace risk and economic decision analysis**  
**Decision and forecast candidate | 9 October 2026 | NOT YET PUBLICLY FROZEN**

> **Decision first.** Under the reference *illustrative* scenario, observing the next Vulcan flight only justifies waiting if the *incremental* cost of waiting is **below US$ 1.279 million**. At US$ 10 million delay cost, the model chooses immediate reallocation instead: expected costs US$ 35.750m (now) versus US$ 44.471m (wait), i.e. net waiting value **−US$ 8.721m**. These are conditional results under hypothetical consequence and approval probabilities, NOT a recommendation for an actual mission or a safety estimate.

## What could change the decision?

| One-at-a-time control | Reference | Evaluated alternatives | Waiting-cost break-even C_D (US$m) |
|---|---:|---|---:|
| Incremental price of alternate provider | 30 | 10 → 100 | −5.000 → 40.497 |
| Alternate provider modeled loss chance | 0.005 | .001 → .020 | −0.872 → 9.343 |
| Additional price of a late alternate switch | 5 | 0 → 20 | 3.591 → −5.657 |

These are the three largest **numerical** threshold ranges among the supplied one-at-a-time controls, not a causal ranking or evidence-based sensitivity of the real ULA/Space Force situation. A negative threshold means waiting loses even at zero delay cost given the relevant other assumptions. For the 360 structural scenario configurations held to the reference financial inputs, **359 prefer reallocation at C_D=10, one prefers waiting**. The structural break-even ranges from **−US$ 5m to +US$ 10.744m**, so the US$ 1.279m threshold is **not universal**. No probabilities are assigned to the 360 scenarios.

## The decision problem

A hypothetical planner responsible for a **3,000 kg communication satellite M\*** with direct GEO delivery and a planning window of 15 Jan–15 Mar 2027; the original Nov–Dec 2026 window remains a stress case asks: **wait for public evidence from Amazon Leo LV-01 before selecting a rocket, or procure an alternative now?** The backup rocket/slot, its pricing, and M\* compatibility are model assumptions. A zero-SRB Vulcan option is excluded. Launching without required authorization is counterfactual only.

The core uses: observed booster-anomaly reports on four earlier Vulcan flights (12 booster-flight exposures, two publicly reported anomalies), a Beta prior, an explicit latent correction-effect scenario Θ, six boosters on the contemplated LV-01, outcome/observation models, and finite exact-enumeration decisions. The physics-to-mission CPTs and cost ranges are **analyst-assigned placeholders, not flight-certified likelihoods**. Evidence on successful mission compensation must not be transferred between different mission configurations.

## Prospective public LV-01 forecast (reference, model-implied)

| Public T+14d observation Y | Probability |
|---|---:|
| Successful mission and clean report | **0.597363** |
| Successful mission with booster anomaly report | **0.207217** |
| Public degraded/lost mission report | **0.095420** |
| Inconclusive disclosure | **0.100000** |

These probabilities are **conditional on LV-01 actually launching**, and on an **unverified MM hardware-revision assumption** and scenario CPTs. The primary proper scores are the full multiclass Brier sum (range 0–2, lower is better) and logarithmic loss in nats. If no launch occurs, no score is assigned; a delay within the declared validity ending 1 Jan 2027 UTC preserves the primary forecast; a flight beyond that limit requires a new episode. A preliminary information review occurs at T+72h; classification for scoring is fixed at **the end of the 14th UTC calendar day after the liftoff date**. Physical booster count K=0..6 is released separately, but **not scored** without an independently ascertainable count: no report ≠ proof of zero anomaly.

## Assurance, provenance, limitations

- Numerical reference reproduced independently. Integrated tests, including `pgmpy`, pass locally; external CI remains pending.
- Historical revisions/lots and detection are only partially observed; correlated common-cause stress test ρ is a synthetic all-or-none mixture, not a physical fault tree.
- The regulatory decision might depend on nonpublic telemetry. Available alternative launch slots, integration lead times and direct-GEO compatibility are not verified. Slot/reservation, integration and informative approval are now implemented as 432 separate scenario sensitivities. **Real operational feasibility remains unresolved**.
- The active reference standard is NASA-STD-7009B (2024), companion NASA-HDBK-7009B (2026); this independently built project makes **no NASA compliance or affiliation claim**.
- The freeze is **not established** until a public release and independent external timestamp/DOI have been checked. Private/local Git hashes do not prove priority.

**Read next:** `docs/TECHNICAL_NOTE.md` → `SPEC.md` → `forecast/reference.json` → `docs/FORECAST_PROTOCOL.md` → code/tests.  
**Sources and citations:** `docs/SOURCE_REGISTER.md`; **errors and corrections:** `docs/RED_TEAM_LOG.md`.

The threshold and regrets above belong to the fixed-slot original reference. See `AUDIT_RESPONSE.md` and `INTEGRATION_REVIEW.md` for extensions and remaining limits.
