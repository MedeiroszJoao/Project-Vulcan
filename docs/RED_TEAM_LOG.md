# Public red-team findings register (prepublication candidate)

| ID | Observation | Class | Status / treatment |
|---|---|---|---|
| RT-01 | Historical 12 booster-flight exposures cannot identify revision/lots separately | Epistemic / identification | OPEN; keep Beta(3,11) as homogeneous reference only; revisions sensitivity predeclared |
| RT-02 | 29 Oct NET is not confirmed actual date | Calendar / source | OPEN; conditional flight forecast, first release ahead of outcome |
| RT-03 | US$1.279m wait threshold describes reference, not 360 scenarios | Reporting / overclaim | CORRECTED in executive brief; structural interval −5 to 10.744m shown |
| RT-04 | 359/360 preferences are not probabilistic evidence for model validity | Interpretation | CORRECTED; no scenario weights or general claims |
| RT-05 | Public zero-anomaly count is censored, not proof of physical zero | Measurement | ADDRESSED by Y signal scoring, latent K never automatically scored |
| RT-06 | pgmpy validation environment absent, tests 13/14 before enhancements | Verification dependency | RESOLVED locally after dependency install; integrated 37-test suite passes; external CI pending |
| RT-07 | Economic backup launch availability + slot timing unverified | Engineering/economics | OPEN; alternative is modeled abstractly; not an operational recommendation |
| RT-08 | Mission consequence CPTs do not constitute physical fault/event tree | Model discrepancy | OPEN; stage 2 event-tree work prior to physical mission assurance claims |
| RT-09 | Shared-shock parameter rho is not estimated or justified as an actual root cause | Common cause | OPEN, scenario stress-test only; ask external reviewer |
| RT-10 | Probabilities for corrected regimes/historical observations not calibrated | Epistemic | OPEN; research illustrates policy sensitivity and forecast discipline only |
| RT-11 | T+14 could precede real flight, postpone or public reporting | Protocol risk | ADDRESSED conditional on actual launch; explicit expiry 2027-01-01 UTC; delay within validity preserves primary, no launch by expiry = no score |
| RT-12 | Public registry/author identity/license/DOI absent | Publication blocker | OPEN, publish only with verified external time stamp, author approval |

Keep failures visible. New factual findings after flight belong in new dated entries; do NOT silently modify preflight claims.


| RT-13 | Forecast could expire selectively because no expiry was specified | Prospective selection | FIXED with explicit validity; no silent primary replacement |
| RT-14 | T+14 date lacked a precise clock cutoff | Endpoint definition | FIXED: UTC liftoff date+15 at 00:00 exclusive; late coding only from pre-cutoff evidence |
| RT-15 | Scorer accepted arbitrary forecast bytes and unverified timestamp strings | Provenance | Hash and temporal consistency checks added; external authenticity still manual |
| RT-16 | Incoming candidate omitted operational extensions | Integration | Merged without replacing corrected core; separate grids explicitly labeled |
| RT-17 | Atlas extension had two local dates labeled UTC | Factual error | Corrected ViaSat-3 F2 and Leo 6; attachments preserved |
| RT-18 | CFF asserted MIT although license was only proposed | Metadata | Removed license assertion pending author's choice |

| RT-19 | VOID_CONFIGURATION previsto no protocolo, não implementado como disposição explícita no score | Protocolo/código | CORRIGIDO no candidato revisado; requisito de descrição e evidência pós-lançamento; revisão humana exigida |
| RT-20 | NOT_LAUNCHED aceitava evidência publicada antes da expiração para provar ausência no futuro | Verificabilidade | CORRIGIDO; exige um registro de status pós-expiração, sem pontuação |
| RT-21 | O scorer admitia um documento pré-voo como única evidência de resultado T+14 | Proveniência | CORRIGIDO; exige ao menos evidência publicada depois do liftoff e antes do corte |
| RT-22 | Fonte Atlas V 2025/26 apontava pasta errada (`docs/`) | Documentação | CORRIGIDO para `data/` |
