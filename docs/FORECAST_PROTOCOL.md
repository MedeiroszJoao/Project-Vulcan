# LV-01: protocolo prospectivo de observação e pontuação

**Candidato não publicado — 09/10/2026.** Exercício sob hipóteses, sem calibração física. Nenhum arquivo local comprova registro prospectivo. Este documento substitui o protocolo recebido antes de qualquer congelamento público.

## Episódio e validade

Alvo: primeiro voo identificado publicamente como Amazon Leo LV-01 em Vulcan VC6L com seis boosters, após registro público verificável e antes de **01/01/2027 00:00:00 UTC**, limite exclusivo. A validade até o fim de 2026 é escolha administrativa prévia, não previsão de lançamento. Alteração material da configuração nominal invalida o episódio; registrar VOID_CONFIGURATION sem pontuar e sem reaproveitar silenciosamente a previsão. A revisão interna MM continua hipótese não verificada; divulgação posterior sobre a revisão não permite trocar a previsão primária já publicada.

Adiamento dentro dessa validade **não** expira a previsão e **não** exige nova previsão primária. Registrar atualizações separadas se úteis, sempre preservando e pontuando a primária. Se não houver voo até o fim da validade, registrar NOT_LAUNCHED sem score, sustentado por uma checagem documental publicada depois do vencimento; um voo posterior exige outro episódio prospectivo. A previsão é condicionada a haver voo, não estima a data dele.

## Corte temporal sem ambiguidade

T0 é o instante real de liftoff em UTC. O conjunto de informações principal fecha às **00:00:00 UTC do início da data UTC de T0 + 15 dias**, limite exclusivo: inclui integralmente a 14ª data posterior à data UTC de lançamento. Exemplo: liftoff em 29/10, corte em 13/11 00:00:00 UTC. Isso difere de exatamente 336 horas após liftoff. T+72 horas é digest preliminar, sem revisão da previsão.

É permitido codificar ou publicar o score depois do corte, mas somente com evidência demonstravelmente pública antes dele. Guardar `first_public_at_utc`, bytes arquivados e SHA256 de cada fonte. Uma página editada após o corte não pode provar seu próprio conteúdo anterior sem captura/versionamento anterior. Se a hora de publicação não puder ser delimitada antes do corte, não usá-la para determinar o resultado; registrar a incerteza. Não alterar a observação principal com revelações tardias.

## Codificação de Y

1. `inconclusive`: material público insuficiente para determinar status de missão ou relatos mutuamente contraditórios que não permitam a classificação abaixo. Não confundir pesquisa não realizada com ausência de notícias.
2. `loss_or_degraded_report`: confirmação suficiente de perda/degradação da entrega da missão, independentemente de atribuição a booster. Não exigir informação sobre motores para classificar perda conhecida.
3. `anomaly_report`: sucesso de entrega confirmado e ao menos uma anomalia atribuída explicitamente ao booster sólido/bocal/desempenho por fonte qualificada.
4. `clean_report`: sucesso de entrega confirmado e nenhuma anomalia qualificável encontrada na busca pré-especificada. Não implica K=0.

Fonte qualificada: comunicado, atualização ou declaração atribuível à ULA, Northrop, Amazon/operador da carga ou autoridade da missão; reportagem pode localizar a declaração, mas deve-se arquivar o conteúdo e sua atribuição. Imagens e especulação sem atribuição não bastam. Definir sucesso pela entrega à órbita prevista declarada pelo operador/lançador, não pela simples sobrevivência da carga. Anomalia posterior do satélite não atribuída à entrega fica fora. Se o critério não resolver o caso, inconclusivo.

Para classificar limpo, exigir documento de sucesso e registro de busca nos canais públicos da ULA, Northrop, operador e autoridade aplicável até o corte, incluindo termos LV-01/Amazon Leo/Vulcan e anomaly/booster/nozzle. Registrar indisponibilidade de páginas. Se a busca mínima não puder ser realizada com evidência temporal, inconclusivo. Fazer idealmente duas codificações independentes; divergência sem resolução documental no corte permanece inconclusiva. Isso reduz, mas não elimina, subjetividade da observação.

O modelo de referência representa inconclusão por missingness independente. Conflitos e limitações reais de observação podem violar essa hipótese; isso é possível discrepância do modelo a registrar, não motivo para reinterpretar a categoria após o resultado.

