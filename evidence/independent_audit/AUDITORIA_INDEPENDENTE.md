# Projeto Vulcan — segunda auditoria adversarial independente

**Data de corte:** 9 de outubro de 2026. **Pacote examinado:** `Vulcan_Decision_Research(1).zip`, `SPEC(1).md` e `RUN_REPORT(1).md` fornecidos nesta conversa. **Status:** aprovação condicionada da implementação matemática; **não** aprovado para publicação como inferência empírica de segurança do Vulcan. Trabalho independente, sem afiliação com ULA, Northrop, SSC ou operadores de missão.

## Sumário executivo

1. **A matemática central foi reproduzida independentemente** por uma implementação alternativa com integração adaptativa (`independent_numeric_check.py`), que não importa o modelo original: discrepância máxima na conjunta `4.16e-17`; EVSI `US$3.98985117488024 mi`; espera `US$44.47099915780434 mi`; ganho líquido de esperar `−US$8.72099915780434 mi`.
2. **Testes recebidos:** 14 definidos. No ambiente disponível nesta auditoria, 13 passaram e o teste pgmpy não rodou porque a biblioteca não está instalada (`ModuleNotFoundError`). O arquivo recebido alega 14/14 em outro ambiente; não é possível reproduzir esse teste localmente sem instalar a dependência. Isso NÃO é diagnóstico de bug na inferência.
3. **Sensibilidade estrutural:** nos 360 cenários do pacote, a preferência em L=US$1000 mi, C_D=US$10 mi favorece realocar em 359, aguardar em apenas um. Num mapa ampliado 61 consequências × 51 atrasos: 2.775/3.111 células favorecem realocar **em todos os 360 cenários**, 336 exibem discordância, nenhuma favorece aguardar **em todos**. Os dois priors originais, isolados, mostravam 98 células com aguardar em ambos. A diferença é substantiva e decorre de aumentar o conjunto de cenários; não é contradição matemática.
4. **A base Atlas V tem recorte explícito até julho/2024**, mas uma nova checagem no manifesto ULA localizou 9 missões Atlas V 551 entre 2025 e julho/2026 (=45 outras exposições de SRBs). São exposições adicionais, **não** 45 demonstrações de ausência física de anomalia e **não** eventos GEM 63XL. Nenhuma foi importada para o prior principal ou para o secundário entregue.
5. **Bloqueios de inferência:** revisões/batches por motor no histórico não identificados; CPTs de consequências e de inspeção sem calibração; alternativa sem slot, custos ou compatibilidade documentados; decisão regulatória G assume artificialmente não conter dados privados; M* GEO de 3000 kg no VC4S não verificado para a missão hipotética; tempo para decisão operacional após LV-01 extremamente curto.
6. **Congelamento público pendente:** local Git commit não fornece prova pública de anterioridade; há dois arquivos que aparecem fora do commit no repositório recebido (`SHA256SUMS` e `BUILD_RECORD.json`); não há release nem DOI emitido.

## 1 — Classificação das constatações

| ID | Gravidade | Constatação | Natureza | Medida exigida |
|---|---|---|---|---|
| F01 | Alta | Posterior Beta(3,11) consolida 12 exposições como uma população base apesar de revisões/lotes desconhecidos | Hipótese forte de inferência, não bug algébrico | Sensibilidade por voo, revisão e detecção; declarar limite de identificabilidade |
| F02 | Alta | A decisão de aprovação G é representada por P(G\|Y); não pode transmitir telemetria privada que regulador possa ter | Insuficiência de modelo de informação | Cenários G\|Y,Θ,R e G\|Y; separar decisão de informação não pública |
| F03 | Alta | Alternativa fica disponível tanto agora quanto depois com penalidade fixa de US$ 5 mi; slot e integração não modelados | Falha de realismo decisório | Ação de reserva, chance de perda do slot, incompatibilidade/lead-time, custos irrecuperáveis |
| F04 | Alta | M* tem janela 15/11–15/12/26 e sinal principal do LV-01 somente T+14 dias | Restrição de calendário | Condicionar a disponibilidade de Y e de G antes de D1 e tempo mínimo para integração |
| F05 | Alta | Região de indeterminação publicada compara só dois priors, embora existam 360 cenários | Apresentação incompleta | Acrescentar envelope estrutural deste pacote; comunicar que nenhum cenário de robustez global foi estabelecido |
| F06 | Média-alta | Consequência K>=2 para M* usa 55% perda sem teste específico dessa célula | Hipótese dominante, não dado | Ampliar sensibilidade explícita da CPT K>=2 e severidade |
| F07 | Média-alta | Atlas secundário para em 30/07/2024, ausentes 45 outras exposições 2025-26 | Recorte histórico correto, incompleto para revisão corrente | Registrar extensão separada, sem adicioná-la automaticamente à potência do prior |
| F08 | Média | λ=0 descarta toda transferência de p e Θ; λ=1 assume compartilhamento total condicionado ao cenário | Escolha de mistura epistemológica | Interpretar λ como dependência informacional, não probabilidade física calibrada |
| F09 | Média | 'Sem boosters' excluído; 3000 kg direct GEO com 4 boosters não certificado para M* | Viabilidade não validada | Deixar flag false; missão e alternativa rotuladas hipotéticas, não manifesto |
| F10 | Média | Disclosure missing-at-random e zero falso positivo no caso base | Simplificação forte de observabilidade | Introduzir missing-not-at-random e detecção histórica por voo |
| F11 | Média | Data LV-01 29/10 conflita com registros que mostram apenas mês ou 31/10 indicativo | Incertidão de calendário | Registrar 29/10 como NET de um agregador, não T-0 confirmado pela ULA |
| F12 | Baixa / publicação | Dois arquivos não rastreados no Git local; autor `Research build` é genérico | Proveniência incompleta | Novo commit, identidade/licença, tag, release com Zenodo ativado antes |
| F13 | Controlada | 13/14 testes reproduzidos: 14º depende de pgmpy ausente do ambiente | Dependência de ambiente | Instalar ambiente travado e rerodar 14/14 |
| F14 | Aceitável | Gauss–Jacobi integra polinômios sem substituir Beta por média e as juntas numéricas conferem | Verificado | Preservar como baseline matemático |

