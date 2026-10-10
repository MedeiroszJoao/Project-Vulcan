# Research-figure language and provenance inventory

English-first public presentation, with source-preserving chart regeneration.

| Chart | Source | Language in generator | Status |
| --- | --- | --- | --- |
| `results/decision_map.png` | `run_analysis.py` | English labels and captions | Regenerated on the localization branch |
| `results/evsi_surface.png` | `run_analysis.py` | English labels and captions | Regenerated on the localization branch |
| `results/structural_envelope.png` | `run_audit_response.py` | **Previously Portuguese**; translated to English | Regenerated on the localization branch |
| `evidence/independent_audit/structural_envelope.png` | `evidence/independent_audit/structural_envelope.py` | Already English | Original audit artifact retained |

Four tracked PNG files were inspected via the full repository tree: three in `results/` and one independently produced image in `evidence/independent_audit/`. There are three figure subjects; the sensitivity-envelope chart has two original variants.

Corrections were made to the figure-generation scripts rather than painting over embedded text. Existing numerics and model inputs are unchanged. The regenerated images are machine outputs; raster antialiasing and hashes may vary with platform and matplotlib version. The hash file `results/FIGURE_SHA256SUMS` records the newly committed English figure binaries.

The original `SHA256SUMS` file is a **historical archive manifest** and must not be described as the checksum of this later localization commit. Earlier binaries and their checksums remain available via Git commit history. No `forecast/*.json` file or historical scoring protocol has been altered in this localization operation.

To rebuild from this branch:

```bash
python -m pip install -r requirements.txt
python run_analysis.py
python run_audit_response.py
python verify_frozen_forecasts.py
```

The workflow `.github/workflows/regenerate-english-figures.yml` renders and commits chart assets on the localization branch after a successful numerical check. This is a presentational update, not a change to physical-risk evidence.

## Other language checks

- `docs/influence_diagram.mmd`: translated to English.
- `results/RUN_REPORT.md`: regenerated in English with original and operational scenario distinctions intact.
- Historical research reports and audit documents: preserve their content and research chronology when translating; translated interpretations must not be described as new ex-ante declarations.