## Previsão e scores

Primária: `forecast/reference.json`, cenário MM com pesos (.2,.6,.2), hipóteses fixas, cinco arquivos de previsão no total. As quatro alternativas são sensibilidades predeclaradas; nenhuma substitui a primária depois de conhecido o resultado. Todas as PMFs e os parâmetros completos ficam nos JSON.

Y é observável publicamente sob a regra acima. K=0..6 é contagem física latente e **não será pontuado neste episódio**: não há protocolo de ascertainment independente congelado para ela. O count-report exploratório também não recebe score primário. Falta de relato não vira zero físico.

Brier multicategoria SOMA: B=Σ_i(p_i−1{i=j})², faixa [0,2]. Log loss: −ln(p_j), em nats. Ambos menores são melhores. p_j=0 gera infinito matemático, representado por JSON null com `zero_probability_observed=true`, sem clipping. Um voo permite pontuar, não demonstrar calibração. Um evento de probabilidade pequena não refuta logicamente uma previsão que atribuiu probabilidade positiva; registra surpresa e perda segundo regra fixa.

## Uso do programa pós-voo

Preparar um JSON documental com:

```json
{
  "registered_forecast_sha256": "SHA256 DOS BYTES EFETIVAMENTE REGISTRADOS",
  "freeze_url": "https://URL-PUBLICA-VERIFICADA",
  "commit_sha": "SHA REAL DE 40 CARACTERES",
  "registered_at_utc": "INSTANTE UTC VERIFICADO ANTES DO VOO",
  "coded_at_utc": "INSTANTE UTC DA CODIFICACAO APOS O CORTE",
  "flight_at_utc": "INSTANTE REAL UTC",
  "configuration_matches": true,
  "outcome": "CATEGORIA DOCUMENTADA",
  "evidence": [{
    "url": "https://FONTE",
    "first_public_at_utc": "INSTANTE UTC COMPROVADO ANTES DO CORTE",
    "snapshot_file": "CAMINHO RELATIVO AO JSON",
    "snapshot_sha256": "HASH DOS BYTES ARQUIVADOS"
  }]
}
```

Os campos acima são placeholders deliberadamente inválidos, não resultado ou registro real. Executar:

```bash
python score_episode.py --forecast forecast/reference.json --record scoring/evidence_record.json --output scoring/episode_01_T14.json
```

O programa valida hashes dos snapshots, hash da previsão, ordem de categorias, datas, validade, corte, sintaxe dos identificadores e recusa sobrescrever a saída. Para observações pontuadas e VOID_CONFIGURATION, exige ao menos uma evidência de publicação posterior ao lançamento mas anterior ao corte de T+14; um arquivo de agenda pré-voo não prova o resultado. Para NOT_LAUNCHED, omitir flight_at_utc, codificar após expiração, e incluir ao menos um registro documental de não lançamento publicado *a partir do vencimento* e até a data de codificação. O estado de não lançamento NÃO recebe score. A regra especial de evidência posterior à validade não reabre a janela de observação da previsão: serve apenas para verificar retrospectivamente que nenhum voo ocorreu antes dela. Para VOID_CONFIGURATION, informar `outcome=VOID_CONFIGURATION`, `configuration_matches=false`, `flight_at_utc` e `configuration_change_description`; anexar prova pública de divergência física no voo, sem score. Mudar para outro lançador ou outra configuração não autoriza reclassificar seletivamente depois de observar se houve falha: a divergência deve ser definida pelo critério objetivo de seis boosters e VC6L e apoiada por documentação verificável.

**Limite de verificação:** o programa é offline. Ele não autentica que URL, SHA, timestamp ou declaração fornecidos são verdadeiros/publicados. Isso exige abrir a release/registro externo e comparar os bytes. Sua saída declara essa limitação. Um JSON preenchido com dados inventados jamais constitui registro prospectivo.

## Registro público

Antes do voo: publicar os bytes exatos, SHA256, protocolo e commit. Verificar release pública e timestamp externo; DOI de versão é desejável e deve ser confirmado após processamento. Não alterar a previsão para inserir retrospectivamente o próprio DOI. Manter registro posterior de publicação separado. Autoria e licença ainda pendentes.

Fonte metodológica: Gneiting & Raftery (2007), https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf .
