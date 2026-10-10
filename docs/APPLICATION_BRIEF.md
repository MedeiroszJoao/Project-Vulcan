# Project Vulcan — Academic project summary

**Field:** probabilistic graphical models, uncertainty quantification, scientific programming, aerospace decision analysis

**Research question:** When would observing another flight provide enough information to justify deferring a hypothetical launch-procurement decision?

## What was developed

A Python-based probabilistic decision-analysis laboratory with explicit uncertainty over historical anomaly reporting, booster revision hypotheses, physical consequences, information transfer and economic decisions. The baseline uses a structured model, numerical integration, independently checked decision arithmetic, unit tests, and immutable candidate forecasts. Research extensions explore identifiability and compare forecast methods on public experimental data.

## Selected research findings

The strongest result is not a claim of a particularly accurate rocket failure rate. The draft identifiability study constructs future-consequence models that agree on the available historical evidence and on the public flight-signal prediction yet lead to different preferred decisions. This locates an information gap rather than concealing it behind a precise-looking probability.

A separate NASA battery-data study provides an external methodological stress test: on four cells, an aggregated linear point forecast improved mean absolute error, while its nominal 90% intervals captured only 60.3% of serially dependent hold-out measurements. A follow-up across 11 other cells shows that apparent model rankings depend on experimental protocols and averaging choices.

These numerical benchmarks do not validate Vulcan propulsion or mission safety.

## Engineering and computational practices

- Specified model assumptions, observable outcomes and proper forecast scores before outcome measurement.
- Checked model arithmetic and numerical consistency with tests and independent calculations.
- Preserved historical forecast bytes with SHA-256 verification.
- Published negative results and evidence limits, rather than selecting only favorable metrics.
- Maintained primary sources, data provenance, code, documentation and CI logs.
- Built an illustrative component-selectable 3D model as an explanatory interface, explicitly separate from safety-critical simulations.

## Scientific boundaries

This is independent student research software, not agency-certified engineering, launch-readiness analysis or a peer-reviewed paper. Flight telemetry, hardware revision/lot data, qualified physical consequence likelihoods and independently validated operational procurement assumptions are unavailable in the public record used.

## Reviewer entry points

[Project overview](../README.md) · [Reproduction](REPRODUCIBILITY.md) · [Scientific limitations](SCIENTIFIC_LIMITATIONS.md) · [Identifiability PR](https://github.com/MedeiroszJoao/Project-Vulcan/pull/2) · [NASA benchmark PR](https://github.com/MedeiroszJoao/Project-Vulcan/pull/3)

Maintainer account: [@MedeiroszJoao](https://github.com/MedeiroszJoao). The applicant should describe their individual role, external computational assistance and independent contributions accurately in the college application.
