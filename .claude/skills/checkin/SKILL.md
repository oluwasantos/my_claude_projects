---
name: checkin
description: Check-in diário de 2 minutos do Sistema de Vida. Registra modo do dia e 3 números (sono, corpo, comida), faz UMA pergunta da fila e atualiza o log. Use quando o usuário digitar /checkin ou disser que quer registrar o dia.
---

# /checkin

Projeto: `sistema-de-vida/`. Todos os caminhos abaixo são a partir da raiz do repo. Não use o `CLAUDE.md` da raiz (é o da viagem); use `sistema-de-vida/CLAUDE.md`.

Objetivo: registrar o dia em ≤2 minutos, com custo mínimo de contexto. Português.

## Passos
1. Leia **apenas** `sistema-de-vida/log/checkin-template.md`, o arquivo de log do mês atual em `sistema-de-vida/log/` (se existir) e o experimento ativo indicado em `sistema-de-vida/CLAUDE.md` (seção Estado). Não leia o diagnóstico nem o perfil.
2. Pergunte, em uma única mensagem curta: modo do dia (🟢🟡🔴✈️), hora que dormiu/acordou e qualidade (1–5), se mexeu o corpo (minutos), refeições (ok/meh/pulei) e energia (M/T/N). Aceite respostas parciais; lacuna é dado.
3. Acrescente **uma linha** ao `sistema-de-vida/log/AAAA-MM.md` no formato do template (crie o arquivo se não existir). Não edite dias anteriores.
4. Se for Semana 0, não sugira mudança alguma. Se houver experimento ativo, diga em uma frase se o dia cumpriu o piso do modo escolhido (sem culpa).
5. Faça **uma** pergunta, a próxima não marcada em `sistema-de-vida/04-perguntas.md` (Bloco A → B → C → D). Registre a resposta em uma linha e marque `[x]`.
6. Se há 3+ dias seguidos em 🟡/🔴, nomeie isso e pergunte o que está acontecendo.

## Regras
- Não acesse Todoist/Calendar/Gmail neste skill.
- Não dê conselhos longos. Fechamento: 1–2 frases.
