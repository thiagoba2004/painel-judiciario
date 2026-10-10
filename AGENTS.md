# AGENTS.md — Painel Judiciário

**project_code:** `PRJ-000005`  
**project_sequence:** `5`  
**project_name:** `Painel Judiciário`  
**repository:** `thiagoba2004/painel-judiciario`  
**generated_from_kernel:** `1.11`  
**migration_origin:** `EA-000000-000019 / Rota B`

## Missão de governança

Preservar e desenvolver o conteúdo comprovado deste repositório sem inferir
regras de domínio, estado histórico, integrações ou capacidades não
documentadas. Arquivos existentes prevalecem sobre memória conversacional.

## Ordem para novos pedidos

Registrar o pedido em `REQUEST_LOG.jsonl`, confirmar a persistência, identificar
a Estratégia Autônoma e seu Plano de Fases e somente então executar trabalho
substantivo. Nunca afirmar salvamento, commit, publicação ou implantação sem
verificação técnica.

## Fontes da verdade

1. arquivos persistidos neste repositório;
2. `PROJECT_STATE.json`;
3. `STRATEGY_LOG.jsonl` e `REQUEST_LOG.jsonl`;
4. histórico Git comprovado;
5. somente depois, contexto conversacional.

## Preservação

Não reescrever histórico append-only, não fabricar estado desconhecido e não
substituir regras locais mais rigorosas. Mudança destrutiva exige alvo exato,
justificativa, verificação e meio de recuperação.

<!-- MOGP:BEGIN AUTONOMOUS_STRATEGY_NUMBERING_V1 -->

## Numeração canônica de Estratégias Autônomas

Este Projeto usa identidade canônica imutável:

```text
Projeto: PRJ-000005
Estratégia: EA-000005-EEEEEE
Fase: F-000005-EEEEEE-FFF
```

Novas Estratégias exigem sequência local única e registro persistente antes
da execução. Identificadores legados permanecem como evidência e não são
reescritos. O catálogo global é índice; plano, estado e logs locais continuam
como fontes primárias do progresso.

<!-- MOGP:END AUTONOMOUS_STRATEGY_NUMBERING_V1 -->

## Continuidade

Ao responder “Onde paramos?”, informar Projeto, Estratégia, Fase, estado
comprovado, ponto exato e próximo passo lógico. Quando não houver Estratégia
local comprovada, declarar explicitamente `UNKNOWN_NOT_INFERRED`.

## Gate de atribuição de ações por executor — 10/10/2026

**Decisão humana transversal:** manter banco local `governanca/EXECUTOR_ACTION_CATALOG.json`, herdando as ações globais do catálogo `GOV-EXEC-ACTIONS-000001` e a política `GOV-POL-ECO-000001`. Para trabalho persistente, decompor a tarefa em ações identificáveis; antes de cada ação material, conferir `action_id`, `required_executor`, autorização, capacidades, limites, segurança e gates locais. É proibido encaminhar uma ação não classificada ou a executor divergente. A exceção exige decisão humana **expressa e específica**, registrada no catálogo global de overrides, com evidência verificável; aprovação desta política não é autorização genérica de exceção.

Preferir mecanismo determinístico seguro quando suficiente; usar o Chat em análise/documentação acessível e reservar Work/Codex para capacidades técnicas necessárias. A catalogação não substitui metodologia, checkpoints, políticas de sigilo ou autorizações existentes. O verificador `runtime/executor_action_gate.py` no repositório da Governança só bloqueia **despachos que efetivamente o invocarem**: não alegar interceptação automática das interfaces nativas Chat, Work ou Codex, nem mudança de executor sem comprovação.
