# Model specification — English technical reader guide

This is an **English explanatory guide** to the baseline model described in [the original working specification](../../SPEC.md). It is not a newly registered protocol, a rewrite of the frozen forecast, a certified safety assessment, or a complete substitute for all original mathematical derivations. The original file and recorded outputs remain the provenance references.

## 1. Objective and decision alternatives

The model asks whether the hypothetical economic gain from a publicly observed Vulcan mission can justify deferring a later procurement decision. A modeled decision maker has a hypothetical 3,000 kg communication satellite, an illustrative direct geosynchronous delivery objective, a January–March 2027 planning window, and abstract alternative launch capacity. None of these is a verified payload manifest, contract, or available backup slot.

Actions at the initial stage include immediate reallocation, waiting, and a modeled reservation-plus-wait strategy. After observing the publicly reported flight signal and modeled authorization/slot conditions, an admissible action is selected. Delaying the target mission is an explicit fallback. A Vulcan no-booster case is not assumed feasible for the target payload.

The original fixed-slot reference is separate from later calendar/availability extensions. Financial values are hypothetical 2026 US-dollar millions, not actual ULA, Space Force, or commercial contract figures.

## 2. Historical observations and posterior risk

The input history uses four reported Vulcan booster exposure/count pairs:

```text
(n,k) = (2,0), (2,1), (4,0), (4,1)
```

Here `n` denotes boosters flown and `k` publicly reported relevant booster anomalies; it does **not** imply that unreported problems were physically absent. With conditionally independent exposures, perfect reporting, exchangeability and a uniform prior:

\[
p\mid D \sim \operatorname{Beta}(3,11).
\]

The illustrative Jeffreys-prior alternative is \(\operatorname{Beta}(2.5,10.5)\). These are **posterior distributions under the reference observation model**, not calibrated risks for corrected GEM 63XL hardware.

Historic detection scenarios allow detection sensitivity below one; external Atlas GEM 63-derived pseudodata are excluded from the principal reference and treated only in a separately qualified sensitivity analysis.

## 3. Revision, correction effectiveness and inter-flight transfer

The latent functional regimes are *historical-equivalent*, *effective correction*, and *ineffective correction*. These are mathematical hypotheses, not verified manufacturer revision classes.

For historical revision, the probability is `p`. For modified revision, the illustrative per-booster probability `q` is

\[
q_\mathrm{equivalent}=p,\qquad
q_\mathrm{effective}=e p,\qquad
q_\mathrm{ineffective}=p+(1-p)u.
\]

The reference uses `e=0.10` and `u=0`, with sensitivity variations. The probabilities assigned to these regimes are scenario weights, not frequencies learned from the four historic flights.

The model distinguishes HH, HM, MH and MM revision pairs, corresponding to original/modified status across observed LV-01 and target M*. A shared-parameter relevance setting \(\lambda\) varies whether their uncertain risks are coupled under a same-revision assumption. Unknown revisions represent uncertainty about true states, not a third physical revision.

## 4. Shared anomalies and consequences

With `n` boosters, underlying per-booster probability `q` and stress-dependence parameter \(\rho\), the counted anomalies follow the reference mixture

\[
P(K=k\mid q,\rho)=(1-\rho)\,\mathrm{Binomial}(k;n,q)
+\rho\{(1-q)\mathbf 1_{k=0}+q\mathbf 1_{k=n}\}.
\]

The correlated term is a deliberately extreme shared-shock stress test. It is **not** a quantified nozzle fault tree or estimated common-cause physics.

Each flight has illustrative conditional-probability tables mapping `K` and severity hypotheses to successful, degraded or lost delivery. The observed next flight (LV-01) and later target (M*) use distinct consequence tables. **Every unmeasured consequence probability is an analyst scenario assumption**. Reported mission survival despite an SRB anomaly cannot identify the exact loss probability for a different payload or mission profile.

## 5. Public observation model

Physical events `K` are not publicly known with certainty. An observation mechanism generates one of four exclusive reports: `clean_report`, `anomaly_report`, `loss_or_degraded_report`, or `inconclusive`. The reference disclosure and detection assumptions are both 0.90, with sensitivity scenarios. An apparently clean public report **does not** establish `K=0`.

The forecast to be scored refers to this public reporting process at a defined T+14-day cutoff, conditional on the eligible launch taking place. The physical anomaly-count distribution is a separate latent quantity and is not assigned a primary score without a defensible physical counting protocol.

## 6. Decision mathematics

Let `L` be a hypothetical total loss consequence (including the modeled payload value), `d` the fraction applied to degradation and `C_D` the incremental waiting cost. Let `C_alt` be the hypothetical alternative-provider expected incremental cost, and `g_y` the chance the Vulcan path is admissible after observing public signal `y`.

The reduced fixed-slot reference calculates

\[
C_\mathrm{alt}=\mathrm{premium}+L[P_\mathrm{loss,alt}+dP_\mathrm{degraded,alt}]
\]

and

\[
C_\mathrm{wait}=C_D+\sum_yP(y)\left[
g_y\min(C_\mathrm{Vulcan}(y),C_\mathrm{alt}+\mathrm{late\ switch\ cost})
+(1-g_y)(C_\mathrm{alt}+\mathrm{late\ switch\ cost})\right].
\]

The **net gain to waiting** is `C_alt - C_wait`, which may be negative. It is **not** the same as pure expected value of sample information (EVSI), where information is free and available actions remain fixed. Positive EVSI does not imply waiting is economically optimal.

The fixed-slot reference gives `C_alt=35.750` and `C_wait=44.471` ($million), hence net waiting gain `−8.721` at `C_D=10`. This is conditional arithmetic, not an actual procurement recommendation. The cross-parameter 360-grid counts are **scenario counts with no probability weights**.

## 7. Numerical verification and unresolved identification

The Python implementation integrates Beta uncertainty with Gauss–Jacobi quadrature and checks the reference against independent sums and pgmpy inferences. Regression tests verify normalizations, analytic reference cases, parameter invariants, monotonicity, proper score definitions and scoring-window consistency.

The [identifiability extension](https://github.com/MedeiroszJoao/Project-Vulcan/pull/2) constructs different target consequence CPTs with the same history likelihood and public-report law yet opposite actions. A calculated simplex-bound interval crosses zero, so a robust preference is unavailable **within that broad specified set**. This result exposes underdetermination; it does not establish a credible mission-level physical risk interval.

Operational extensions model authorization conditioned on latent state, reservation, slot access, integration lead time and alternate planning windows. They are discrete stress scenarios, not measured real-world launch availability.

## 8. References and status

- [Original full specification](../../SPEC.md) (historical source, may include Portuguese)
- [Original technical note](../TECHNICAL_NOTE.md)
- [Prospective protocol: English guide](FORECAST_PROTOCOL.md)
- [Data provenance](../DATA_PROVENANCE.md)
- [Numerical reproducibility](../REPRODUCIBILITY.md)
- [Scientific limitations](../SCIENTIFIC_LIMITATIONS.md)

No result in this document certifies a rocket, a specific booster, a mission, or an operational safety threshold.
