# Resultado executado — laboratório de decisão Vulcan

Exercício independente com dados públicos. Nenhuma CPT de engenharia abaixo é uma estimativa validada do Vulcan.
Estado: implementação executada; não é registro público congelado.

## Cenário ilustrativo de referência
M*: 3.000 kg, comunicações resilientes, GEO direto, janela 15/11–15/12/2026.
Revisões MM são hipótese, não conhecimento do hardware instalado.
Prior uniforme; sem Atlas; 6 boosters no LV e 4 no alvo; P(Θ)=(.2,.6,.2).
Consequência de perda US$ 1.000 milhões; atraso incremental US$ 10 milhões.

| Métrica | US$ milhões |
|---|---:|
| EVSI puro, conjunto de ações fixo contrafactual | 3.989851 |
| Custo esperado de realocar agora | 35.750000 |
| Custo esperado de aguardar e decidir com autorização | 44.470999 |
| Ganho líquido de aguardar | -8.720999 |

Ação preferida neste cenário: **realocate_now**. Não extrapolar para recomendação operacional.

## Arquivos
- decision_map.png / decision_map.csv: benefício de esperar e discordância entre dois priors, demais premissas fixas.
- evsi_surface.png / evsi_surface.csv: grade de pesos de regime e relevância; ação fixa para EVSI.
- policy.csv: quatro observações, condicionadas a autorização concedida ou negada.
- structural_sensitivity.csv: 360 cenários estruturais, sem média entre cenários.
- heritage_sensitivity.csv: análise secundária sob observabilidade perfeita da herança.
- controls.csv: eficácias, severidade, observação e política de autorização.

Uma região estável entre dois priors não é robustez universal. Custos, CPTs, transferência e governança
continuam hipóteses. O mesmo número de anomalias pode produzir consequências muito diferentes.
O ensaio pgmpy valida a inferência a partir das CPTs emitidas, não valida a física dessas CPTs.

## Resposta executada à auditoria independente

Mapa principal: `structural_envelope.png`: 2.775 células realocar em todos, 336 discordância, zero aguardar em todos os 360 cenários. Envelope recebido reproduzido numericamente.

Extensões: 432 cenários operacionais e 12 controles físicos/observacionais separados. A janela de planejamento de M* passa a 15/01–15/03/2027; a referência acima preserva as hipóteses antigas como teste de regressão. Não confundir os resultados.

42 testes passaram, incluindo pgmpy. Integração adaptativa independente recebida executável em `independent_numeric_check.py`. Consulte `docs/AUDIT_RESPONSE.md` para limites e alterações. Não há release pública nem DOI.
