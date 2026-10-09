# Vulcan: valor da informação de um voo comercial

**Exercício independente de análise de decisão com dados públicos. Não constitui recomendação operacional, certificação ou avaliação oficial de segurança.**

Estado em 09/10/2026: especificação revisada, código e testes executáveis. Não é ainda um registro público congelado. Prazo solicitado: pacote pronto antes de 18/10/2026; meta interna 17/10, America/Sao_Paulo. Não há execução futura automática agendada.

## 1. Pergunta e missão M*

Sob quais hipóteses o valor de observar o LV-01 compensa o custo incremental de aguardar antes de alocar uma missão sensível?

Um planejador hipotético, sem vínculo com os operadores reais, escolhe para um único satélite de comunicações resilientes:

| Item | Premissa do estudo |
|---|---|
| Massa | 3.000 kg; hipótese, não manifesto real |
| Órbita | entrega direta geossíncrona, circular, altitude de referência 35.786 km e inclinação-alvo próxima de zero |
| Configuração de referência | Vulcan com quatro boosters e Centaur de alta energia; compatibilidade assumida para o exercício, não certificada |
| Janela | 15/01/2027 00:00 UTC até 16/03/2027 00:00 UTC, limite superior exclusivo |
| Data-base de lançamento | 15/01/2027; janela original nov–dez/2026 preservada como estresse |
| Valor contábil hipotético da carga V | US$ 250 milhões |
| Consequência total de perda L | US$ 250–2.000 milhões, referência US$ 1.000 milhões; já inclui V, não somar V novamente |
| Consequência degradada | dL, d=.25 referência, sensibilidade .1–.5 |
| Alternativa | provedor abstrato, com capacidade, autorização e slot assumidos; não é estimativa da SpaceX |

Não é preciso estimar perdas estratégicas secretas. L é um limiar variável, e pode ser substituído por uma restrição de risco. O modelo atual é neutro a risco monetário; não implementa uma restrição regulatória de probabilidade de perda.

## 2. Ações e sequência

- D0: realocar agora, aguardar ou reservar a alternativa e aguardar. Reserva tem custo irrecuperável hipotético.
- Após esperar: observar Y, G e disponibilidade do slot; escolher entre ações viáveis. Adiar M* é fallback explícito se nenhuma oportunidade de lançamento for viável ou econômica.
- Lançar Vulcan imediatamente fica apenas no conjunto contrafactual do EVSI puro. Sua indisponibilidade é uma premissa de governança do caso, não uma conclusão jurídica atual.
- Vulcan sem boosters: excluído deste núcleo; flag de viabilidade false. Não há demonstração pública de compatibilidade de M*.
- Referência aritmética antiga mantém slot certo. A extensão operacional varia slot, reserva, prazo de integração e informação adicional na aprovação. As duas análises têm nomes distintos.

## 3. Correções à especificação recebida

1. Revisão desconhecida é estado de conhecimento: hardware verdadeiro é histórico ou modificado. Modelar uma distribuição conjunta sobre (R_LV,R_M), não uma terceira espécie de motor.
2. Mesma revisão é condição de transferência assumida, não prova de intercambiabilidade. Lotes e condições distintas podem reduzir a relevância λ.
3. O resultado orbital pode informar a taxa de anomalia indiretamente pela verossimilhança. O que não transferimos é a CPT de compensação/consequência entre LV e M*.
4. Beta é contínua: a rede não é literalmente toda discreta. A implementação enumera estados discretos e usa quadratura de Gauss–Jacobi exata para os polinômios deste modelo, até arredondamento numérico. Não substitui a Beta pela sua média.
5. EVSI≥0 vale para informação gratuita com conjunto de ações e utilidade fixos. Ganho líquido da espera pode ser negativo. Esses resultados são separados nos arquivos.
6. EVSI=0 se Y for independente de todos os determinantes de utilidade, mantendo ações fixas. Independência somente de Θ não basta quando Y informa p ou revisão.
7. Três regimes não são três revisões certificadas. São hipóteses funcionais, com pesos escolhidos por cenário; não estimados em quatro voos.

## 4. Evidência e atualização histórica

