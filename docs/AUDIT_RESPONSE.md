# Resposta à auditoria independente — 09/10/2026

Exercício público de decisão sob cenários; não é estimativa validada de segurança nem recomendação de lançamento. Candidato à publicação, sem registro público ex ante emitido.

## Decisão

Aceitamos a distinção entre aritmética correta e hipóteses interpretáveis. O cenário de referência permanece como regressão. A contribuição principal é a sensibilidade da decisão às hipóteses e oportunidades realmente disponíveis.

| Achado | Tratamento executado | Limite que permanece |
|---|---|---|
| F01, revisões históricas | Betas rotuladas como submodelo; contraste de risco e detecção por voo | Revisões não identificadas; não estimamos eficácia de correção |
| F02, informação privada em G | Conjunta P(Y,G,Z) e política condicionada a G; gate responde a escore latente | Modelo reduzido, sem telemetria; não resolve toda estrutura de revisão |
| F03, alternativa garantida | Slot aleatório, reserva com custo, integração, adiamento explícito | Custos e contratos hipotéticos; grade principal ainda assume alternativa viável agora |
| F04, janela curta | Jan–mar/2027 para planejamento; janela original como estresse; sinal T+14 e lead-time | Não há compromisso real de provedor |
| F05, mapa restrito | Reproduzido envelope dos 360 cenários, agora mapa principal | Não inclui cruzamento de todas as novas hipóteses |
| F06, vários boosters | Perda em K≥2=.1,.3,.55,.8; degradação fixa .2 | Sensibilidade, sem calibração |
| F07, Atlas | Extensão em tabela separada; correções UTC | Não incorporada ao prior |
| F08, λ | Mantida como mistura de dependência informacional | Não é probabilidade física calibrada |
| F09, viabilidade | Sem boosters excluído; GEO 3000kg continua hipótese | Compatibilidade não validada |
| F10, divulgação | Divulgação condicionada a K>0 e detecção por voo | Outras formas de censura não modeladas |
| F11, calendário | NET secundário distinto de confirmação ULA | Revalidar antes do freeze |
| F12, proveniência | Build e checksums rastreados, escopo definido sem autorreferência | Autoria, licença, release e DOI pendentes |
| F13, testes | 21 testes executados, incluindo pgmpy | Novo código ainda requer revisão externa |
| F14, aritmética | Integração adaptativa recebida executada novamente | Valida contas do cenário, não probabilidades físicas |

## Resultados reproduzidos

Envelope de 3.111 células e 360 cenários: **2.775 realocar em todos; 336 discordância; zero aguardar em todos**. Todos os mínimos, máximos e rótulos coincidem com o CSV recebido, tolerância numérica 1e−10 milhão. Nenhuma distribuição de probabilidade foi atribuída aos modelos.

Referência: EVSI puro 3,989851 milhões; realocar 35,75; esperar 44,470999; ganho líquido −8,720999. A regra original de G e disponibilidade é preservada somente nessa referência. A nova análise operacional não deve herdar esses números como sua conclusão.

Foram acrescentados **432 cenários operacionais** e **12 controles físicos/observacionais**. Esses conjuntos são separados: não alegamos envelope conjunto sobre todo o espaço de hipóteses. Reserva é uma ação possível paga antes do sinal, não uma escolha gratuita depois de saber o resultado. Adiamento é opção explícita, com consequência hipotética.

## Duas correções à própria auditoria

No CSV recebido, `date_utc` continha data local em duas linhas:

| Missão | Recebido | Corrigido UTC | Fonte |
|---|---|---|---|
| ViaSat-3 F2 | 2025-11-13 | 2025-11-14, 03:04 | https://www.ulalaunch.com/missions/next-launch/atlas-v-viasat-3-f2 |
| Amazon Leo 6 | 2026-04-27 | 2026-04-28, 00:53:30 | https://www.ulalaunch.com/missions/next-launch/atlas-v-amazon-leo-6 |

A soma de exposições não muda. O anexo original foi preservado; só a tabela incorporada ao projeto foi corrigida. As nove páginas ULA foram abertas na revisão; sucesso da missão não prova ausência física de anomalia. Identificação GEM63 no Atlas: https://blog.ulalaunch.com/blog/kuiper-2-atlas-v-to-launch-amazons-next-step-in-journey

Também evitamos a circularidade de um arquivo de checksums conter seu próprio hash ou de um commit conter seu próprio identificador. `SHA256SUMS` exclui a si mesmo e o diretório Git; `BUILD_RECORD.json` identifica o commit-base e o procedimento de construção, não pretende conter o hash do commit que o inclui. O identificador do commit de entrega é obtido de `git rev-parse HEAD`.

## Condições restantes para publicação

A conclusão defensável é condicional: existem hipóteses em que informação muda a decisão, mas isso não demonstra que aguardar seja preferível para uma missão real. Ainda faltam revisão humana das novas premissas, identidade/licença e publicação efetiva com data verificável. A aprovação condicionada recebida não equivale a aprovação externa das extensões implementadas nesta resposta.
