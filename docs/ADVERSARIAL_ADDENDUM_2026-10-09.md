# Independent Prospective Audit Addendum — October 9, 2026

*English translation of a dated review record. Publication, licensing, and test status below refer to the historical audit rather than present repository state.*

**Historical status: revised candidate, NOT YET PUBLICLY REGISTERED.** The five forecast files and the original Y observation methodology remained unchanged. No forecast should be retrospectively altered after observing the launch.

## Checks performed

- Physical anomaly count K=0..6 and the four-state public Y forecast were reproduced using independent Wolfram calculations.
- NASA-STD-7009B (March 5, 2024) and NASA-HDBK-7009B (February 3, 2026) were used as credibility references. No agency certification was claimed.
- October 29, 2026 was only a tentative non-operator NET date; prospective registration must precede actual launch.
- Reference model P(Y) = [0.5973632855, 0.2072166864, 0.0954200281, 0.1]. This is not a physically calibrated risk estimate.

## Four defects addressed

1. The protocol described `VOID_CONFIGURATION` but the scorer had no such state. The revision permits this **unscored** disposition with concrete hardware-mismatch description and post-liftoff evidence.
2. `NOT_LAUNCHED` cannot be verified solely through a schedule published before episode expiry. Require documentary evidence published after January 1, 2027 UTC.
3. Scored flight outcomes require at least one qualifying source published after actual liftoff; an old schedule is insufficient.
4. The Atlas table reference was corrected from `docs/` to `data/`.

## Remaining limitations

- pgmpy was not installed in the independent audit environment. Test success in a different environment was a package claim, not a new independent reproduction; later tests were separately logged.
- Offline URL/snapshot timestamp checks cannot prove public publication at a claimed time; `score_episode.py` validates local bytes, not external history.
- VOID status is vulnerable to outcome-driven selection. Freeze the objective criteria and independently audit each VOID case.
- A flight-conditional forecast is not a launch-date prediction. One scored event does not establish probabilistic calibration. Document all NOT_LAUNCHED cases.
- Hardware revision/lots, launch authorization, alternative-provider contracts, and mission-consequence CPTs were not physically calibrated.
- Individual authorship, licensing, a public release, and DOI remained to be confirmed as of the audit cutoff.

Sources: https://standards.nasa.gov/standard/NASA/NASA-STD-7009 ; https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009 ; https://help.zenodo.org/docs/github/archive-software/github-upload/ ; https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf .
