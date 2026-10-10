# Controlled information-limit experiment

Status: exploratory continuation after earlier minimax results were observed. This protocol is recorded before the new grid is evaluated; it is not a preregistration of earlier findings or a flight forecast.

Base: main 9d1c7d8299ec1793c4aff29729e5100d8ac87d3b. No forecast bytes or original model parameters will be changed.

Question: does reducing uncertainty about baseline anomaly frequency, at a fixed posterior mean, remove decision ambiguity when target consequence CPTs remain partially identified?

Design fixed before computation:
- Reference mean mu=3/14. Precision t in {14,28,70,140,700,infinity}; finite p~Beta(mu*t,(1-mu)*t), infinity means p=mu. This is controlled contraction, NOT additional observed flights, an expected posterior experiment, or EVSI.
- Keep reference regime mixture (0.4 at q=p, 0.6 at q=0.1p), disclosure, detection, LV CPT, target booster count, costs and approval probabilities fixed. Knowing p does not reveal the correction regime.
- Monotone target consequence polytope: P(degraded or loss) and P(loss) nondecreasing from zero anomalies to one mild, one severe and multiple anomalies; zero row fixed at (.998,.001,.001).
- Shrink this polytope by c=(1-r)*c_reference+r*v with r in {1,.75,.5,.25,.1,0}. Reference rows are (.97,.02,.01),(.55,.20,.25),(.25,.20,.55). This is a geometry sensitivity, NOT measured information or a confidence region.
- Enumerate 17 fixed policies (now, or wait with each binary mapping from four signals to Vulcan-if-approved). Oracle uses the same 17 policies. Evaluate deterministic and randomized minimax regret and the interval for optimized wait gain. Do not describe world-specific wait optimization as a single implementable policy.
- Use polytope vertices for maximum regret and maximum wait gain. For minimum wait gain, solve a linear program over convex combinations: a concave waiting-cost maximum may lie in the interior.
- Record every grid cell; no omission based on favorability. Locate the largest r for which now is uniformly optimal by bisection, reporting a bracket and numerical tolerance.

Checks: t=14,r=1 must reproduce monotone regret 10.460237/9.597222; joint at reference CPT must match core model; quadrature orders 24 and 48 agree; r=0 has zero minimax regret; for fixed t regret cannot increase as nested consequence sets shrink. Preserve primary forecasts.

Failure criteria: failure of these checks blocks interpretation. No novelty claim if the result reduces to established finite-action decision theory or identification principles. No empirical claim about actual revised boosters. No monotonicity theorem is assumed for the frequency-contraction axis. No claim that a selected center is the true consequence CPT.
