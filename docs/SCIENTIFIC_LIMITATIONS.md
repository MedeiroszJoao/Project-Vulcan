# Scientific claims and limitations

| Claim | Status | Evidence and qualification |
| --- | --- | --- |
| Reference computations implement the declared equations | Computationally supported | Original unit tests, cross-calculations and baseline CI; an internally correct program may still encode the wrong physical assumptions |
| Four historic public flight records determine the future mission's consequence CPT | Not supported | Structural non-identifiability witnesses in draft PR #2 |
| A preferred economic action is robust to all physically possible risks and contracts | Not established | Evaluated scenario grids and selected mathematical CPT simplexes are neither a complete physical uncertainty set nor a posterior |
| NASA battery measurements were used for external method tests | Supported within stated dataset scope | Four-cell and eleven-cell draft benchmarks with NASA provenance checks and serially dependent outcomes |
| Nominal predictive intervals are always calibrated | Refuted for tested plug-in models/observations | PR #3 linear coverage of 60.3% vs 90% nominal; PR #4 AR(1) ~84.8% vs 90% nominal |
| Experimental battery forecasts validate Vulcan rocket propulsion hazards | Not supported | Different systems, degradation mechanisms, data and operating regimes |
| A future flight's official reliability or launch-readiness has been determined | Not supported | No hardware-level calibrated model or authority to certify readiness |
| This repository has completed independent peer review or an archived DOI | Not established | Public source and CI evidence exist; archival release and third-party review require their own proof |

## Key methodological limitations

- **Sparse events and ascertainment:** the model uses reported anomalies rather than complete measurement of all physical failures. Revision/lot identity and detection rates are incompletely observed.
- **Assumed consequences:** the probability of compensation, degraded delivery or mission loss is not identified by the public count data. Mathematical CPT bounds are conditional on what is held fixed.
- **Forecast scoring:** a scoring rule can judge a recorded outcome conditional on a frozen forecast; one future categorical event cannot establish probability calibration.
- **Economic assumptions:** launch alternatives, compatibility, lead times, authorization, reservation fees, payload value and opportunity costs are hypothetical.
- **Monte Carlo:** the AR(1) demonstration conditions on estimated parameters and does not capture parameter uncertainty, changing operational regimes or full model discrepancy.
- **Battery series:** observations are serially correlated, experimental protocols are heterogeneous, and some initial recorded measurements are atypical. Pooled metrics are sensitive to cohort weighting.
- **Visualization:** the interactive model uses public dimensions and schematic interior geometry. It is **not** dimensionally certified CAD, engineering FEA/CFD, flight software or measurement data.

### Interpretation rule

A numerical result with many decimal places is not a physically accurate probability unless its assumptions are themselves supported. Keep empirical measurements, conditional mathematical proofs, counterfactual scenarios and forecasts in separate categories.
