# Prospective freeze and postflight operational runbook

## Before the earliest possible LV-01 outcome

1. Confirm UTC cut-off: still preflight. Verify publicly available sources and explicitly log any new observations, schedules, changes in mission configuration and document snapshots. If already launched, **do not** claim this episode is prospective.
2. Confirm authorship, public byline, code license, data redistribution legality and disclosed role of AI assistance. The `CITATION.cff` and `LICENSE` currently contain identifiable TODO fields: replace before publishing.
3. Reproduce in a clean Python 3.12 environment: `python -m pip install -r requirements.txt`, `python -m unittest discover -s tests -v`, `python run_analysis.py`, `python build_forecast.py --check`, `python make_decision_brief.py`, and `python check_candidate.py`.
4. Check the git diff, commit ALL intended prediction files/README/SPEC and hashes in a real user repository. Do not commit secret keys or claim local file timestamps prove ex ante registration.
5. Connect GitHub repository at https://help.zenodo.org/docs/github/enable-repository/ BEFORE creating a new release. Publish a **public versioned GitHub release** containing the frozen reference forecast and scores protocol. Check commit SHA and tag in GitHub.
6. Follow https://help.zenodo.org/docs/github/archive-software/github-upload/ ; after Zenodo processing, OPEN and verify the archived code, version DOI, release timestamp, title and files. It is possible that the actual public DOI becomes available AFTER the initial release; until verified, status is "release created, DOI pending".
7. Record the release URL, SHA, DOI and externally verifiable observation time in a **separate post-release attestation file**. Do not rewrite the frozen preflight prediction.

## Following flight

- At **T+72h (UTC)** record preliminary source URLs and evidence without scoring the T+14 forecast. Note conflicts and any unavailable source.
- At **T+14 UTC calendar days**, classify the mutually exclusive public reporting event as defined in `docs/FORECAST_PROTOCOL.md` and create `scoring/episode_01_T14.json` via the scorer. Include source URLs and SHA256 of the original frozen forecast; publish both Brier and log scores (including unfavorable outcomes).
- If launch has NOT occurred, record `NOT_LAUNCHED`, no score. Postpone/retarget only by publishing another verifiably prospective forecast before flight. Never backdate.
- Later disclosures are tracked in another version as measurement revisions; the original score remains preserved. Do not incorporate them into an unregistered ex-ante forecast.

## Revisions post-freeze

A scientific revision is possible; it must have a new version and new externally registered release. Do not erase or rewrite the prior forecast or retrospective error log. Forecast episodes must include first data-availability time, issue time and target time to avoid look-ahead bias.
