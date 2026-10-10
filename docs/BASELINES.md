# Public-report comparator forecasts

The primary object remains `forecast/reference.json`. The five original forecast JSONs are unchanged. `baselines/public_report.json` adds comparators in the same category order: clean, anomaly, loss/degraded, inconclusive. These objects are unregistered until their exact bytes are externally archived before the eligible flight. Their creation date is not proof of prospective registration.

| Comparator | Probability vector | Definition |
| --- | --- | --- |
| Uniform | [0.25, 0.25, 0.25, 0.25] | No preference among four categories |
| Historical raw | [0.5, 0.5, 0, 0] | Retrospective proxy counts [2, 2, 0, 0] |
| Historical add-one | [0.375, 0.375, 0.125, 0.125] | (count + 1) / 8, explicit symmetric Dirichlet prior |

The counts come from `data/vulcan_flights.csv`: successful flights with zero reported anomalies are mapped to clean; successful flights with positive reported anomalies to anomaly. This is a proxy classification, not a retrospective application of the present cutoff and source-search protocol. Configurations, revisions and public disclosure differ; exchangeability is not established. The source hash is recorded in the JSON.

Run `python build_baseline_scores.py` to generate scores for all hypothetical outcomes. No outcome is asserted. Uniform Brier SUM is 0.75 and log loss is ln(4). Add-one Brier scores are [9/16, 9/16, 17/16, 17/16]. Raw zero-probability outcomes have infinite log loss, serialized as null with `zero_probability_observed=true`.

For a valid observed Y, report primary and comparator scores using exactly the same outcome and evidence record. VOID_CONFIGURATION and NOT_LAUNCHED are not scored. An episode-specific Brier skill score against uniform may be reported as 1 - Brier/0.75; do not interpret one episode as demonstrated general predictive skill. Report log-loss differences, not a ratio, and retain infinite-loss flags. Do not select the comparator after seeing Y.

The primary observation model assumes state-independent missingness at 10%. This is uncalibrated; it is not a logical assertion that a publicly confirmed loss is inconclusive. Removing missingness or choosing 2-3% changes assumptions and requires a separate model and registration. An alternative's better score conditional on a hypothetical clean outcome is not justification for replacing the primary.