## 2 — Confirmações factuais e diferenças causais

- **Space Systems Command / GPS III-8**: comunicado de 20/03/2026 confirma transferência ULA→SpaceX durante investigação e USSF-70 para Vulcan NET verão de 2028. Não quantifica o custo de realocação. Fonte: https://www.ssc.spaceforce.mil/DesktopModules/ArticleCS/Print.aspx?Article=4439687&ModuleId=705&PortalId=3 (acesso HTML pode ser bloqueado; o texto foi indexado publicamente).
- **Northrop 10-Q junho/2026**: 71 mi de EAC desfavorável no 1º trimestre ligados à análise/implementação de ações corretivas; 91 mi no 2º trimestre relacionados principalmente a aumento projetado de materiais/custos do GEM 63XL. Somam 162 mi contábeis, não caixa desembolsado por missão. https://www.sec.gov/Archives/edgar/data/1133421/000113342126000034/noc-20260630.htm
- **Vulcan**: voos e contagens do arquivo: Cert-1 (2/0), Cert-2 (2/1), USSF-106 (4/0), USSF-87 (4/1). O comunicado ULA sobre USSF-87 confirma anomalia significativa de performance num dos quatro motores, mas missão inserida diretamente em órbita geossíncrona. https://www.ulalaunch.com/about/news-detail/2026/02/12/ula-vulcan-rocket-successfully-launches-the-future-of-defense ; confirmação de configuração em https://www.ulalaunch.com/missions/next-launch/vulcan-ussf-87
- **LV-01**: agregador Next Spaceflight registra VC6L de seis boosters, Centaur otimizado LEO, NET 29/10/2026, mas exibe em outra interface apenas 'outubro/2026'. Outros espelhos indicam 31/10 como aproximação sem T-0 confirmado. ULA confirmou variante LEO Centaur, distinto da versão alta energia. https://api.nextspaceflight.com/launches/details/7425 ; https://www.nextspaceflight.com/launches/details/7425 ; https://blog.ulalaunch.com/blog/vulcan-new-centaur-v-version-readies-for-amazon-leo?hs_amp=true
- **Vega-C**: 21/12/2022 a 05/12/2024 = 715 dias de calendário; teste de motor modificado 28/06/2023 falhou. É analogia de cauda de prazo e falha de correção, **não** likelihood para Vulcan. https://www.esa.int/Newsroom/Press_Releases/Flight_VV22_failure_Arianespace_and_ESA_appoint_an_independent_inquiry_commission ; https://www.esa.int/Newsroom/Press_Releases/Vega-C_Zefiro40_Test_Independent_Enquiry_Commission_announces_conclusions ; https://www.esa.int/Newsroom/Press_Releases/Double_win_for_Europe_Sentinel-1C_and_Vega-C_take_to_the_skies
- **Atlas pós-2024**: 9 Atlas V 551 (Kuiper 1-3, ViaSat-3 F2, Leo 4-8), todas com 5 SRBs, total adicional **45 exposições em voo**. O conjunto antigo permanece **32 exposições até 2024**; a série potencial é **77 exposições**, sujeito a auditoria de observabilidade, compatibilidade GEM 63 vs GEM 63XL e data. Checagem de cada voo em `atlas_2025_2026_extension.csv`. O comunicado da ULA sobre Kuiper-2 identifica explicitamente **GEM 63** para Atlas 551: https://blog.ulalaunch.com/blog/kuiper-2-atlas-v-to-launch-amazons-next-step-in-journey
- **M* GEO**: o USSF-106 voou direto a GEO em configuração VC4S, mas isso não certifica 3000 kg e parâmetros orbitais exatos de um satélite futuro. https://www.ulalaunch.com/missions/missions-details/2025/08/13/vulcan-rocket-ushers-in-new-era-of-national-security-space-launch

## 3 — Reprodução, arquivos e proveniência

