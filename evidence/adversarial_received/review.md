# Vulcan — conferência independente dos arquivos anexados (09/10/2026)

## Parecer

**Candidato prospectivo tecnicamente sólido como exercício, mas NÃO congelado/publicado.** A previsão e os scores possuem implementação reprodutível e o Wolfram reproduziu a distribuição de sete K e quatro Y com integração Beta racional. A verificação externa de pgmpy **não** foi reproduzida neste ambiente: 41 de 42 testes passaram; um falhou por dependência ausente. O material recebido registra 37 testes aprovados em outro ambiente, mas isso não substitui CI pública.

## Resultado central e suas limitações

O modelo hipotético (MM, e=.1, P(Θ)=(.2,.6,.2), Beta(3,11), n=6) produz P(Y)=(.5973632855118782,.2072166863854239,.09542002810269795,.1). O limiar de espera US$ 1.279000842 mi vale apenas para a referência sem incerteza operacional. Os 360 cenários estruturais, 432 operacionais e 12 testes de física são conjuntos separados; suas contagens não têm interpretação probabilística, nem estabelecem segurança do lançador.

## Problemas corrigidos sem alterar a previsão

1. O protocolo dizia VOID_CONFIGURATION, mas o scorer não registrava o resultado; ele agora produz uma disposição sem score e exige divergência física documentada após o liftoff.
2. NOT_LAUNCHED agora exige publicação verificável ao menos após a expiração; um agendamento antigo não comprova não lançamento até o fim do intervalo.
3. Um resultado de voo pontuado requer ao menos uma evidência com publicação depois do liftoff e antes do corte, evitando que uma página pré-voo seja usada sozinha para qualificar o resultado.
4. Fonte Atlas V 2025–26 apontava para diretório errado.

## Pendências relevantes

- Validação humana da objetividade da regra de VOID para evitar anulação oportunista após conhecer desempenho; um perito externo deve confirmar incompatibilidade real de VC6L/seis boosters.
- Auditoria externa de fontes datadas, completa com evidência de rastreabilidade temporal independente (o scorer não certifica que bytes foram públicos).
- Reproduzir 42/42 numa instalação com pgmpy 1.1.2 e CI externa, licença e identidade de autor.
- Publicar tag/release antes do voo e verificar DOI de versão no Zenodo.
- Revalidação física de CPTs, revisão/lotes, sinal regulatório e calendário; previsão não é taxa de falha certificada.

## Fontes oficiais e científicas

- NASA-STD-7009B: https://standards.nasa.gov/standard/NASA/NASA-STD-7009
- Handbook 2026: https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009
- Zenodo integração: https://help.zenodo.org/docs/github/enable-repository/
- Release/DOI: https://help.zenodo.org/docs/github/archive-software/github-upload/
- Gneiting & Raftery 2007: https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf

Esta revisão é uma contribuição à garantia metodológica; não é aprovação NASA, recomendação de lançamento ou afirmação de erro físico em hardware ULA.