Dados: (n,k)=(2,0),(2,1),(4,0),(4,1), sendo k a contagem pública de anomalias. Não relatada não equivale a ausência física comprovada. Referência assume observação histórica perfeita, independência condicional e taxa estacionária de referência. Essa estacionariedade é uma simplificação, pois revisão/lote por motor não são conhecidos. Não alegar que as correções de 2024 e 2026 são idênticas.

Sem dependência e com observação perfeita:

    uniforme: p|D ~ Beta(3,11)
    Jeffreys: p|D ~ Beta(2.5,10.5)

Essas distribuições são resumos do submodelo estacionário e intercambiável. NÃO são estimativas da taxa física de motores corrigidos. Quatro voos com revisões/lotes desconhecidos não identificam o efeito de correções. Mesmo a extensão de heterogeneidade abaixo é uma grade de hipóteses, sem inferir revisão real.

Sensibilidade histórica: s_H ∈ {.7,1}, falso positivo zero. Para cada voo:

    P(k_reportado|p)=Σ_{k≥k_reportado} P(K=k|p,ρ) Binomial(k_reportado;k,s_H).

Multiplicar as quatro verossimilhanças, não adicionar 2/4 como evidência independente de 2/12.

Herança: principal w=0. Secundária w∈{.25,.5}, com likelihood (1-p)^(32w), condicionada a assumir exposições Atlas perfeitamente observadas e comparáveis no evento. Ela adiciona 8 ou 16 pseudonão-anomalias, quantidade grande diante de 12 observações Vulcan. Não chamar de empréstimo pequeno. Datas Atlas encerradas em 30/07/2024; recorte histórico explícito, não inventário até 2026. Sem essa hipótese de observabilidade, retirar a análise de herança quantitativa.

## 5. Regime, revisões e transferência

Θ∈{equivalente histórico, correção eficaz, correção ineficaz}. Para R=histórico, risco por motor é p em todos os regimes. Para R=modificado:

    histórico equivalente: p
    eficaz: e p
    ineficaz: p+(1-p)u

Referência e=.10, u=0. Sensibilidades e∈{.05,.1,.3}, u∈{0,.05,.15}. Essas funções são hipóteses matemáticas, não medições. u permite uma correção piorar o risco. Com u=0, regimes histórico e ineficaz têm a mesma distribuição observável; não são identificáveis separadamente.

Grade de pesos: (.6,.2,.2), (.2,.6,.2), (.1,.8,.1). O mapa contínuo usa P(eficaz)∈[0,1] e divide o restante igualmente. Nenhum peso vem do caso Vega-C.

Revisões HH, HM, MH, MM e um cenário desconhecido com .25 por par. A referência MM é somente ilustração: não se sabe que ambos usarão hardware modificado.

Para revisão igual, a distribuição conjunta é uma mistura entre:

    λ: mesma hipótese Θ e mesmo parâmetro p nos dois voos;
    1−λ: cópias independentes do mesmo conhecimento marginal.

λ∈{0,.5,1}; o mapa usa onze pontos. Para revisões diferentes, λ=0 por convenção conservadora deste estudo. Não é uma lei física. Em revisão desconhecida, Y ainda pode informar R_LV e, se os pares forem correlacionados, R_M. O teste de transferência nula usa pares conhecidos.

## 6. Plate, severidade, consequência e sinal público

Em cada voo, n boosters. Com probabilidade 1−ρ, independentes condicionalmente ao risco q. Com probabilidade ρ, todos compartilham uma única realização Bernoulli(q). Portanto:

    P(K=k|q,ρ)=(1−ρ) Binomial(k;n,q) + ρ[(1−q)1{k=0}+q1{k=n}].

A correlação entre dois motores, dado q, é ρ. Marginais preservados. É um stress test all-or-none, não hipótese sobre causa raiz. As condições compartilhadas são independentes entre voos. A mesma família é aplicada aos dados históricos para evitar aprender p sob uma likelihood e prever sob outra sem declarar.

Severidade: dado K=k, chance de ao menos um evento severo =1−(1−h)^k. h_LV=.20, h_M=.25 são hipóteses. Condições de missão distintas são fixadas em CPTs distintas:

