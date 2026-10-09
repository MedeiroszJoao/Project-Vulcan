# Verificação local após patch adversarial — 09/10/2026

42/42 testes aprovados, incluindo pgmpy 1.1.2, no ambiente documentado.
`bash reproduce.sh` terminou com sucesso, incluindo integração independente,
envelope, previsões e scores hipotéticos. Logs em results/tests.txt e
results/reproduction_log.txt. Este ensaio não é CI pública nem instalação limpa
independente. O resultado 41/42 da auditoria recebida permanece preservado em
evidence/adversarial_local_suite_log.txt como registro de outro ambiente.

Os cinco arquivos forecast/*.json foram comparados byte a byte por SHA256 com
o commit anterior e com o ZIP adversarial recebido; todos coincidem.
A previsão principal mantém fc9d0e290adef51459b86c8ad4a1a6ddc03ea087163e48da6e59f6d106f82d1f.

GitHub autenticado como MedeiroszJoao; consultas de repositórios acessíveis e
próprios retornaram listas vazias. Não houve push, CI remota, tag pública,
release ou DOI. Ainda é necessário fornecer/acessar o repositório de destino.
