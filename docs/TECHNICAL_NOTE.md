# Vulcan — A Public-Data Prospective Decision & Forecast Laboratory

**Technical research note · Release candidate · 9 October 2026**  
**Independent work, not endorsed by ULA, Northrop Grumman, NASA, the U.S. Space Force, or Amazon.**  
**Every physically uncalibrated conditional probability in the study is a scenario assumption.**

> **Abstract.** We construct a finite probabilistic decision model to examine whether observing an upcoming commercial rocket launch could have economic value for a hypothetical planner of a later, sensitive orbital mission. The study uses publicly reported booster anomalies, alternative Beta priors, latent technical-effect regimes, uncertain hardware revisions, a flight-level common-cause stress parameter, explicit missingness/detection, mission-dependent outcome conditional tables, and authorization and calendar gates. The main result is a scenario-dependent boundary on the incremental cost of waiting; we do not estimate actual launch failure probabilities. We additionally prepare for registration a model-implied four-category public reporting forecast for the upcoming flight, together with fixed strictly proper scoring rules and a postevent publication protocol. This is a release candidate, not yet a publicly timestamped forecast.

## 1. Decision context, intended use and scope

A hypothetical program manager M* must allocate a communication payload after a launch vehicle (LV) series has publicly reported booster anomalies. The manager may immediately commit to an abstract alternate provider or defer and observe the next six-solid-booster Vulcan mission, Amazon Leo LV-01, before reassessing an assumed later Vulcan opportunity. This is a **decision experiment**, not an engineering flight-readiness assessment. We define the reference payload as 3,000 kg to direct geosynchronous orbit (GEO); planning window from 2027-01-15 to 2027-03-15, inclusive; the former 2026-11-15 to 2026-12-15 window is retained as a stress case. We intentionally do not identify an actual contracted mission matching these characteristics. The availability, costs, integration compatibility and late commitment opportunity for an alternate launcher are deliberately hypothetical. No permission to fly unapproved hardware follows from any model probability.

The user-facing decision is narrow: *under which combinations of loss consequence L, alternate provider premium, delay cost C_D, Bayesian hypotheses and observed public reports would waiting be economically preferable?* The operational meaning depends on approval by the relevant regulator and the calendar. A second, statistically distinct question is: *which public reporting outcome Y is predicted before the future flight?* The two questions must not be conflated. A valuable signal is not automatically a good reason to delay, because delaying imposes costs and may not preserve the alternate option.

**Intended users:** scientists, operations research analysts and prospective employers reviewing a reproducible educational risk/decision case. **Explicit exclusions:** certification, flight safety acceptance, defect root-cause analysis, actual cost estimates for government decisions and physical risk estimation for the Vulcan. The public information set is insufficient for those tasks. Detailed upstream risk-fault-tree and trajectory/propulsion dynamics are not included.

## 2. Public flight observations and limits of the evidence

The reference observational table in `data/vulcan_flights.csv` lists four flights by booster exposure counts and reported anomalies: (2,0), (2,1), (4,0), (4,1). This yields twelve booster-flight exposures and two publicly reported booster anomalies. The word **reported** matters: absence of a public statement cannot establish that every motor had no physical anomaly. No flight telemetry, borescope investigation, hardware material traceability or private inspection record has been obtained. All flight-level reports are situated with sourced statements; `docs/SOURCE_REGISTER.md` documents the main contemporaneous public references, and `evidence/` holds prior archive attempts subject to their success status.

The nine Atlas V GEM 63 subset launches ending 2024-07-30 provide 32 previous booster exposures in an older, related but not identical hardware family. Their perfect-observation equivalence to Vulcan GEM 63XL is unsupported, so the central fit sets prior borrowing w=0. Hypothetical power-prior analyses with w=.25/.5 add 8/16 pseudonon-anomalies **only if** perfect reporting and comparability are assumed. The independent audit also assembled an extension to 2025–26, but did not automatically pool it. Vega-C serves solely as an illustration of the long tail in corrective-action return-to-flight delays, not a probabilistic estimator for the Vulcan.

