# Identifiability of hypothetical target-mission consequences

**Scientific status:** MODEL-SPECIFIC NON-IDENTIFICATION RESULT, not physical rocket validation. **Date:** 2026-10-09. Code: `src/identifiability.py`, `run_identifiability.py`, `tests/test_identifiability.py`. The five original LV-01 prediction JSON files are not changed.

## Mathematical reason

The current historical likelihood is constructed from only four records `D={(n_i,k_i_reported)}` of reported booster anomalies:

`L(D|p,ψ,η)=∏_i P(k_i_reported|n_i,p,ψ_i)=L(D|p,ψ)`

Here `p` is booster base risk, `ψ` includes the history observation model, and `η` is the **future hypothetical M*** consequence CPT. The latter does not occur in the historical likelihood. Thus distinct choices of `η` have identical likelihood at every `p`. Assuming a prior dependence between `p` and `η` or adding physical data can transmit information, but those are additional assumptions or observations. This result is limited to the actual current likelihood, not a theorem that engineering mission risk is unidentifiable in principle.

## Counterexample under fixed scenario assumptions

All three mathematical worlds hold fixed the complete historical likelihood, prior, LV-01 public-observation model, pair revision assumptions, target booster dynamics, costs, gate and action set. All keep the target CPT at K=0 as `(.998,.001,.001)`. **Only** hypothetical M* target consequence CPT rows for K>=1 change.

| World | P(target M* loss) | Net wait benefit, US$m (C_D=$10m) | Action |
|---|---:|---:|---|
| Original reference | 0.0633784 | -8.720999 | Reallocate |
| Low-consequence mathematical witness | 0.00199746 | +9.621932 | Wait |
| High-consequence mathematical witness | 0.1490045 | -15.000000 | Reallocate |

The published LV-01 signal probabilities remain `[0.5973632855, 0.2072166864, 0.0954200281, 0.1000000000]` across all three worlds. The likelihood of the four historical booster-count reports is *exactly identical* across them. Future M* consequence risk and decision differ dramatically. None of the worlds is asserted to be physically calibrated.

## Exact full-simplex consequence uncertainty bounds

Holding *all other model inputs fixed*, allow each K>=1 target consequence row `(success,degraded,loss)` to be **any nonnegative probability triple summing to 1**. Keep the K=0 row unchanged. Then, with `C_v(y;η)` denoting target cost conditional on public signal y:

`C_wait(η)=C_D + Σ_y P(y)[g_y min(C_v(y;η),A) + (1-g_y) A]`

where A is the later-alternative cost. The conditional target expected cost is a nonnegative weighted sum of loss states ordered `0 <= dL <= L`; hence `C_wait` is nondecreasing in each target CPT row's expected loss. **Both global extrema are attained** by assigning every K>=1 branch either success with certainty or loss with certainty. Unlike a sampled 360-row grid, this is a mathematical sharp bound **for this specifically defined class**.

With reference economic assumptions at C_D=US$10m:

| Metric | Result |
|---|---:|
| Lower bound of gain from waiting | -US$15.000000m |
| Upper bound of gain from waiting | +US$10.619867m |
| Robust dominance | **Undetermined — neither action dominates** |
| Maximum regret of waiting | US$15.000000m |
| Maximum regret of immediate reallocation | US$10.619867m |
| Minimax regret within this **mathematical set** | Reallocation |

Robust dominance and minimax regret are different decision criteria. The latter is **not an operational recommendation**: the unconstrained CPT simplex contains physically unrealistic extremes, and launch logistics, observable data and approval models remain hypothetical and fixed.

## Reproduce

```bash
python -m unittest tests.test_identifiability -v
python run_identifiability.py
```

The code writes a separate JSON at `results/scientific_upgrade/identifiability_witness.json`. Six additional tests cover equivalence with the original numerical joint distribution, observation invariance, decision reversal, sharp bounds, 20 reproducibly generated interior CPTs, and invalid probability rows. All primary forecast files stay byte-for-byte unchanged.

## Scientific limits and next gate

What is established: **the current data likelihood does not identify the target consequence mapping**, and that under the displayed broad uncertainty class, no action is robustly dominant. What is not established: physically plausible bounds for a GEM 63XL, real ULA/SSC costs, calibrated mission safety, new physical theory, external expert approval, or superior predictive accuracy.

Next obtain reviewed mechanistic/engineering constraints on the consequence CPT and corresponding observation evidence, then repeat bounding. Do not narrow the admissible set without new physical or elicited evidence.

Primary references: [NASA PRA Guide](https://ntrs.nasa.gov/citations/20120001369); [NASA Model Credibility Standard](https://standards.nasa.gov/standard/NASA/NASA-STD-7009); [NASA Risk Assurance Cases (2025)](https://ntrs.nasa.gov/citations/20250002210).
