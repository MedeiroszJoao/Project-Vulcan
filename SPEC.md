# Vulcan: Value of Information from an Observed Commercial Flight

**Independent public-data decision-analysis exercise. Not an operational recommendation, engineering certification, or official launcher safety assessment.**

*English translation of the original specification dated October 9, 2026. Historical status statements and deadlines below describe that date; original Portuguese text remains accessible from the earlier Git commit. Translating this record creates no new prospective timestamp or revised prediction.*

**Original status:** revised research specification, executable code and tests, but no independently archived public freeze at the time. The requested delivery was before October 18, 2026, with an internal October 17 target in America/Sao_Paulo. No automated future work was scheduled.

## 1. Research question and target M*

Under which assumptions can the information obtained from observing the forthcoming LV-01 flight compensate for the incremental cost of waiting before assigning a sensitive mission?

An independent hypothetical planner, unaffiliated with actual operators, makes a decision for a single resilient communications satellite.

| Variable | Study assumption |
| --- | --- |
| Payload mass | 3,000 kg; hypothetical, not a real mission manifest |
| Orbit | Direct circular geosynchronous delivery, reference altitude 35,786 km, intended inclination approximately zero |
| Reference vehicle | Vulcan with four solid boosters and a high-energy Centaur variant; compatibility assumed for the exercise, **not certified** |
| Planning window | January 15, 2027, 00:00 UTC through March 16, 2027, 00:00 UTC (exclusive upper bound) |
| Nominal launch date | January 15, 2027; the earlier November–December 2026 window is separately retained as stress |
| Hypothetical payload book value V | USD 250 million |
| Total loss consequence L | USD 250–2,000 million; reference USD 1,000 million **already includes V** |
| Degraded consequence | dL, with reference d=0.25 and sensitivity d in [0.1,0.5] |
| Alternative | An abstract provider with assumed capacity, authorization and launch slot; **not a SpaceX performance estimate** |

Secret strategic-loss valuations are not estimated. L is a variable decision threshold and could be replaced by a risk constraint. The implemented reference assumes monetary risk neutrality and does not enforce a regulatory mission-loss probability limit.

## 2. Decisions and event sequence

- Initial decision D0: reallocate immediately; wait; or pay a nonrefundable abstract reservation fee and wait.
- After waiting, observe the public signal Y, approval information G and any surviving backup-slot capacity. Choose among feasible subsequent actions. Deferring M* is an explicit fallback if no timely/economic launch exists.
- An immediate Vulcan launch is included **only** in the fixed-action counterfactual defining pure EVSI. Its exclusion from the operational option set is a **case assumption**, not a statement of current law.
- Booster-free Vulcan is excluded; the compatibility flag remains false because there is no public feasibility demonstration for M*.
- The original arithmetic reference assumes a backup slot is certainly available. Operational extensions instead vary slots, reservations, integration time and private information contained in approval. Keep these analyses distinct.

## 3. Corrections to the incoming model

1. An unknown revision is **uncertainty over hardware state**, not a physically distinct third motor type. Model a joint distribution over (R_LV,R_M), with historically equivalent or modified as the actual states.
2. A matching revision is an assumed condition for information transfer, not proof of interchangeable motors. Serial lots and operating environments may reduce relevance lambda.
3. Orbital outcome can indirectly update anomaly risk through its likelihood. What is **not** transferred without evidence is an LV mission consequence/compensation CPT directly to M*.
4. The Beta latent probability is **continuous**. The network is not literally wholly discrete: the implementation enumerates discrete states and integrates Beta-polynomial terms using Gauss–Jacobi quadrature to floating-point accuracy. It must not merely substitute the Beta mean.
5. EVSI >= 0 applies to free information with fixed feasible actions and utilities. Net waiting gain may be negative when waiting/approval costs matter.
6. EVSI vanishes if Y is independent of **all utility-relevant uncertain variables**, with actions fixed. Independence of Y from Theta alone is insufficient if Y informs p or revisions.
7. Three functional regimes are **not** three certified hardware revisions. Their scenario probabilities were not estimated from four flights.

## 4. Historical data and posterior inference

Observed public booster counts: (n,k) = (2,0), (2,1), (4,0), (4,1); k is the **reported** anomaly count, not an independently ascertained physical count.

