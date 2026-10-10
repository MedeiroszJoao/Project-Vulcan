# Package integrity and build records

`SHA256SUMS` covers every Git-indexed file except itself. Its own bytes are bound by the containing commit or externally archived package. Untracked environments, scratch analyses and local audit outputs are not part of the package. Stage additions and removals before generation.

```
python scripts/package_manifest.py --write
python scripts/package_manifest.py
```

CI checks inventory and bytes immediately after checkout, before computations regenerate results. To verify an extracted archive without Git, use `python scripts/package_manifest.py --archive`; this checks listed bytes but cannot independently establish inventory completeness. A manifest does not authenticate its own origin.

The superseded manifest and build record from base commit 8f85b9a7573352e72b8f157786656d4f306d388c are retained byte-for-byte in `evidence/package_history/8f85b9a7/`. They describe historical metadata and are not validators for the current tree. Original forecast integrity is checked separately by `verify_frozen_forecasts.py` before and after reproduction.

`BUILD_RECORD.json` reports observed local checks, environment and base revision, without a self-referential delivery commit. Git identifies the final delivery commit. Successful local tests do not imply public CI success, external registration, peer review or physical validation. Check final remote CI and any archive record independently.

Persistent archival identifiers aid citation. Prior existence requires a verifiable external time record linked to exact content; a locally assigned date or hash alone is insufficient. Zenodo and OSF provide different archival/registration workflows. No DOI is asserted by this correction.