| Condição | LV: sucesso / degradada / perda | M*: sucesso / degradada / perda |
|---|---|---|
| K=0 | .998 / .001 / .001 | .998 / .001 / .001 |
| K=1, não severa | .985 / .010 / .005 | .970 / .020 / .010 |
| K=1, severa | .750 / .150 / .100 | .550 / .200 / .250 |
| K≥2 | .400 / .200 / .400 | .250 / .200 / .550 |

TODAS AS CÉLULAS SÃO HIPÓTESES. Os dois sucessos Vulcan com anomalia não calibram essas tabelas. Risco sem anomalia de booster representa outros subsistemas.

Y tem quatro estados mutuamente exclusivos:
- inconclusivo: probabilidade 1−d, d=.90 (disponibilidade/divulgação suficiente);
- perda/degradada reportada: se há divulgação suficiente e a consequência é degradada/perda;
- anomalia reportada: missão bem-sucedida com divulgação e ao menos uma detecção;
- limpo reportado: sucesso com divulgação, sem detecção, inclusive anomalias não detectadas.

Detecção por motor s=.90; P(ao menos uma detecção|K)=1−(1−s)^K. Falso positivo zero na referência. Sensibilidades s,d∈{.5,.9,1}. Falta de divulgação é independente do estado na referência; a extensão implementa divulgação dependente de K>0, com d_anomalia∈{.3,.6,.9}. Não rotular Y=limpo como ausência física comprovada.

## 7. Admissibilidade e custos

G|Y é cenário de governança. P(liberado|limpo,anomalia,perda/degradada,inconclusivo)=(.90,.30,.05,.40); testar também (0,0,0,0),(.5,.1,0,.1),(1,1,1,1). G não traz informação técnica adicional além de Y na referência antiga; a extensão permite informação adicional via estado latente (seção 12). Os números não descrevem a Space Force real.

Unidade: US$ milhões constantes de 2026, sem desconto financeiro no núcleo. Custos comuns às estratégias cancelados.

| Parâmetro | Referência | Grade/faixa |
|---|---:|---|
| Prêmio incremental da alternativa | 30 | 10,30,100 |
| Risco de perda da alternativa | .005 | .001,.005,.02 |
| Risco de degradação da alternativa | .003 | .001,.003,.01 |
| Custo extra de realocar depois | 5 | 0,5,20 |
| Custo incremental de esperar C_D | 10 | 0–100 no mapa |
| Fração de perda na degradação | .25 | .1,.25,.5 |
| L | 1000 | 250–2000 |

C_D é agregado incremental em relação ao lançamento-base, sem incluir novamente o prêmio da alternativa. Tradução opcional de calendário: atrasos adicionais de 7,45,715 dias; custo/dia 0,.1,.5; penalidade de janela 20 se a data ultrapassar 15/12/2026. Os 715 dias vêm de um caso histórico diferente e são só stress scenario. Não são previsão do Vulcan. O evento informativo e a autorização devem estar disponíveis antes da ação D1; não pressupomos hardware magicamente corrigido durante a espera.

    C_alt = prêmio + L(P_loss_alt + d*P_deg_alt)
    C_v(y) = L[P_loss_M|y + d*P_deg_M|y]
    C_wait = C_D + Σ_y P(y){g_y min[C_v(y),C_alt+extra] +(1−g_y)(C_alt+extra)}
    ganho_espera = C_alt − C_wait

EVSI puro (contrafactual com ações fixas, sem atrasos ou G):

    min(E[C_v],C_alt) − Σ_y P(y) min(C_v(y),C_alt).

Não chamar ganho_espera de EVSI. O valor da restrição atual é C_alt−min(E[C_v],C_alt), apenas nesse conjunto reduzido.

## 8. Cálculo e validação

Gauss–Jacobi com 24 nós por Beta; a likelihood histórica tem grau ≤12, a conjunta LV/M grau ≤10; a integração de grau ≤22 é exata matematicamente (24 nós integram até grau47). Referência e sensibilidades usam transformações lineares em p. Testar ordem48, posterior Beta analítica e enumeração binária dos boosters.