The historical reference assumes perfect detection, conditionally independent and exchangeable booster exposures, and a stationary baseline rate. These are simplified assumptions because individual lot/revision identities are unavailable. In particular, never assert that the 2024 and 2026 fixes were physically identical.

Under independence and complete detection:

~~~text
Uniform prior:   p | D ~ Beta(3,11)
Jeffreys prior:  p | D ~ Beta(2.5,10.5)
~~~

These distributions summarize only the **homogeneous exchangeable submodel**, not actual reliability of a revised GEM 63XL. Four flights of unknown revision/lot do not identify correction effectiveness.

For imperfect historical ascertainment, s_H is in {0.7,1}, false-positive probability zero:

~~~text
P(k_reported | p) = sum_{K>=k_reported} P(K | p,rho)
                    * Binomial(k_reported; K,s_H)
~~~

Multiply the four observed-flight likelihood terms. Never add the 2/4 reported anomaly episodes as independent new evidence over the already included 2/12 booster count.

Atlas-derived heritage is excluded from the principal posterior (weight w=0). Secondary weights w in {0.25,0.5} apply hypothetical likelihood (1-p)^(32w), **conditional** on all 32 Atlas booster exposures being fully observed, physically comparable and correctly classified. That is equivalent to 8 or 16 pseudo-non-anomalies, a large addition relative to 12 Vulcan exposures. The original Atlas historical window ended July 30, 2024, and was not represented as coverage through 2026. Without a defensible ascertainment/exchangeability argument, remove this quantitative heritage inference.

## 5. Functional regime, revisions and information transfer

Functional regime Theta is one of {historical-equivalent, effective correction, ineffective correction}. If hardware revision R is historical, per-booster risk is p in all regimes. For modified revision R:

~~~text
historical-equivalent:    q = p
effective correction:    q = e*p
ineffective correction:  q = p + (1-p)*u
~~~

Reference e=0.10 and u=0. Sensitivity e in {0.05,0.10,0.30}, u in {0,0.05,0.15}. They are mathematical scenario transformations, **not measurements**. Positive u allows an ineffective change to worsen risk. If u=0, historical-equivalent and ineffective regimes are observationally identical, hence separately unidentifiable.

Correction-regime scenario weights: (0.6,0.2,0.2), (0.2,0.6,0.2) and (0.1,0.8,0.1). The continuous map varies the effective-regime weight from zero to one and splits the remainder equally. No probability was learned from Vega-C.

Revision combinations HH, HM, MH, MM, plus an unknown-revision distribution allocating 0.25 to each. Reference MM is **illustrative**, not confirmation of actual modified hardware on both flights.

When revisions match, the joint epistemic mixture is:

~~~text
with probability lambda:    share the same uncertain Theta and p
with probability 1-lambda: independent draws from the same marginal knowledge
~~~

lambda in {0,0.5,1}; the EVSI surface uses eleven grid values. When revisions differ, lambda=0 by this study's conservative convention—not a physical law. Under unknown revisions, Y may inform both R_LV and, via joint pair dependence, R_M. Zero-transfer checks use specified known revision pairs.

## 6. Booster plate model, severity, consequences and public signal

Each flight carries n solid boosters. With mixture weight (1-rho), anomaly counts are conditionally binomial given q. With weight rho, all booster anomaly indicators share a single Bernoulli(q) draw. Hence:

~~~text
P(K=k | q,rho) =
 (1-rho)*Binomial(k;n,q)
 + rho*[(1-q)*1{k=0} + q*1{k=n}]
~~~

The conditional pairwise anomaly correlation is rho, while individual marginals remain q. This is an **extreme common-shock stress scenario**, not an inferred nozzle failure mechanism. Shared shocks are independent between flights. Apply the same likelihood family to historical data and future predictions when varying rho.

Conditional on anomaly count K=k, the chance of at least one severe event is 1-(1-h)^k; assumed h_LV=0.20 and h_M=0.25. LV and M* consequences are modeled with different *assumed* CPTs:

