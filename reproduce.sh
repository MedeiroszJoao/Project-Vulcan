#!/usr/bin/env bash
set -euo pipefail
python -m unittest discover -s tests -v 2>&1 | tee results/tests.txt
python run_analysis.py
python run_audit_response.py
python independent_numeric_check.py
python make_decision_brief.py
python build_forecast.py --check
python build_scores.py
python check_candidate.py
printf '\nSUCCESS: complete reproduction. Candidate NOT automatically publicly registered.\n'
