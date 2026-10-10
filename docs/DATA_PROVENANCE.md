# Data provenance

The project makes a strict distinction between publicly reported mission facts, numerical assumptions and laboratory measurements from a different physical domain.

| Data class | Location | Interpretation |
| --- | --- | --- |
| Public Vulcan flight reports | `data/vulcan_flights.csv`, `docs/SOURCE_REGISTER.md` | Reported anomaly counts under limited observability; not a complete component reliability database |
| External contextual launch records | `data/atlas_gem63.csv`, `data/atlas_2025_2026_extension.csv`, `data/vega_timeline.csv` | Contextual, not automatically interchangeable booster exposures |
| Decision assumptions | `data/reference_scenario.json`, `SPEC.md` | Counterfactual probabilities, dollar consequences, procurement and approval choices |
| Frozen candidate forecasts | `forecast/*.json` | Five scenario-conditional predictions whose original bytes must remain unmodified |
| NASA PCoE laboratory batteries | [PR #3](https://github.com/MedeiroszJoao/Project-Vulcan/pull/3), [PR #4](https://github.com/MedeiroszJoao/Project-Vulcan/pull/4) | Actual measured lithium-ion capacity series; never rocket motor observations |
| Archived source records | `evidence/source_manifest.json` and linked evidence files | Traceability of consulted sources, not proof that every external page was independently authenticated |

For the original NASA battery-capacity cross-check, all 636 measured capacity values used by PR #3 were compared to NASA source MATLAB records; the audit reports zero maximum numeric difference for that column. This does not certify all extracted metadata or forecasting performance. PR #4 uses different physical cells and protocols. Refer to the branches for source archive SHA-256 and per-device results.

## Reuse boundaries

- Never substitute an observed battery aging distribution for an estimated GEM 63XL hazard rate.
- Never equate non-reporting with physical absence of an anomaly.
- Distinguish model input assumptions from measurements, including for commercially sensitive launch decisions.
- External source materials and experimental files are not granted a new license by appearing in this repository.

Methodological sources are linked from `docs/SOURCE_REGISTER.md`, `SPEC.md` and the research PR descriptions.