pgmpy 1.1.2: comparar conjunta e posteriores por VariableElimination usando um estado latente discreto que representa a mistura integrada. Isso valida o motor de inferência, não fornece auditoria independente da parametrização física.

Testes: exemplo .6391924983790723; médias Beta 3/14 e 2.5/13; preditiva limpa Beta; normalização; correlação/marginais; transferência nula; EVSI≥0; EVSI≤EVPI; sinal inconclusivo sempre → EVSI0; autorização zero → custo de espera sem benefício; monotonicidade do custo; configuração separada; erros de entrada.

## 9. Saídas e indeterminação

1. Mapa principal C_D×L: envelope dos 360 cenários estruturais. Mapa de dois priors preservado apenas como diagnóstico restrito.
2. EVSI×peso de correção eficaz×relevância.
3. Política por Y e G, incluindo evento raro e inconclusivo.
4. 360 cenários estruturais sem média arbitrária entre modelos; herança em arquivo separado.
5. Classificar por mínimo e máximo nos 360 cenários: aguardar em todos, realocar em todos, discordância ou limiar ±US$ .01 milhão. Não extrapolar robustez para controles físicos e operacionais que não integram esse cruzamento.

## 10. Registro prospectivo e calendário comprimido

| Até | Gate |
|---|---|
| 09/10 | especificação, núcleo e resultados ilustrativos executados |
| 12/10 | revisar premissas físicas, missão, observação e dimensões de sensibilidade |
| 14/10 | auditoria final de fontes e cenários; nenhuma alteração motivada pelo resultado futuro |
| 16/10 | candidato a congelamento, checksum e reprodução limpa |
| 17/10 | publicar release e verificar o registro externo com data antes do voo |

Publicação pendente de repositório/conta e identidade de autoria. Não inventar DOI, hash público ou data verificável. Um commit local e um checksum não são timestamp público independente. Se LV-01 adiantar, antecipar a publicação; se ocorrer antes dela, abandonar o rótulo ex ante para esse voo.

Depois do freeze, atualizações em outro diretório/release, citando o hash original. Regra de codificação: registrar Y preliminar em T+72h e um ponto principal em T+14d; sem informação suficiente nesse ponto, inconclusivo. Nenhuma decisão hipotética usa informação publicada depois de sua própria data. Revisões posteriores são análises separadas.

## 11. Fontes metodológicas

- Heath et al., Simulating Study Data to Support Expected Value of Sample Information Calculations: A Tutorial, DOI 10.1177/0272989X211026292. https://pmc.ncbi.nlm.nih.gov/articles/PMC8793320/
- Ibrahim & Chen, Power prior distributions for regression models, Statistical Science (2000), DOI 10.1214/ss/1009212673. https://doi.org/10.1214/ss/1009212673
- https://pgmpy.org/api/generated/inference/pgmpy.inference.VariableElimination.html
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/

Consensus consultado em 09/10/2026: cota mensal esgotada; nenhuma conclusão atribuída a uma pesquisa não realizada. Wolfram executou o exemplo numérico e os momentos Beta; resultados guardados em evidence/wolfram-verification.json.

## 12. Resposta à auditoria de 09/10/2026

### História parcialmente não identificável
`history_risk_multipliers` aplica q_i=m_i p aos quatro voos, m=(1,1,1,1), (1,1,.5,.5), (.5,.5,1,1). A escala é uma hipótese de contraste, não identificação de lote/revisão. Detecção por voo: (1,1,1,1) ou (.7,1,.7,1). As Betas conjugadas são válidas apenas no submodelo original. A análise principal continua sem Atlas.

### Informação privada reduzida à decisão G
Seja H o estado latente da mistura usada no modelo, contendo revisão e risco compartilhado quando aplicável. Definimos t(H)=P(perda|H,M*)+.25P(degradada|H,M*). Cenários:

    P(G=1|Y,H)=g_Y [1−a t(H)], a∈{0,.5,1}.
    P(Y,G,Z)=Σ_H P(H)P(Y|H)P(G|Y,H)P(Z|H).