The Space Systems Command's GPS III-8 reassignment is an observed precedent that procurement alternatives can sometimes be exercised, but the financial premium, technical feasibility and lead time for the fictional M* are not implied by the precedent. Northrop's disclosed unfavorable estimate-at-completion adjustments of US$71m and US$91m in 2026 provide business context but do not belong in mission-level net utility. Mixing producer accounting adjustments with a purchaser's launch decision cost would double-count or commit a causal fallacy.

The upcoming LV-01 target is described by public launch aggregators as Vulcan VC6L, six strap-ons, an optimized LEO Centaur. The launch calendar changed during 2026; a listing that shows October cannot verify an exact 29 October launch. **Prospectivity requires release ahead of the earliest possible outcome**, not confidence in any NET date.

## 3. Uncertainty architecture: aleatory, epistemic, and structural

We distinguish **aleatory** variability conditional on a specified model from **epistemic** uncertainty about whether that model and its parameters describe reality. The individual booster event indicator A_i is aleatory only after its risk q, flight context and technical regime are stipulated. Uncertainty over the historical base event probability p is represented by a Beta distribution. Uncertainty over whether a hardware correction is genuinely effective and over which version is installed is epistemic and not resolved by assuming an arbitrary prior distribution.

A discrete regime Θ has three scenario labels: `historical_equivalent`, `effective_correction`, `ineffective_correction`. It is not a manufacturer certification state. The modified booster probability under the effective case is q=e p; under the ineffective/worsening case it is q=p+(1-p)u. For historical hardware q=p in all three regimes. Reference values are e=.10, u=0, and Θ weights (.20,.60,.20). When u=0, historical-equivalent and ineffective regimes are observationally identical; they are distinct narrative states but *not identified by data*. The joint hardware version pair for LV-01 and M* is represented as HH, HM, MH, MM, or mixtures. The reference MM is an illustration: actual revisions remain unverified.

The cross-flight transfer relevance λ mixes a joint common-hypothesis posterior with independent copies of the same marginal posterior for a matched revision. It governs **information dependence** between predicted public LV-01 observations and later mission risk. It is not a measured probability of equivalent hardware or a guaranteed transfer of a mission consequence CPT. If revisions differ, the reference explicitly zeroes λ. The target's consequence tables remain mission-dependent. The unconditional LV-01 forecast does *not* depend on λ: it is a marginal prediction for the first flight.

**Structural uncertainty is not exhausted by distributions over Θ or p.** Physical common-cause mechanism, regulator-only evidence, late slot scarcity, reporting selection, consequence calibration, and integration feasibility are alternatives not probabilistically averaged. A useful risk engineer is expected to identify what lies outside a given probabilistic graph. Different complete structures may support opposite decisions; the model produces an envelope instead of inventing weights to obtain one averaged answer.

## 4. Learning from four flights

The simplest reference treats the 12 reported booster states as conditionally independent Bernoulli observations from a single stationary event probability p, with perfect public observability. If a Beta(a,b) prior is assumed and k=2 anomalies are reported out of n=12, the reference posterior is Beta(a+2,b+10). A uniform Beta(1,1) prior yields Beta(3,11); Jeffreys Beta(.5,.5) yields Beta(2.5,10.5). **This posterior is conditional on assumptions, and not a literal reliability estimate for redesigned GEM 63XL hardware.**

Other scenarios use probability of detection less than one and nonzero within-flight dependence, so the posterior is not generally Beta. For reported count r in a flight of n boosters, detection sensitivity s_H and latent anomaly count K, the flight likelihood is

\[
\Pr(R=r\mid p,\rho,s_H)=\sum_{k=r}^n\Pr(K=k\mid p,\rho){k\choose r}s_H^r(1-s_H)^{k-r}.
\]

The model multiplies likelihoods for the four flight reports, then integrates over a prior using Gauss–Jacobi quadrature. Historical counts are not added twice or treated as independent evidence after being aggregated. Posterior uncertainty is retained by quadrature over p instead of substituting posterior mean. The exactness claim is **algebraic for the implemented polynomial likelihoods**, up to floating-point computation and integration order, not validity of the physical assumptions.

## 5. Flight-level dependence and common-cause stress

The physical number of anomalous boosters in a flight with n strap-ons is represented by an all-or-none contamination of the independent binomial count distribution:

