#!/usr/bin/env bash
# Reproduce the original reference calculations without rewriting forecasts.
set -euo pipefail

mkdir -p results
python -m unittest discover -s tests -v 2>&1 | tee results/tests.txt
python verify_frozen_forecasts.py
python run_analysis.py
python run_audit_response.py
python independent_numeric_check.py
python make_decision_brief.py
python build_scores.py
python check_candidate.py
python verify_frozen_forecasts.py
printf '\nReproduction complete. Public forecast registration is not implied.\n'