| Condition | LV: success / degraded / loss | M*: success / degraded / loss |
| --- | --- | --- |
| K=0 | 0.998 / 0.001 / 0.001 | 0.998 / 0.001 / 0.001 |
| K=1, not severe | 0.985 / 0.010 / 0.005 | 0.970 / 0.020 / 0.010 |
| K=1, severe | 0.750 / 0.150 / 0.100 | 0.550 / 0.200 / 0.250 |
| K>=2 | 0.400 / 0.200 / 0.400 | 0.250 / 0.200 / 0.550 |

**Every numerical consequence probability is an assumption.** Two delivered Vulcan missions with booster anomalies do not calibrate these tables. Baseline failure possibility when K=0 represents other subsystems.

The modeled four-category public signal Y is:

- `inconclusive`: insufficient disclosure, reference probability 1-d with d=0.90;
- `loss_or_degraded_report`: mission delivery degraded/lost and sufficiently disclosed;
- `anomaly_report`: delivery success and at least one disclosed/detected booster anomaly;
- `clean_report`: reported delivery success with no qualifying detected anomaly, **possibly including undetected physical anomalies**.

Reference per-booster detection sensitivity s=0.90, yielding P(any detected | K)=1-(1-s)^K, with false positives zero. Sensitivities s,d in {0.5,0.9,1}. Missingness is independent in the reference. The extension tests state-dependent anomaly disclosure d_anomaly in {0.3,0.6,0.9} whenever K>0. A clean report is **not physical K=0**.

## 7. Approval, feasibility and cost arithmetic

Approval G is conditional on public signal Y in the original decision model, with hypothetical:

~~~text
P(G=approved | clean, anomaly, loss/degraded, inconclusive)
  = (0.90,0.30,0.05,0.40)
~~~

Test gates (0,0,0,0), (0.5,0.1,0,0.1), and (1,1,1,1). In the old reference G conveyed no additional physical state information beyond Y; the later extension includes dependence on latent state (section 12). None of these probabilities describe actual Space Force rules.

All costs are constant-2026 USD million, ignoring financial discounting in the core. Common costs cancel:

| Parameter | Reference | Sensitivity |
| --- | ---: | --- |
| Alternative-provider incremental premium | 30 | 10, 30, 100 |
| Alternative mission-loss probability | 0.005 | 0.001, 0.005, 0.02 |
| Alternative degradation probability | 0.003 | 0.001, 0.003, 0.01 |
| Extra cost to reallocate later | 5 | 0, 5, 20 |
| Incremental waiting C_D | 10 | 0–100 on map |
| Degradation loss fraction d | 0.25 | 0.1, 0.25, 0.5 |
| Total loss L | 1,000 | 250–2,000 |

C_D is an incremental aggregated cost relative to original launch timing; it does **not** include the backup-provider premium again. Optional calendar sensitivities use 7, 45 or 715 extra days, a cost per day of 0, 0.1 or 0.5 million, plus a 20-million window penalty if exceeding December 15, 2026. The 715-day value is from a **different historical case**, only a schedule stress, not a Vulcan prediction. Y and authorization information must arrive *before* follow-up decision D1; waiting does not magically correct actual hardware.

~~~text
C_alt   = premium + L*(P_loss_alt + d*P_degraded_alt)
C_V(y)  = L*(P_loss_M_given_y + d*P_degraded_M_given_y)
C_wait  = C_D + sum_y P(y) *
          [ g_y * min(C_V(y), C_alt+extra)
           +(1-g_y) * (C_alt+extra) ]
Net waiting gain = C_alt - C_wait
~~~

Pure EVSI with **free information and unchanged counterfactual actions**:

~~~text
EVSI = min(E[C_V],C_alt) - sum_y P(y)*min(C_V(y),C_alt)
~~~

Net waiting gain is **not** EVSI. The value of the current decision restriction is C_alt - min(E[C_V],C_alt), only for this reduced action set.

## 8. Integration and mathematical/software verification

The reference uses **24-point Gauss–Jacobi quadrature** for Beta integrals. Historical likelihood degree <=12 and joint LV/M degree <=10 yield an integrand of degree <=22; a 24-point quadrature integrates polynomials up to degree 47 exactly in exact arithmetic, and only machine-precision rounding remains. Probability q is an affine function of p under the studied scenarios.

