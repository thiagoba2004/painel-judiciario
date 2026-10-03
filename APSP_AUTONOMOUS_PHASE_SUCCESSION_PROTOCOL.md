# APSP — Autonomous Phase Succession Protocol

**Version:** 1.0  
**Strategy:** EA-000000-000003  
**Status:** CANONICAL / IMPLANTADO

## Purpose

Garantir que uma Estratégia Autônoma não dependa de um novo comando do usuário entre Fases quando a próxima ação já estiver autorizada, disponível e determinística.

## State machine

`IN_PROGRESS → ACT → VERIFY → PERSIST → ADVANCE → IN_PROGRESS`

Terminal/exception states:

- `COMPLETED`
- `BLOCKED`
- `WAITING_HUMAN_DECISION`
- `RUNTIME_INTERRUPTED`
- `FAILED`

## Mandatory loop

1. Recuperar estado canônico.
2. Selecionar a primeira Fase não concluída.
3. Ler entry gate e blockers.
4. Selecionar a primeira ação executável.
5. Executar.
6. Verificar.
7. Persistir resultado/checkpoint.
8. Promover estado.
9. Selecionar novamente.

## No-prompt rule

Não perguntar ao usuário “posso continuar?”, “qual o próximo passo?” ou equivalente quando a ação seguinte já estiver autorizada pelo Plano e não exigir decisão humana.

## Blocker rule

Bloqueio somente quando houver dependência material verificável. A ausência de um comando adicional do usuário não é blocker.

## Runtime rule

Se o ambiente encerrar a execução antes da conclusão, registrar `RUNTIME_INTERRUPTED` e preservar o próximo passo. Em nova execução, recuperar o checkpoint e continuar automaticamente.

## Human decision rule

Parar somente quando a ação exigir decisão, autorização, credencial, conteúdo ou escolha que o usuário não tenha previamente delegado.

## Evidence rule

Nenhum estado de conclusão pode ser promovido sem evidência verificável do completion gate.

## Anti-loop

Não repetir ação concluída sem motivo documentado.

## Finality

Uma Estratégia só termina quando todas as Fases executáveis estiverem concluídas ou quando um estado terminal previsto no Plano tiver sido formalmente registrado.
