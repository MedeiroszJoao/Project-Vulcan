# Adversarial Review of the Research Package

*English translation of the original prepublication review, which was conducted within the same project process and **was not an independent external review**.*

## Issues addressed before initial execution

| Risk | Treatment |
| --- | --- |
| Representing continuous Beta uncertainty as an exact discrete node | Gauss–Jacobi integration with explicit quadrature order and convergence checks |
| Replacing a shared uncertain anomaly rate by its mean before predicting six motors | Integration retains shared uncertainty |
| Reporting a negative EVSI through mixing in waiting/approval costs | Pure EVSI and net waiting gain treated as distinct metrics |
| Treating unknown revision as a physical type | Mixture over HH/HM/MH/MM |
| Treating orbital success as proof of an anomaly-free motor | Observation CPT allows incomplete detection/disclosure |
| Applying LEO compensation CPTs directly to GEO | Distinct mission consequence tables; public outcome may indirectly inform p |
| Counting 32 Atlas successes as 32 direct Vulcan exposures | Discounted, separate heritage sensitivity with explicit observability assumptions |
| Deriving waiting cost directly from a Vega-C historical delay | Delay-day, daily cost and window penalty assessed separately |
| Treating passing software tests as physical validation | Engineering CPTs remain hypotheses |
| Averaging unidentified models | Structural scenarios reported individually without arbitrary model weights |

## Unresolved limitations

- Only four publicly reported flights. A stationary historical rate is an unverified simplification.
- Severity, consequence, observation and authorization CPTs were neither measured nor professionally elicited.
- Individual motor lots/revisions cannot be identified; HH/MM remain cases.
- Historic-equivalent and ineffective-correction regimes are observationally identical when the ineffective increment is zero.
- The alternative provider is abstract; costs, reliability and launch access are not operator estimates.
- Information-transfer relevance lambda is epistemic-dependence stress, not a calibrated physical parameter.
- Reference disclosure missingness is independent; actual public reporting may be missing-not-at-random.
- Alternative capacity does not disappear after a wait in the original model; it merely becomes more expensive.
- Waiting costs are aggregated; the day grid is not a probability distribution over launch schedules.
- No M* performance/integration feasibility analysis. Booster-free feasibility remains false.
- The two-prior indeterminacy map does not establish universal robustness.
- pgmpy checks inference under the *same assumptions*, not a physically independent model.

## Sources and chronology

Web pages were opened in the original session and captures were attempted by script. `evidence/source_manifest.json` records actual collection timestamps and hashes. The SSC domain rejected direct HTML capture; a separately identified textual extraction was used without pretending equivalence to original source bytes.

Saved HTML contains page markup and text but may not include remotely linked images or scripts. Upstream copyright owners retain their rights; do not redistribute full captures without checking them.

At the original cutoff the package had no published release or DOI, and no later flight outcomes had been incorporated.

## Gates before claiming a prospective freeze

Review CPT assumptions, confirm author/license/publication destination, recheck the real preflight situation, and issue an externally timestamped public release preserving the registered forecast bytes. Methodology and code review can proceed independently of the planned October 17 target.
