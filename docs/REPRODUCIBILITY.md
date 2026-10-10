# Reproducibility

## Environment

Baseline: Python 3.12; four pinned direct dependencies in `requirements.txt` (NumPy, SciPy, Matplotlib and pgmpy). These direct pins do **not** fully lock transitive packages or OS-level math libraries. `environment.txt` is a historical snapshot of a broader working environment, not a recommended complete installation.

```bash
git clone https://github.com/MedeiroszJoao/Project-Vulcan.git
cd Project-Vulcan
python -m venv .venv
# Activate .venv using the command for your shell.
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python verify_frozen_forecasts.py
```

Run the reference calculation:

```bash
python run_analysis.py
python run_audit_response.py
python independent_numeric_check.py
python make_decision_brief.py
python build_scores.py
python check_candidate.py
```

Use `bash reproduce.sh` on a POSIX-compatible shell for the legacy end-to-end sequence.

## Two separate reproducibility checks

1. **Artifact integrity:** SHA-256 digest comparisons demand **byte-for-byte** preservation of each of the five archived `forecast/*.json` objects.
2. **Model consistency:** independently compute all forecast values from the declared `Scenario` inputs and compare numeric fields within an explicit 1e-12 tolerance while preserving exact categories, metadata, lengths and booleans. Differences in the final binary floating point digits may occur across machines; they must not be confused with intentional historical file edits.

Never regenerate and overwrite the original forecast objects as a way to make CI green. `build_forecast.py --check` remains a strict legacy diagnostic; the primary CI gate uses the two-part verifier.

## Scientific distinctions

- Passing CI confirms a reproducible computation for declared code and inputs; it is not external physical validation.
- GitHub's public Action timestamps support public-source provenance; they are not a DOI or evidence of peer review.
- NASA battery branches use separately fetched source material and contain their own pinned input hashes, datasets, tests and workflows. They are not included in the baseline command.
- The original `main` forecast has been archived in Git commits; any externally registered version, independent timestamp or future score requires separate verification of the exact bytes.

## Troubleshooting

- If tests pass but strict `build_forecast.py --check` fails due to last-bit JSON serialization, **do not overwrite the archived files**. Run `python verify_frozen_forecasts.py` and examine the integrity and numerical results independently.
- If the verifier fails an archived hash, stop: the tracked forecast bytes have changed.
- If the numerical comparison fails at tolerance, compare model version, Python/NumPy/SciPy versions, parameter definitions and source data.
- If dependency resolution changes the environment, record the exact package and platform versions before reporting equivalence.
