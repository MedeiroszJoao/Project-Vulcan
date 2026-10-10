# Frequency precision versus consequence ambiguity

**Status: MODEL-SPECIFIC RESULT and application of established decision theory. No original theorem or empirical launcher-validation claim.**

The protocol was published in commit `fdcfa78dec39bcec99582ec065f11154c91746cc` before running the new grid. Earlier minimax results and the reference CPT were already known. This is an exploratory continuation, not a retrospective preregistration of those earlier findings.

## Question and design

Can greater precision about anomaly frequency remove ambiguity about a procurement decision when target consequences remain partially identified? We separate two changes: (1) concentrating a Beta distribution around the fixed reference mean 3/14, and (2) contracting a monotone set of target consequence CPTs around the existing reference CPT. The experiment preserves the original public-report model and all five forecast files.

At precision t, p follows Beta(3t/14,11t/14). At t=infinity, p=3/14. This is not a simulation of accumulating actual observations: posterior means do not ordinarily stay fixed across realized samples. It does not compute EVSI, expected regret after an experiment, or a sample-size recommendation. Even at infinite precision the correction regime remains uncertain (0.4 weight at q=p and 0.6 at q=p/10).

Let C be the original monotone consequence polytope. We use C_r=(1-r)c0+r C, centered at the reference CPT c0, with r in [0,1]. Radius r is not a probability, confidence level, fraction of risk removed or fraction of information acquired. No evidence establishes that c0 is the true CPT. All zero-anomaly consequences remain fixed.

## Results

All monetary figures are USD million. The oracle may choose among the same 17 fixed policies as the decision maker, with knowledge of the consequence world. Policy evaluation integrates frequency and regime uncertainty. It is not an oracle observing realized mission outcomes.

| Precision t | Maximum optimized wait gain, r=1 | Deterministic minimax regret, r=1 | Mixed minimax regret, r=1 | Largest radius with now uniformly optimal |
| --- | ---: | ---: | ---: | ---: |
| 14 (reference) | 10.460237 | 10.460237 | 9.597222 | 0.559727111 |
| 28 | 10.223953 | 10.223953 | 9.432024 | 0.602393401 |
| 70 | 10.067274 | 10.067274 | 9.318955 | 0.629594992 |
| 140 | 10.012208 | 10.012208 | 9.278580 | 0.638978205 |
| 700 | 9.967053 | 9.967053 | 9.245231 | 0.646611282 |
| infinity | 9.955606 | 9.955606 | 9.236743 | 0.648538000 |

For the full consequence set (r=1), the minimum optimized wait gain is -15 at every precision examined. Thus ambiguity persists even if this particular baseline rate is known exactly. The mixture regret decreases by about 3.76% between the reference and point-mass cases. This is conditional on that mean, regime model, observation channel, costs and consequence set; it is not a general upper bound on the value of learning frequency.

At r=0.5, reallocate now is uniformly optimal at every examined precision, so minimax regret is zero. Maximum wait gain is -1.060349 at t=14 and -2.997738 at infinite precision. A reduction of ambiguity around a selected reference CPT can therefore eliminate decision ambiguity even when concentrating frequency alone does not. This is a controlled geometry result, not a comparison of the cost effectiveness of actual experiments.

The binding policy at the radius threshold is wait and use Vulcan if approved following clean or inconclusive; otherwise use the alternative. At t=14 its cost at the binding vertex varies as 45.686962781754 - 17.753227581701*r. Equating this with 35.75 yields r=0.559727110804. At infinite precision the cost is 48.838549130459 - 20.181622555588*r, giving r=0.648538000074. At the boundary there is a tie; uniform optimality need not mean uniqueness.

## Elementary propositions, not novelty claims

### Uniform action identification

Let A be a finite set of policies, C a nonempty compact polytope of consequence parameters, and L_a(c) affine in c. A fixed policy a is optimal for every admissible c if and only if max over c in C of [L_a(c)-L_b(c)] <= 0 for every b in A.

Proof: pointwise optimality is precisely the conjunction L_a(c)<=L_b(c). Taking the maximum over c gives the stated equivalent condition. Each contrast is affine, so checking the vertices suffices. This is a direct finite-action robust-optimization characterization, not a new identification theorem.

Equivalently, a has zero maximum regret. Thus nonidentification of a single uniformly optimal policy does not prevent selection by a specified robust criterion. Parameter nonidentification need not imply decision nonidentification.

### Why vertex enumeration suffices for regret

For a fixed mixture w, regret is L_w(c)-min_b L_b(c)=max_b[L_w(c)-L_b(c)], a convex piecewise-affine function. For any convex combination of vertices its value is bounded above by the maximum vertex value. Hence the worst case is attained at a vertex, and mixed minimax regret is a finite linear program.

