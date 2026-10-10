# Audit corrections implementation plan

Goal: add transparent comparator forecasts and current-package integrity without changing the five original forecasts.
Architecture: separate baseline JSON and hypothetical score table; tracked-file SHA-256 manifest with historical manifest retained; documentation changes only to scientific scope and attribution.
Spec: accepted audit corrections in this session, 2026-10-10.

- Add baseline definitions and score-table generator, with tests for uniform scores, add-one smoothing and zero-probability log loss.
- Clarify case-study status, uniform optimality versus minimax regret, observation assumptions and AI-assisted audit provenance. Identify the verified maintainer handle; do not invent a personal name.
- Archive the previous manifest and build record unchanged. Add generation/check tooling and CI check before result regeneration. Test tampering, missing entries and duplicate entries.
- Run all tests, frozen-forecast verification and original reproduction. Record actual environment and counts; generate final manifest after all edits.
- Publish an isolated GitHub branch and PR with verification evidence.

Review focus: no altered forecast bytes; no claimed retrospective preregistration; no baseline zeros silently clipped; no untracked local audit files published; no claim of human peer review or verified DOI.
