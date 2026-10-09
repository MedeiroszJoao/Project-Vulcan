# Revisão adversarial do pacote

Esta revisão foi feita no mesmo processo que implementou o modelo; não é revisão externa independente.

## O que foi corrigido antes da execução

| Risco | Tratamento |
|---|---|
| Tratar Beta contínua como nó discreto exato | Integração polinomial Gauss–Jacobi, ordem e teste de convergência explícitos |
| Usar média de p antes de prever seis motores | Integração preserva a incerteza de p compartilhada |
| EVSI negativo por contar espera/autorização | EVSI puro e ganho líquido são métricas distintas |
| Revisão desconhecida como hardware real | Mistura sobre HH/HM/MH/MM |
| Sucesso orbital como prova de motor limpo | CPT de observação com falhas de detecção e divulgação |
| Transferir compensação LEO para GEO | Tabelas distintas por missão; o resultado ainda pode informar p indiretamente |
| Passar 32 sucessos Atlas por 32 boosters Vulcan | Herança separada e descontada, observabilidade assumida expressamente |
| Inferir custo do atraso de um prazo Vega-C | Cenários de dias separados de custo diário e penalidade |
| Sucesso de testes de software como validação física | Todas as CPTs de engenharia continuam hipóteses |
| Média entre modelos não identificáveis | Cenários estruturais reportados separadamente |

## Limitações que permanecem

- Somente quatro voos públicos; regime estacionário histórico é simplificação não verificável.
- CPTs de severidade, consequência, observação e autorização não foram estimadas nem elicitadas de especialistas.
- Não há identificação de lote ou revisão individual; HH/MM são cenários.
- Os dois estados histórico/ineficaz são observacionalmente iguais quando incremento ineficaz=0.
- Alternativa é abstrata; risco, disponibilidade e custo não representam um provedor real.
- Transferência λ é cenário de dependência epistemológica, não coeficiente calibrado.
- A falta de divulgação é independente na referência. Sinais públicos podem ser missing-not-at-random.
- Oportunidade de slot alternativo não desaparece no modelo; somente custa mais depois.
- Custos de atraso são agregados. A grade de dias não é uma distribuição probabilística do prazo real.
- M* não tem estudo de desempenho ou integração; flag sem boosters permanece false.
- A figura de indeterminação cobre dois priors com demais premissas fixas; não implica robustez universal.
- pgmpy verifica a inferência sobre a mesma parametrização; não é um segundo modelo físico.

## Fontes e anterioridade

As páginas foram abertas/consultadas nesta sessão e capturas feitas pelo script. source_manifest.json
registra horário real da coleta e hashes. O domínio SSC recusou captura HTML direta; há uma extração
textual identificada separadamente, sem alegar equivalência a bytes originais.
Capturas HTML preservam texto e marcação, mas não baixam automaticamente imagens/scripts externos.
As páginas pertencem aos respectivos titulares; conferir direitos antes de republicar capturas integrais.
Não existe release pública ou DOI neste pacote. Nenhum resultado futuro foi incorporado.

## Gates antes de afirmar que o estudo está congelado

Revisão das premissas; confirmação de autoria/licença e destino; conferência final pré-voo;
release pública com hash e data externa verificável. A especificação e o pacote técnico podem
ser revisados agora, sem aguardar até 17/10.