A política usa P(Z|Y,G), inclusive quando G é negado. Não condicionamos autorização ao desfecho futuro realizado. Este é um modelo reduzido de associação entre informação privada e aprovação, não uma especificação da telemetria nem das regras da SSC. Com a>0, também muda a frequência marginal de aprovação: a sensibilidade combina seleção informacional e menor disponibilidade. Não interpretar a diferença de custos como EVSI exclusivo de informação privada. Mesmo com λ=0, o estado latente de M* é preservado na extensão de G, permitindo informação privada sobre o alvo sem transferência do LV. Não alegar cobertura completa de G|Y,Θ,R.

### Oportunidades e relógio
A extensão operacional enumera 432 cenários: a em três níveis, data LV em {29/10,31/10,01/12/2026}, integração em {30,90} dias, espera adicional de G em {0,30} dias, disponibilidade futura do slot em {0,.5,1}, reserva em {não,sim}, janela em {original,planejamento}. Não atribuir probabilidades aos cenários.

Sinal principal em T+14 dias; data de decisão = sinal + espera de G. Integração começa conservadoramente nessa data. Nesta grade o mesmo lead-time é usado para ambos os lançadores. Se data de decisão + integração exceder o fim da janela, ambos ficam indisponíveis; não usar lançamento tardio como se fosse pontual. Custos de atraso=.1 milhão × dias após o início da janela até prontidão, piso zero. Para manter transparência, esse custo de oportunidade é cobrado mesmo se ao final for escolhido adiar; o custo de adiar abaixo é incremental a ele.

Reserva custa 10 milhões, paga em todos os ramos, e garante slot apenas no cenário de contrato idealizado (probabilidade 1); não garante integração ou autorização. `reserved_slot` é configurável. Provedor alternativo disponível agora é premissa; `alternative_now=False` permite retirar essa opção. O código também admite adiar agora. O fallback custa 100 milhões hipotéticos, sem assumir perda física da carga. Capacidade, certificação e contratos reais não foram validados.

A janela principal passa a 15/01–15/03/2027 UTC, preservando massa/órbita hipotéticas. A janela original de 15/11–15/12/2026 é estresse explícito. A referência numérica anterior continua com C_D=10 e sem calendário operacional; não apresentá-la como resultado da janela nova.

### Severidade e observabilidade
Para M* e K≥2, P(perda)∈{.1,.3,.55,.8}, P(degradada)=.2, P(sucesso)=.8−P(perda). Divulgação quando K>0 varia separadamente. São 12 controles unifatoriais, não um cruzamento exaustivo com os 432 cenários operacionais ou com os 360 estruturais. A indeterminação fora desses conjuntos permanece aberta.

### Proveniência factual
Northrop: 71 milhões no Q1 para avaliar/implementar ações corretivas; 91 milhões no Q2 sobretudo aumento projetado de custo e quantidade de materiais. Total de EAC 162 milhões não é custo direto da investigação e permanece fora da utilidade. Fonte: https://www.sec.gov/Archives/edgar/data/1133421/000113342126000034/noc-20260630.htm

Extensão Atlas: nove voos e 45 exposições adicionais documentados separadamente em `data/atlas_2025_2026_extension.csv`; não entraram nos priors. Duas datas UTC corrigidas contra a auditoria: ViaSat-3 F2 14/11/2025 e Leo 6 28/04/2026. Fontes primárias por linha. A soma 32+45=77 não demonstra 77 ausências físicas de anomalia nem intercambiabilidade GEM63/63XL.

LV-01: 29/10 é NET secundário, não data confirmada pela ULA. 31/10 e dezembro são alternativas de calendário para sensibilidade, não novas previsões. O freeze deve preceder o voo real, qualquer que seja sua data.

## 13. Integração prospectiva

O protocolo normativo para Y passa a ser `docs/FORECAST_PROTOCOL.md`: validade até
01/01/2027 00:00 UTC exclusivo, adiamento interno preserva primária, corte no início
da data UTC de liftoff+15 dias (fim do 14º dia posterior). Isso torna preciso o T+14
anterior. Previsões físicas não são pontuadas. Somente Y recebe Brier soma e log loss.
`src/scoring.py` verifica consistência temporal e hashes; não autentica publicação externa.
As regras de decisão e extensões operacionais permanecem como nas seções anteriores.