\[
\Pr(K=k\mid q,\rho)=(1-\rho){n\choose k}q^k(1-q)^{n-k}
  +\rho\left[(1-q)\mathbf{1}_{k=0}+q\mathbf{1}_{k=n}\right].
\]

Each booster has marginal anomaly chance q. For distinct boosters in the same flight, conditional-on-q pair correlation is ρ. The all-or-none component is an **abstract common-cause stress test**, not an assertion that nozzle failures share the real-world mechanism of a simultaneous all-six event. It accentuates tails and probes fragility; it cannot substitute for a fault tree identifying manufacturing defects, loads, ignition, stage control, separation and guidance contingencies. All uncertainty scenarios involving ρ must be displayed alongside their baseline, never as inferred engineering causation.

A more physically credible successor should construct a minimal event tree branching on anomaly detection, separation, burn-phase thrust deficit, vehicle guidance margin, intended orbit and regulatory actions. Such a tree must be reviewed by an appropriate engineering specialist, with source provenance for each conditional probability or an explicitly elicited expert range. Without that step, the present mission outcome CPTs are placeholders.

## 6. Mission outcomes and public observation

After K booster anomalies, a severity node assigns probability 1−(1−h)^K that at least one event is severe. Separate mission-outcome tables map severity and K to success/degraded/loss for LV-01 and the hypothetical GEO-bound M*. The two tables are intentionally different because orbital energy, guidance margins, upper-stage operations and the definition of success differ. In the current model K=0 still admits small degraded/loss outcome mass (.001 each) as an abstract risk from other systems. The model does not claim those probabilities are physically calibrated.

The *public observation* Y has four mutually exclusive categories: `clean_report`, `anomaly_report`, `loss_or_degraded_report`, `inconclusive`. Its availability is controlled by disclosure probability d, reporting detection sensitivity s and a scenario false-positive flag. Precedence is clear: absent adequate disclosure gives inconclusive; a known degraded/lost outcome takes priority over booster anomalies; among successful missions, an identified booster anomaly gives `anomaly_report`; otherwise an adequately publicly documented success gives `clean_report`. The distinction between physical A and public Y is essential: **Y=clean does not entail K=0.**

These signal probabilities are a **model of evidence acquisition**. In reality, disclosure may depend on failure severity or on investigation, so missing-at-random is a strong assumption. The forecast protocol makes failure to resolve conflicting primary sources a separate inconclusive case; the published Y categories should never be silently reinterpreted to improve a score.

The additional booster-count distribution of K=0..6 is intentionally **latent**. A disclosed number of anomalies would require a different measurement likelihood, possibly with unreported events and more than one physical defect per booster. The reference `hypothetical_disclosed_count_pmf` is provided as a diagnostic exercise and is not independently evaluated by default. In this sense a binary public anomaly disclosure score is technically more defensible than treating a six-way physical defect count as directly observed.

## 7. Decisions, approval and expected value of information

Let L represent total monetary equivalent of mission loss, already including the hypothetical payload book value, and d_L a fractional consequence of degradation. Expected losses for using Vulcan and an alternate provider are

\[
 C_V(y)=L\big(\Pr(\mathrm{loss}_M\mid Y=y)+d_L\Pr(\mathrm{degraded}_M\mid Y=y)\big),
\]
\[
 C_A=P_A+L\big(p_{A,\mathrm{loss}}+d_Lp_{A,\mathrm{degraded}}\big).
\]

The optional approval gate G has scenario probabilities g_y=Pr(G=approved|Y=y). This only models an **assumption that approval contains no additional private technical evidence conditional on Y**. In practice approval by the relevant agency may depend on nonpublic telemetry; the integrated extension lets G depend on a latent target-risk score and updates P(Z|Y,G), retaining target uncertainty even at zero LV transfer. This reduced-form association is not a calibrated regulator model. The post-observation planner can use Vulcan only when G is approved; otherwise the fallback alternative is assumed available at premium H above C_A.

\[
 C_{\rm wait}=C_D+\sum_y p_y\left[g_y\min(C_V(y),C_A+H)
           +(1-g_y)(C_A+H)\right].
\]

