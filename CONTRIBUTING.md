# Contributing

Project Vulcan is a research-software repository. Contributions are welcome when they make an assumption, experiment, numerical result, or limitation easier to inspect and reproduce.

## Development workflow

1. Open an issue describing the question, expected effect and relevant data or code path.
2. Work in a short-lived branch. Keep changes to the original forecast bytes separate from ordinary bug fixes; the historical forecast JSON files are immutable research artifacts.
3. Run the baseline suite and numerical verification described in [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).
4. Submit a pull request with an explanation of the physical/statistical assumptions, before/after test evidence and reproducibility commands.
5. Label post-hoc analyses as such. Never present a model selected after inspecting held-out data as prospectively registered.

## Scientific standards

- Distinguish an exact mathematical statement *within a specified model* from empirical validation, operational advice and publication status.
- Report adverse results, uncertainty bounds, units, effective numbers of independent physical systems and sensitivity to assumptions.
- Compare independent test sets at the physical-system level where applicable; prevent future-data leakage.
- Document external sources and license restrictions. Do not include proprietary telemetry, export-controlled data or personal credentials.
- Disclose material computational assistance accurately. Automated code or text generation is not an independent scientific reviewer; the submitting contributor is accountable for tests and claims.
- Do not edit past commit history to obscure erroneous results, failed tests or external feedback.

## Pull request checklist

- [ ] Changes are scoped and technically justified.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] `python verify_frozen_forecasts.py` passes.
- [ ] No original `forecast/*.json` bytes or scoring definitions are silently altered.
- [ ] Claims match the supplied evidence and are qualified where necessary.
- [ ] Documentation and interface text are in English for new contributions.