Test quadrature order 48, closed-form analytic Beta posterior and booster Bernoulli enumeration.

pgmpy 1.1.2 checks joint/marginal/posterior inference with VariableElimination on discrete latent mixture quadrature nodes. That validates computational inference **given the same CPTs**, not a second independent physical model.

Regression checks include the original numerical example 0.6391924983790723; Beta posterior means 3/14 and 2.5/13; analytic Beta-binomial clean probability; mass normalization; dependence/marginals; zero transfer; EVSI >= 0 and EVSI <= EVPI; an entirely inconclusive Y contributes no pure EVSI; zero authorization implies no benefit to waiting; waiting-cost monotonicity; separate configuration feasibility; input validation.

## 9. Output and structural non-identification

1. Primary C_D by L structural envelope over **360 discrete scenarios**, with the two-prior map retained as a narrower diagnostic.
2. Pure EVSI surface over correction-regime weight and information-transfer relevance.
3. Policy indexed by Y and G, including rare loss/inconclusive outcomes.
4. Full structural grid without unjustified probability-weighted averaging, with Atlas heritage separate.
5. Classify each point by the min/max net waiting benefit across the **specified 360 scenarios**: wait in all, reallocate in all, disagreement, or within USD 0.01 million of the zero threshold. No universal robustness claim over additional physics/operational controls outside the cross-product.

## 10. Prospective registry plan — dated snapshot

| By (October 2026) | Historical work package |
| --- | --- |
| 09 Oct | Specification, model core and illustrative results executed |
| 12 Oct | Review physical assumptions, mission interpretation, public observations and sensitivity dimensions |
| 14 Oct | Audit sources/scenarios without incorporating later outcomes |
| 16 Oct | Candidate freeze, checksums, clean rerun |
| 17 Oct | Public release and external registration verification before flight |

At the original cutoff the destination repository/author identity remained unresolved. Never invent a DOI, public object hash or verified timestamp. A local commit and checksum are insufficient evidence of independent public pre-registration. If the flight advances ahead of registration, abandon the ex-ante label for that flight.

Following a real freeze, updates belong in separate dated files/releases referencing the original hash. The plan was to record a preliminary Y interpretation at T+72 hours and one primary T+14-day classification. Insufficient evidence at the cutoff is inconclusive, not unreported proof of success. Hypothetical decisions cannot use information published after their own decision times.

## 11. Methodological references

- Heath et al., *Simulating Study Data to Support Expected Value of Sample Information Calculations: A Tutorial*, DOI 10.1177/0272989X211026292, https://pmc.ncbi.nlm.nih.gov/articles/PMC8793320/
- Ibrahim & Chen, *Power prior distributions for regression models*, Statistical Science (2000), DOI 10.1214/ss/1009212673, https://doi.org/10.1214/ss/1009212673
- pgmpy VariableElimination: https://pgmpy.org/api/generated/inference/pgmpy.inference.VariableElimination.html
- Zenodo enable repository: https://help.zenodo.org/docs/github/enable-repository/
- Zenodo GitHub archive: https://help.zenodo.org/docs/github/archive-software/github-upload/

During the October 9 session, Consensus usage quota had been reached; **no source claim** was attributed to an unperformed search. Wolfram checked the numerical example and Beta moments; recorded in `evidence/wolfram-verification.json`.

## 12. Response to the October 9 independent audit

### Partially unidentifiable historical hardware

The field `history_risk_multipliers` sets flight-specific q_i=m_i*p, with m vectors (1,1,1,1), (1,1,0.5,0.5), or (0.5,0.5,1,1). These are contrast assumptions, **not identified hardware lots**. Per-flight historical detection vectors are (1,1,1,1) or (0.7,1,0.7,1). Closed-form conjugate Beta updates remain exact only in the original simpler submodel. Atlas remains excluded from the primary history.

### Approval with reduced private risk information

Let H be the integrated latent mixture state, including revisions and shared risk when applicable. Define a target physical-consequence severity score t(H) = P(loss|H,M*) + 0.25 P(degraded|H,M*). Set:

~~~text
P(G=1 | Y,H) = g_Y * [1-a*t(H)],  a in {0,0.5,1}
P(Y,G,Z) = sum_H P(H)*P(Y|H)*P(G|Y,H)*P(Z|H)
~~~