Pure **EVSI** is separately defined under an identical, counterfactual fixed feasible action set with free observation: `min(E[C_V],C_A) - Σ_y p_y min(C_V(y),C_A)`. It is nonnegative under valid probabilities because more freely available information cannot reduce optimal expected utility. It is **not** equivalent to the net value of waiting with calendar, authorization, and fallback costs. The latter, `C_A-C_wait`, can be negative. The baseline formula assumes a certain fallback; `src/operations.py` separately enumerates unavailable slots, reservation, integration, informative G and deferral. These extensions are scenario sensitivities and may overturn the baseline preference. Similarly, the refusal of a real authorization cannot be evaded by expected utility.

## 8. Reference result and reversals

At the reference assumptions (L=US$1,000m, d_L=.25, alternate premium US$30m, alternate loss chance .005, degraded chance .003, late fallback extra US$5m, C_D=US$10m, G probabilities [.90,.30,.05,.40]), original arithmetic and an independent adaptive-integration implementation agree: C_A=US$35.750m, C_wait=US$44.470999m, net wait gain −US$8.720999m, pure EVSI US$3.989851m. Thus the reference waiting-cost break-even threshold is `C_A - (C_wait-C_D)` = **US$1.279001m**. A sensitivity result at exactly C_D=10 is **359/360** structural scenarios preferring reallocate now and **1/360** preferring wait. This ratio describes a grid of selected models, not an estimated likelihood that reallocation is correct.

The structural threshold minimum/maximum over these 360 specified cases is **−US$5m to +US$10.744m**. No universal positive waiting region was identified in the previous all-structural map. At the reference L=US$1000m and C_D=US$10m, the worst-case regret of the reference choice (reallocate) over this discrete grid is US$0.744m, versus US$15m for always waiting. The word worst-case is restricted to those 360 scenarios and those financial assumptions; it is not a robust bound against all physically possible outcomes or erroneous source records.

A *one-at-a-time* sensitivity over the supplied controls identifies the largest numerical variation in break-even among the alternate premium (US$10m to US$100m), alternate modeled mission-loss probability (.001 to .02), and cost of late switching (US$0m to US$20m). These variations were not elicited by experts and do not prove those quantities dominate all scientifically plausible sensitivities. Target severity, technical correction efficacy, detection and disclosure matter, but comparisons depend strongly on assigned ranges. In particular, a more effective correction can increase the relevance of observing LV-01 for the chosen binary decision while other assumptions move in the opposite direction.

## 9. Candidate outcome forecast (episode 1)

The baseline forecasting distribution is not the value of any single physical parameter. It is the Y marginal obtained by combining the historical posterior, scenario Θ, hardware revisions, six-booster count distribution, severity and mission outcome table, and observation model. In the **reference MM scenario**, the four probabilities are:

| Y outcome | P(Y) | Meaning and major caveat |
|---|---:|---|
| clean_report | .59736329 | Success with no booster anomaly publicly detected in sufficient report; not K=0 |
| anomaly_report | .20721669 | Mission-success and booster anomaly reported |
| loss_or_degraded_report | .09542003 | Reported mission degradation/loss from any modeled cause |
| inconclusive | .10000000 | No adequate disclosure per the scenario missingness model |

The associated reference latent K distribution is `[0.645851, 0.200295, 0.093078, 0.042357, 0.014601, 0.003406, 0.000413]` for K=0,1,...,6. It is neither a statement about what ULA knows nor a physically verified anomaly count. Five model-implied forecast files are generated prospectively, with the above reference explicitly predesignated as the primary one. Revision-uncertain sensitivity changes Y to approximately `[.445667,.296435,.157898,.100000]`, demonstrating just how strongly a seemingly plausible choice of hardware prior changes the scoreable prediction. No sensitivity series may be chosen *after* Y is learned to replace the primary reference.

