# Project Vulcan

Public-data Bayesian decision and prospective forecast laboratory.
**Illustrative assumptions, not a validated launch safety estimate.**

- [Executive brief](docs/EXECUTIVE_BRIEF.md)
- [Forecast protocol](docs/FORECAST_PROTOCOL.md)
- [Primary forecast](forecast/reference.json)
- [Technical specification](SPEC.md)
- [Public source scope](docs/PUBLIC_SOURCE_SCOPE.md)

Local verification: 42 tests passed. Public CI status appears in Actions;
no successful remote run or DOI is assumed. Authorship and licensing pending.

# Vulcan public-data decision laboratory

Exercício independente. Não é previsão validada, recomendação operacional ou certificação.

Comece por `SPEC.md` e `results/RUN_REPORT.md`. O código produz quatro entregáveis:
mapas de decisão, superfície EVSI, política por observação e sensibilidade/indeterminação.
Todos os valores de engenharia sem medição pública são hipóteses declaradas.

## Reproduzir

Python 3.12 foi usado nesta execução.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_analysis.py
python run_audit_response.py
python independent_numeric_check.py
```

Sem números aleatórios ou Monte Carlo. Não requer chaves, serviços pagos ou acesso à internet após instalar dependências.
O runtime completo desta execução está registrado em `environment.txt`.

## Estado

- Especificação e execução disponíveis; nada publicado em GitHub/Zenodo.
- Resultados ilustrativos; a região de robustez é relativa à grade explicitada.
- Git local e checksums não provam anterioridade pública.
- `docs/FREEZE_CHECKLIST.md` contém as verificações para publicação.
- `data/` contém tabelas factuais e cenário. `evidence/` contém recibos da pesquisa e hashes.
- Não misture os ajustes contábeis EAC com custo de perda ou atraso da missão.

Os arquivos não afirmam que o LV-01 está usando a revisão modificada. MM é uma hipótese na figura de referência;
HH, HM, MH e revisão incerta estão na sensibilidade.

O mapa principal é `results/structural_envelope.png`. A resposta ponto a ponto está em `docs/AUDIT_RESPONSE.md`. A auditoria recebida foi preservada em `evidence/independent_audit/`; caminhos absolutos nos scripts recebidos não são portáveis. A cópia de execução na raiz altera apenas os caminhos.

## Reprodução integrada e entrada de leitura

`bash reproduce.sh` executa testes, resultados originais, envelope estrutural,
cenários operacionais, integração independente, previsões e scores hipotéticos.
Comece por `docs/EXECUTIVE_BRIEF.md`, depois `docs/TECHNICAL_NOTE.md` e `SPEC.md`.
`docs/FORECAST_PROTOCOL.md` fixa a validade e o corte do episódio ainda não publicado.
O arquivo LICENSE é uma proposta pendente, não declaração de concessão confirmada.
A CI está configurada; nenhum sucesso de CI remota é alegado sem execução observada.

## Adendo de integridade temporal da rodada atual

Consulte `docs/ADVERSARIAL_ADDENDUM_2026-10-09.md`: correções em `VOID_CONFIGURATION`, `NOT_LAUNCHED` e evidência pós-liftoff. A previsão numérica primária não foi alterada. A CI pública, o DOI, a licença e a autoria ainda aguardam validação.
