## Purpose

Describe the question being addressed and why this change is necessary.

## Methods and evidence

- Assumptions changed:
- Data sources and version/hash:
- Baseline comparison:
- Independent or adversarial checks:

## Reproduction

```bash
python -m unittest discover -s tests -v
python verify_frozen_forecasts.py
```

## Research integrity

- [ ] No frozen forecast or scoring protocol was silently changed.
- [ ] Post-hoc analysis is labeled as such.
- [ ] Scientific claims do not exceed the available data.
- [ ] New external assets are attributed and their terms reviewed.