**Logarithmic loss** is `−ln(p_observed)`. **Multiclass Brier sum** is Σ_i(p_i−δ_i,j)^2, with a 0–2 range. Smaller is better. We score the outcome observed in public reporting **at T+14 UTC calendar days after actual liftoff**, regardless of whether the score is good or bad. A preliminary T+72h source digest may help trace the evidence but does not revise the submitted forecast. If LV-01 does not fly, the outcome is `NOT_LAUNCHED`, which receives no score because this study made a flight-*conditional* prediction. Conditional-on-flight scoring prevents a schedule slip from being mislabeled as a clean, failed or inconclusive mission. The integrated protocol preserves the primary forecast for schedule slips within its fixed validity ending 2027-01-01 UTC; beyond expiry a new prospective episode is required.

A single scored flight tests **falsifiability and prospective honesty**, not frequentist calibration or discriminative performance. Skill relative to climatology requires an appropriate reference distribution and many prospective episodes; no genuine baseline is available from four inconsistently observable flights. The first score is published for transparency, not marketed as empirical safety accuracy. Future forecast episodes must predeclare whether the same target, measurement model and outcome priority apply; otherwise, they are separate series.

## 10. Verification, validation, and credibility assessment

**Verification:** the computational algorithm uses explicit finite mixture summation and Gauss–Jacobi quadrature. Checks include normalization, analytical Beta-binomial moments, four-category likelihood, invariance of LV-01 marginal to target-only hardware, null transfer, expected-utility identities, EVSI≥0, discount/cost monotonicity, detection and missingness handling, and comparison with a pgmpy Bayesian-network representation of identical CPTs. The independent numerical check used adaptive integration rather than the original quadrature. This verifies computational consistency, **not** physical predictive validity.

**Validation:** prior flight facts are sparse, technical revisions hidden, detection uncertain and consequence tables not empirically calibrated. The next flight gives a useful prospective test of the **public reporting forecast** and can identify surprising observations and modeling error; no one observation validates physical or probability calibration. Empirical validation requires sufficient independently defined observations, properly specified benchmarks and reconciliation of missing/public reports with verified hardware outcomes. Retrodictions of previous launch-allocation decisions can provide illustrations of time-available evidence but cannot by themselves identify what decision would have been globally optimal.

**NASA technical context:** NASA-STD-7009B, currently active, provides an institutional standard for modeling and simulation credibility, and NASA-HDBK-7009B is its companion implementation handbook. This repository adopts a subset of their vocabulary: intended-use statement, uncertainty qualification, provenance, verification and model discrepancy. It **does not** imply formal compliance with NASA requirements, delegated Technical Authority approval, mission assurance certification or a NASA contracting relationship. The explicit credibility gap is lack of direct physical model validation.

Reproducibility must be considered separately from registration. A clean environment can check all tests and regenerated forecasts against the fixed release artifact. GitHub Actions is configured to install pinned dependencies, run tests (including pgmpy) and recompute. The integrated local suite, including pgmpy, has now been run successfully; external CI remains unexecuted and is not claimed. A local Git commit and cryptographic hashes establish integrity of local content but cannot alone prove that the content existed publicly before launch.

## 11. Foresight, postflight learning and alternatives to overclaim

A longer program can predeclare a series of flight-conditional public events with identical rules, then publish proper scores after fixed cutoffs. Each target's information set is frozen as-of a documented timestamp and any new model version receives a new registration; no analysis is permitted to import future public disclosures into an earlier prediction. Physical failure counts are marked unknown unless supported by source-specific inspection or official root-cause disclosures. Scores cannot be rescued after an unfavorable outcome by changing the categorization.

A **retrodiction** uses a chronological data room that reconstructs what was publicly available at a historical decision date, with dates for each source and its public availability. The decisions around Vega-C return-to-flight, GPS III-8 reassignment and others are candidate demonstrations, but the actual decision makers had private commercial, safety and engineering information. Agreement with observed decisions is not proof the study is causally correct; disagreement is not proof they were wrong.

A future reusable software library should extract base-rate learning by hardware revision and lot, posterior updates, observation likelihoods, common-cause mechanisms, authorization information and a calendar-gated value of information. Two useful next technical milestones are **EVPPI** (expected value of partial perfect information for important uncertain inputs) and **hierarchical pooling across revisions/lots**. Both require care: EVPPI for structural uncertainty is ill-defined without a legitimate joint measure, while hierarchical pooling without actual lot labels can produce fictitious precision. An interactive UI is less valuable than those checks and is deliberately postponed.

