# Revisão integrada do candidato prospectivo — 09/10/2026

**Resultado: candidato tecnicamente reproduzido; congelamento público pendente.**

O pacote recebido acrescenta a previsão probabilística e os scores necessários à série prospectiva. Seu núcleo, porém, antecedia as correções operacionais da auditoria. A integração preserva ambas as contribuições e mantém os originais recebidos como evidência.

## O que foi conferido e corrigido

| Ponto | Resultado |
|---|---|
| Limiar econômico | US$1,279001 milhão reproduzido somente na referência original |
| Arrependimento máximo na grade original | Realocar: US$0,744 milhão; aguardar: US$15 milhões, sem generalização além da grade |
| Previsão de Y | PMF principal reproduzida; modelo hipotético MM, sem alegação de calibração |
| K físico | Publicado como latente, expressamente não pontuado neste episódio |
| Scores | Brier soma [0,2], log loss em nats, evento de probabilidade zero sem clipping |
| Validade | Primeiro LV-01 na configuração nominal depois do registro e antes de 01/01/2027 UTC |
| Adiamentos | Preservam primária dentro da validade; não autorizam substituição seletiva |
| Corte | Fim da 14ª data UTC após liftoff, codificação tardia permitida só com fontes anteriores |
| Integridade | Hash da previsão registrada e dos snapshots checados; publicação externa não autenticada offline |
| Testes | 37 passaram após instalar pgmpy; comando de reprodução completo executado |
| Correções operacionais | Mantidas: informação em G, slot, reserva, prazo, fallback e janela de 2027 |
| Documentação | Resumo, nota técnica, SPEC e protocolo harmonizados; licenciamento ainda proposto |

## Leitura correta da contribuição

O estudo entrega uma previsão probabilística pontuável e uma decisão condicionada a hipóteses. Não entrega evidência de acurácia antes do voo. Mesmo depois dele, um único score não estabelece calibração, nem um evento improvável refuta sozinho uma distribuição de suporte positivo.

A PMF primária permanece `[0.5973632855, 0.2072166864, 0.0954200281, 0.1]` para limpo, anomalia com sucesso, perda/degradação e inconclusivo. O limiar de espera usa o modelo original com alternativa garantida; não deve ser vendido como conclusão das extensões de calendário e slot.

Os 360 cenários estruturais, os 432 operacionais e os 12 controles físicos são experimentos distintos. Nenhuma contagem sobre cenários é probabilidade posterior de uma ação estar correta. O programa de G informativo é reduzido e altera também frequência de aprovação; não identifica separadamente o valor da telemetria privada.

## Fontes metodológicas abertas nesta revisão

- Gneiting & Raftery (2007): https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf
- NASA-STD-7009B, documento de 05/03/2024, ativo: https://standards.nasa.gov/standard/NASA/NASA-STD-7009
- NASA-HDBK-7009B, documento de 03/02/2026, ativo: https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009

Essas referências sustentam terminologia e práticas de verificação; não conferem certificação NASA ao projeto.

## O que falta

Revisão humana do protocolo de codificação e das premissas; identidade de autoria e licença; repositório público, release e timestamp/DOI de versão verificados. O arquivo CITATION.cff permanece rascunho. Nenhuma mensagem foi enviada a revisores e nenhum resultado externo foi publicado. EVPPI, pooling hierárquico e retrodições permanecem no roteiro, não são entregas concluídas.


## Fechamento do patch adversarial — 09/10/2026

O patch recebido foi aplicado ao repositório Git original e a reprodução completa
foi executada: 42/42 testes, inclusive pgmpy. As cinco previsões mantêm os mesmos
bytes do commit anterior e do ZIP recebido. VOID_CONFIGURATION agora gera um
registro sem score; NOT_LAUNCHED exige verificação documental posterior à expiração;
resultados pontuados exigem evidência pós-liftoff. O caminho Atlas foi corrigido.

Isso valida os controles de consistência, não a veracidade dos documentos ou
objetividade de cada VOID. Essa avaliação documental permanece humana. A conexão
GitHub identifica MedeiroszJoao, mas retornou zero repositórios acessíveis. Nenhuma
CI pública ou publicação ocorreu. Próximos dados necessários: URL do repositório,
nome de autoria e decisão de licença para o código original.
