---
name: revisao-semanal
description: Revisão semanal de 30 minutos do Sistema de Vida. Compara o log da semana com o plano, consulta Todoist e agenda só da semana, e decide UM ajuste e até 3 compromissos. Use quando o usuário digitar /revisao-semanal ou pedir a revisão da semana.
---

# /revisao-semanal

Português. Mantenha o uso de contexto baixo: janelas curtas e resultados agregados.

## Passos
1. Leia `log/semana-template.md`, as linhas da semana em `log/AAAA-MM.md` e o experimento ativo (`CLAUDE.md` → Estado). Não releia o diagnóstico.
2. Calcule do log: registros/7, sono médio, noites ≤0h, sessões de corpo, refeição-âncora ok, contagem de modos.
3. Consulte **somente a semana**:
   - Todoist: `find-activity` (objectType=task, eventType=completed, `initiatorId` do usuário via `user-info`, dateFrom/dateTo da semana). Se a resposta for grande, use `jq` no arquivo salvo e traga só contagens por projeto e por faixa de horário. Não liste tarefas uma a uma.
   - Calendar: `list_events` da semana; resuma blocos de Treino/Sono/compromissos.
4. Escreva em `log/AAAA-WNN.md` seguindo `semana-template.md`: dados, leitura (**fato × hipótese**), o que atrapalhou (classifique cada falha), **um** ajuste e até **3** compromissos.
5. Compare com a decisão anterior: o ajuste da semana passada funcionou? Diga, sem culpa.
6. Se o experimento ativo cumpriu o critério de decisão (ver arquivo), sinalize e sugira `/revisao-temporada`.
7. Se algo no Todoist precise mudar, **proponha** em `05-proposta-todoist.md`; não escreva no Todoist.

## Regras
- Nunca mais de 1 ajuste por semana.
- Nunca puxar 90 dias; nunca despejar listas longas no contexto.
- Se o log tiver <4 registros, o primeiro achado é a dificuldade de registrar: simplifique o log antes de qualquer intervenção.