External review should seek narrow falsification questions, not endorsement: whether an all-or-none ρ is a defensible sensitivity device, whether the decision timeline leaks future information, and which mission event-tree branch most materially undermines the outcome CPTs. All feedback must be logged in the open error register, distinguishing resolved implementation bugs from open empirical unknowns.

## 12. Limitations, release criteria and conclusion

The present work lacks manufacturer reliability datasets, independent measurement of anomaly observability, transfer validation between revisions, physical consequence calibration, a certified candidate mission/alternative, regulator-only data, feasible integration timing, and validated late switching cost. These limitations are *not* repaired by deeper mathematics or a polished dashboard. The project is not evidence that any actual rocket is safe or unsafe. It is evidence of a transparent method for examining what uncertainty might matter to a decision **under stated, reproducible assumptions**.

Scientific publication should be conditional on a clean build, verification of the forecast file's SHA256 within a public versioned GitHub release, a confirmed external timestamp and an accessible Zenodo version DOI. After publication, the forecast and this protocol must be immutable as a historical reference. Subsequent improvements and measured outcomes are new dated releases. As of this candidate, neither release nor DOI has been observed, so the statement "prospectively registered" is **not yet warranted**.

The central scientific contribution is a controlled separation: a model can contain internally consistent Bayesian inference, and information can have positive counterfactual EVSI, while the economically rational feasible action remains reallocation and real reliability is unresolved. The value of publication is not an asserted numerical accuracy; it is a publicly testable, reproducible, and appropriately modest commitment to a forecast and a decision rule in advance.

---

### Reproducibility pointers

`SPEC.md` defines all states and CPTs. `src/model.py` implements the decision model; `src/prospective.py` produces the observation and count marginals; `build_forecast.py` writes the five prospective candidates; `score_episode.py` scores a future evidence record without altering the forecast; `make_decision_brief.py` generates threshold and regret diagnostics; `check_candidate.py` checks key values. `docs/FORECAST_PROTOCOL.md` is normative for endpoint coding; `docs/SOURCE_REGISTER.md` records source limits; `.github/workflows/ci.yml` declares the intended clean CI verification job.

### Selected citations (all URLs free of marketing parameters)

1. NASA-STD-7009B, *Standard for Models and Simulations*, 5 March 2024. https://standards.nasa.gov/standard/NASA/NASA-STD-7009
2. NASA-HDBK-7009B, *Implementation Guide for NASA-STD-7009B*, 3 February 2026. https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009
3. Gneiting, T. & Raftery, A., *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 102(477), 359–378 (2007). https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf
4. Heath, A., et al., *Simulating Study Data to Support Expected Value of Sample Information Calculations*, https://pmc.ncbi.nlm.nih.gov/articles/PMC8793320/
5. Chen, M.-H. & Ibrahim, J., *Power prior distributions for regression models*, *Statistical Science* 15, 46–60 (2000). https://doi.org/10.1214/ss/1009212673
6. Official source and historical observation register: `docs/SOURCE_REGISTER.md` and archived evidence manifest.

## Integration addendum: authoritative scope

`SPEC.md` sections 12–13 and `FORECAST_PROTOCOL.md` supersede earlier baseline-only
language in this note. The original 360-case envelope is reproduced exactly;
432 operational scenarios and 12 one-factor physical/observation controls are separate
experiments, not a single all-assumptions envelope. The US$1.279m break-even and regret
figures use the original fixed-slot/G|Y reference, not the new planning window.
The physical-history Beta is only a stationary exchangeability submodel, not an
estimated corrected-motor rate. New history multipliers and per-flight detection are
hypotheses, not inferred revisions. Two Atlas extension UTC dates were corrected:
ViaSat-3 F2 2025-11-14 and Amazon Leo 6 2026-04-28; original attachments retained.

The scoring cutoff is exactly the start of UTC liftoff-date+15 days, exclusive.
Late publication of a score is permitted with evidence provably available before
that cutoff. Registration syntax and hashes are checked offline; authenticity of
public timestamps requires separate independent inspection. Every distribution here
remains an unpublished candidate, not a scientifically calibrated safety forecast.