Optimized waiting cost min_b L_b(c), over the waiting policies, is concave. Its maximum may occur in the interior. We therefore use an epigraph-style LP (maximize a common lower bound on all waiting-policy costs) over convex combinations of vertices for the lower endpoint of wait gain; we do not blindly enumerate vertices for both endpoints.

### Exact radius certificate

For any candidate policy a that is uniformly optimal at r=0, define A_b=L_b(c0)-L_a(c0) and B_bv=[L_b(v)-L_a(v)]-A_b. Uniform optimality on C_r holds exactly when A_b+r B_bv>=0 for every competitor b and vertex v. Consequently the maximal radius is min(1,min_{B_bv<0} A_b/(-B_bv)). This follows from affine dependence and the preceding vertex criterion. If the candidate is not optimal at c0, the certificate does not apply. Ties and zero slopes are handled explicitly.

### Why absence of likelihood dependence is not enough

If data likelihood factors as ell(D|p) and does not depend on c, it supplies no likelihood discrimination among c at a fixed p. This alone does not imply that every Bayesian marginal for c is unchanged: a prior dependence between c and p can transmit learning. Nor does it imply that the optimal action is unidentified. Our experiment expressly holds the admissible consequence set fixed during frequency contraction, rather than treating either assertion as a general theorem.

## Literature comparison and novelty assessment

This is a focused first pass, not an exhaustive novelty search or a proof audit of the cited papers. Exa discovery returned five entries; Parallel Search broadened coverage. Firecrawl retrieved full HTML text for the three papers below, from which the indicated sections were inspected.

| Source and inspected scope | Assumptions compared | Relation and remaining gap |
| --- | --- | --- |
| [Montiel Olea, Qiu, Stoye, arXiv 2312.17623v2](https://arxiv.org/html/2312.17623v2), introduction and Assumption 1 in section 3.3 | Finite-sample Gaussian experiment; convex centrosymmetric parameter space and linear reduced-form/welfare maps for the stated MMR results | Vulcan instead conditions on a fixed frequency distribution and optimizes 17 policies over a bounded CPT polytope. Their specific theorems cannot be transplanted. Randomization and persistent ambiguity are established antecedents. |
| [Aradillas Fernandez et al., arXiv 2408.11621v2](https://arxiv.org/html/2408.11621v2), introduction and framework discussion | Binary treatment choice; multiple priors, including a symmetric two-point reduced-form prior; distinct ex-ante and ex-post regret criteria | Vulcan's current robust criterion fixes one integrated frequency model while varying target consequences. It does not solve their preposterior problem, establish dynamic consistency, or evaluate future data acquisition. |
| [Jackson et al., arXiv 1703.08994v1](https://arxiv.org/html/1703.08994), introduction and VOI definitions | A Bayesian joint model; EVPPI for revealing parameters and EVSI for a specified sampling design | Learning consequence parameters is already within that framework if assigned a joint distribution. Our consequence-set contraction lacks a data likelihood and thus is not an EVSI alternative. |
| [Manski, Identification and Statistical Decision Theory](https://arxiv.org/abs/2204.11318), abstract and publication metadata only | Identification versus finite-sample decision performance, including randomized choice | Supports the conceptual distinction, but detailed theorem-by-theorem comparison remains pending. |

Additional search leads: Troffaes, *Decision making under uncertainty using imprecise probabilities* (2007), and Landes/Destercke, *On the value of varied evidence for imprecise probabilities* (2025). Search also returned arXiv 2607.06570 on rule-specific VOI and envelopes; direct retrieval was unsuccessful here, so no theorem from it is relied upon. These leads remain to be read, not claimed as completed review.

The present numerical result passes computational checks but does not pass an originality claim: its mechanism follows from established partial-identification and finite-action decision principles. The useful output is an explicit conditional boundary and executable experiment. A subsequent research contribution must exceed this application, not merely rename it.

## Verification and next discriminating experiment

The reference kernel reproduces the original joint distribution. The reference full-set regrets reproduce 10.460237 and 9.597222. Quadrature orders 24 and 48 agree within 1e-12 throughout the grid. Nested-set regret checks pass. Bisection radius brackets contain the analytic certificates. Wolfram independently constructed the point-mass kernel with rational binomial expressions, reproduced regrets 9.955606415618 and 9.236742652263, and the threshold 0.648538000074489. The reference threshold arithmetic was separately checked.

Next: specify an actual likelihood for additional frequency observations and enumerate possible outcomes with adaptive policies. Keep the nature/decision timing explicit and do not subtract robust objectives with different oracles and label the result VOI. Any experiment concerning consequences also needs an observation likelihood and an acquisition cost. Such designs have not been implemented here.

Run `python -m research.information_limits.experiment` and `python -m unittest discover -s tests -v`. Complete 36-cell outputs, vertex coordinates, mixture weights, dual gaps and quadrature diagnostics are in `results.json`.
