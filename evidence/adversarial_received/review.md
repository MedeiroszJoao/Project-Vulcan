# Vulcan — Independent Review of Submitted Files (October 9, 2026)

*Translated review originally received in Portuguese. It reports an environment-specific snapshot, not current release status.*

## Verdict

**Technically credible as a hypothetical prospective exercise, but not yet formally frozen or published at review time.** Model probabilities and proper-score implementations were reproducible. Wolfram replicated all seven K-count and four Y-category probabilities using rational Beta integration. The external pgmpy run was **not** reproduced in that audit environment: 41 of 42 tests passed, and one failed for a missing dependency. A different environment reported 37 passing tests; that was not a substitute for public continuous integration.

## Numerical scope and limitations

With assumed MM hardware, effectiveness multiplier e=0.1, regime weights (0.2,0.6,0.2), Beta(3,11), and six boosters, the hypothetical model yields P(Y) = (0.5973632855118782, 0.2072166863854239, 0.09542002810269795, 0.1). A waiting-cost threshold of **USD 1.279000842 million** belongs to the fixed-slot reference alone.

The 360 structural scenarios, 432 operational scenarios and 12 physics controls are separate grids. Their frequencies are not model probabilities and do not demonstrate actual launch safety.

## Problems corrected without changing the forecast

1. The scorer now represents `VOID_CONFIGURATION` as an unscored outcome, requiring documented post-liftoff hardware mismatch.
2. `NOT_LAUNCHED` requires verifiable publication after expiry; a preflight schedule does not establish nonlaunch through the entire period.
3. Scored mission outcomes require at least one source dated after liftoff and before the fixed T+14 evidence cutoff.
4. Corrected an Atlas V 2025–26 source path.

## Remaining issues

- Human validation of objective VC6L/six-booster VOID rules, preventing opportunistic invalidation after seeing mission performance.
- External, independent time-traceable publication/source authentication; the offline scorer does not certify when the stated bytes became public.
- Complete pgmpy 1.1.2 test reproduction with external CI; verify license and author identity.
- Publish a versioned tag/release prospectively and verify any actual Zenodo version DOI.
- Physically assess assumed consequence CPTs, real hardware revisions/lots, approval mechanics, and launch schedule. The modeled output is not a certified rocket failure rate.

## Primary standards and methodological references

- NASA-STD-7009B: https://standards.nasa.gov/standard/NASA/NASA-STD-7009
- 2026 handbook: https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009
- Zenodo repository integration: https://help.zenodo.org/docs/github/enable-repository/
- Archived release/DOI: https://help.zenodo.org/docs/github/archive-software/github-upload/
- Gneiting & Raftery (2007): https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf

This is a contribution to methodological assurance, **not** NASA approval, an operational launch recommendation, or a diagnosis of an actual ULA hardware fault.