Decisions depend on P(Z|Y,G), even when approval is denied. The model does **not** condition G on a future realized outcome. It is a reduced proxy for association between confidential information and approval, not a telemetry definition or Space Systems Command regulation. For a>0, the *marginal probability of approval also changes*; the estimated cost difference conflates informational selection with less availability and **cannot** be presented as pure EVSI of private telemetry.

Even at lambda=0, latent M* uncertainty remains in the informative-approval extension, making G potentially informative about the target independent of LV transfer. The model does not exhaust the possible structures of G conditioned on Y, Theta and revision.

### Opportunities and timing

The operational experiment enumerates **432 scenarios**: three values of private-information strength a; LV date October 29 or 31 or December 1, 2026; integration 30/90 days; approval-processing wait 0/30 days; backup slot chance 0/0.5/1; reservation false/true; old/planning window. No probability weights are assigned across scenario combinations.

The principal LV signal is T+14 calendar days after flight; decision date equals signal date plus additional approval processing time. Integration conservatively starts then. The same lead time is used for either provider in this simplified grid. If decision date plus integration exceeds window end, both providers are treated as unavailable; do not represent a late mission as timely.

Incremental calendar opportunity cost = USD 0.1 million times days from window start to readiness (minimum zero). It applies even to an eventual deferral; the separate deferral penalty is incremental to it.

Abstract reservation costs USD 10 million in every branch and guarantees a backup slot only within the idealized contract scenario; not delivery compatibility, integration or authorization. `reserved_slot` is configurable. `alternative_now=False` can disable immediate backup availability, and deferral-now is implemented. Hypothetical fallback cost is USD 100 million, without asserting physical payload loss. Actual certification, capacity and contracts are not validated.

Planning window now January 15–March 15, 2027, preserving M*'s hypothetical mass/orbit; the old November 15–December 15, 2026 window remains separate stress. Original fixed numerical reference still has C_D=10 and **no actual operational calendar**; it must not be presented as a result of the 2027 expansion.

### Severity and observation controls

For M* when K>=2, P(loss) in {0.1,0.3,0.55,0.8}, P(degraded)=0.2, and P(success)=0.8−P(loss). Disclosure for K>0 is varied separately. These are 12 one-factor controls, **not** fully crossed with the 432 operational or 360 structural points. Structural underdetermination outside the tested sets remains unresolved.

### Factual and financial evidence boundaries

Northrop 2026 Q1 reported USD 71 million in unfavorable estimate-at-completion impact related to evaluation/implementation of corrective actions; Q2 included USD 91 million largely tied to projected materials quantity and cost. The USD 162 million accounting total must **not** be labeled direct investigation cash cost and does not enter decision utilities. Source: https://www.sec.gov/Archives/edgar/data/1133421/000113342126000034/noc-20260630.htm

The separate Atlas extension documented nine additional flights and 45 booster exposures in `data/atlas_2025_2026_extension.csv`, excluded from the principal prior. Corrected UTC dates: ViaSat-3 F2 November 14, 2025, Amazon Leo 6 April 28, 2026. The potential 32+45=77 exposure sum does **not** prove 77 physically anomaly-free events or GEM 63/GEM 63XL interchangeability.

The LV-01 date October 29 remained an unconfirmed **secondary-source NET**, not a ULA-approved T0. October 31 and December are alternative stress dates rather than predictions. An actual ex-ante freeze must precede the *real* liftoff.

## 13. Prospective forecast integration

The normative Y endpoint is in `docs/FORECAST_PROTOCOL.md`: exclusive 2027-01-01 00:00 UTC episode expiry; in-window delay preserves the primary; data cutoff is 00:00 UTC at the beginning of the liftoff UTC date +15 days (the full fourteenth day afterward). Only Y's public category receives the main multiclass Brier sum and log-loss score; the physical latent anomaly count K is not scored.

`src/scoring.py` checks internal date/hash consistency but cannot authenticate external publication. The economic action-set and operational extensions remain as described above.

**This entire specification is about assumptions and reproducible computations, not a certified assessment of Vulcan or GEM 63XL flight safety.**
