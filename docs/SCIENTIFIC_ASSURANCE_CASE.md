# Scientific assurance case — self-assessment, NOT agency certification

Adapted as a claims/evidence/rebuttal ledger from [NASA's 2025 guidance](https://ntrs.nasa.gov/citations/20250002210). None of the claims below implies ULA, NASA or manufacturer approval.

| Claim | Evidence | Rebuttal / limitation | Assessment |
|---|---|---|---|
| Reference computations implement declared equations | Original CI 42/42, original numerical integration, `pgmpy` comparison | A correct computer program can implement the wrong physical model | Computationally supported |
| Historic reports identify the future target mission consequence CPT | New `docs/IDENTIFIABILITY_REPORT.md` shows opposite-action witnesses with same likelihood | CPT absent from the historical likelihood | **Refuted for current likelihood** |
| Original Y forecast is objectively evaluable | Preserved original `forecast/reference.json` and `docs/FORECAST_PROTOCOL.md` | Reporting probability and detection assumptions not calibrated; one future score is not calibration | Partially supported |
| Model determines a robust action under unconstrained CPT risk | Sharp full-simplex extrema straddle zero | No robust dominance; minimax regret depends on assumed costs and broad model class | **Not supported** |
| A booster causal failure sequence is quantitatively validated | `docs/MECHANISTIC_PRA_SCAFFOLD.md` only | No traceable physical CPTs or independent propulsion/GNC review | **Not achieved** |
| Operational decision is suitable for a real mission | Illustrative cost and approval model | No validated contract, manifest, launch authority, physical mission risk | **Not supported** |
| Transferable prediction/decision engine outperforms baselines | No untouched external benchmark yet | Needs prespecified held-out NASA data and real baselines, report failures too | Pending |

**Next tests:** physically constrained event-tree CPT admissibility; expert challenge; external NASA engine-simulation **or** experimental battery dataset benchmark separated from actual Vulcan rocket validation. Original public prospective records remain immutable.
