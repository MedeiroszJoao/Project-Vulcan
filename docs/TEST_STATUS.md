# Local Validation after Adversarial Patch — October 9, 2026

*English translation of the original environment-specific test record, not a current CI claim.*

In the recorded environment, **42/42 tests passed**, including pgmpy 1.1.2. `bash reproduce.sh` succeeded with the submitted independent integration check, structural envelope, forecasts and hypothetical scores. Logs: `results/tests.txt` and `results/reproduction_log.txt`. This was not then an independently clean installation or public CI.

The received audit had reported **41/42**, with the missing dependency recorded in `evidence/adversarial_local_suite_log.txt`; this is preserved as a distinct historical environment result.

All five `forecast/*.json` objects matched the previous commit and submitted adversarial ZIP byte for byte by SHA-256. The reference digest was `fc9d0e290adef51459b86c8ad4a1a6ddc03ea087163e48da6e59f6d106f82d1f`.

At the time of this earlier session, GitHub authenticated as MedeiroszJoao but accessible/owned repository searches returned empty lists, and no remote push, public CI, tag, release or DOI had yet been created. **This describes the recorded historical session**, not current repository visibility. See the current GitHub Actions page for actual recent results.