| Teste | Constatação |
|---|---|
| Conjunta 4×3 | Independentemente reconstituída com `scipy.integrate.quad` e Beta(3,11), erro máximo absoluto 4.16e−17 |
| EVSI | 3.98985117488024 mi, igual ao arquivo de referência até arredondamento |
| Esperar | 44.47099915780434 mi, igual ao arquivo |
| Realocar agora | 35.75 mi, conforme a função de custo alternativa |
| Preferência | Realocar no cenário de referência; ganho da espera −8.72099915780434 mi |
| Testes | 13/14 OK nesta auditoria; um erro devido exclusivamente à ausência de `pgmpy` |
| Hashes | 29 capturas brutas do manifest têm SHA-256 coincidente; 66 entradas de SHA256SUMS coincidem com arquivos locais |
| Registro público | Nenhum DOI, release ou timestamp público verificável neste pacote |

Há uma regra de nomenclatura importante: o EVSI puro usa ações hipoteticamente fixas e não sofre os custos de atraso/autorização. O ganho líquido de esperar é uma função distinta, **pode ser negativo**, e incorpora G e custos. O teste numérico não autentica os parâmetros físicos (CPTs, custos, detectabilidade).

### Envelope estrutural novo

O mapa de dois priors original em 3.111 pontos classifica 98 como 'aguardar com ambos', 2.990 como 'realocar com ambos' e 23 como divergência/limiar. Ao testar todos os 360 cenários estruturais (não só dois priors), **zero** pontos sustentam 'aguardar' uniformemente; 2.775 sustentam realocar e 336 produzem discordância entre cenários. Esse é um envelope relativo a uma grade especificada; não constitui prova universal. Arquivos: `structural_envelope.csv` e `structural_envelope.png`.

## 4 — Duas correções conceituais obrigatórias

**A. Não inferir revisão técnica de uma Beta única.** A leitura de quatro voos como 12 Bernoulli intercambiáveis só é defensável sob o submodelo explicitamente simplificado (estacionariedade, observação perfeita, rho=0). Versões, lotes, inspeções e localizações distintas fazem o modelo mais geral parcialmente não identificável. O posterior Beta(3,11) é um **resumo do submodelo**, não a taxa física de um GEM 63XL revisado.

**B. Condicionar decisões à oportunidade realmente existente.** Um planejador que transfere satélite sensível para outro foguete precisa ter alternativa certificada, cronograma, integração, adaptadores e contrato. A GPS III-8 ilustra que trocas são possíveis institucionalmente, mas não comprova que M* possa escolher e integrar outro provedor entre LV-01 +14 dias e 15/11. Se G se basear também em dados privados, observar G informa risco adicional; é inválido impor G ⟂ Θ\|Y como fato. Manter os dois casos como *cenários*, sem atribuir percentuais reais à Space Force.

## 5 — Calendário de freeze, assumindo hoje 09/10 e meta 17/10

- **09–11/10:** auditar cobertura das fontes e corrigir F01–F05 como cenários ou limitações formais; confirmar que M* permanece estritamente hipotética.
- **12–13/10:** ampliar teste da CPT K>=2, censura/observabilidade e efeito de dados privados no gate; não calibrar com resultados futuros.
- **14/10:** rerodar num ambiente travado pgmpy, conferir checksum dos resultados e congelar tabela de fontes com corte temporal explícito.
- **15–16/10:** incluir licença, identidade de autoria, `CITATION.cff`, novo commit rastreando build-record e checksums; revisar documentação, selar candidate de release.
- **Até 17/10:** conta do responsável habilita repo na integração GitHub–Zenodo ANTES da nova release, faz release pública e verifica DOI **após processamento**. Se não houver DOI/release, não declarar registro ex ante publicamente verificável. Fontes: https://help.zenodo.org/docs/github/enable-repository/ e https://help.zenodo.org/docs/github/archive-software/github-upload/

**Limite explícito:** nada aqui faz uma avaliação de engenharia da segurança do voo, estima causa raiz, substitui autoridades de missão ou pode instruir autorização real de lançamento.

## 6 — Conferência bibliográfica dos métodos

- Heath et al., *Simulating Study Data to Support Expected Value of Sample Information Calculations: A Tutorial* (2021/2022), https://pmc.ncbi.nlm.nih.gov/articles/PMC8793320/ — distingue valor da informação de benefício líquido após custos e enfatiza censura/observabilidade. O modelo independente aqui usa enumeração, não o método de Monte Carlo do tutorial.
- Chen & Ibrahim, *Power prior distributions for regression models*, *Statistical Science* 15(1), 46–60 (2000), https://doi.org/10.1214/ss/1009212673 — justifica o uso conceitual de likelihood elevada a uma potência, mas não valida a troca física GEM 63→GEM 63XL nem resolve viés de divulgação.

### Resumo de liberação

**Aprovado:** núcleo de enumeração e aritmética de referência, mapa preliminar e valor da informação como **experimento decisório sob cenários**. **Não aprovado:** interpretação como probabilidade real de perda, aconselhamento de certificação, inferência causal sobre correções ou publicação como registro público já congelado.
