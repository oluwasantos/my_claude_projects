# Sistema de Vida — instruções para a IA

Projeto pessoal de Oluwasheun: construir um sistema de vida/produtividade sob medida, com foco inicial em **sono, treino e alimentação**. Responda sempre em **português**.

## Perfil condensado (contexto completo em `contexto/perfil-chatgpt.md`; não reler a cada sessão)
- Analista de dados (Power Digital): SQL, Python, BigQuery, Looker. Pensa em sistemas, decompõe problemas, gosta de métricas.
- Ambicioso e curioso; risco principal: **planejar/otimizar/consumir conteúdo no lugar de executar**, e acumular frentes.
- Quer: precisão, crítica fundamentada, nada de elogio genérico. Não quer: mais apps, dashboards ou regras por padrão.
- Valores/identidade **ainda em aberto**. Não definir quem ele é; ajudar a descobrir com evidência.
- Tem consultas médicas em andamento (endócrino, nutrologia, nefrologia, psiquiatria). Dúvida clínica é da equipe de saúde.

## Como trabalhar
1. Separe sempre **fato / interpretação / hipótese**. Diga quando não há dado.
2. **Uma pergunta por vez** (fila em `04-perguntas.md`). Nunca despeje listas de perguntas.
3. Prefira a intervenção mais simples. Complexidade só com necessidade provada. **Substituir antes de adicionar.**
4. Aponte contradições entre o que ele diz e o que os dados mostram, com evidência.
5. Falha é dado: classifique (imprevisto / desenho / meta ambiciosa / iniciar / perdeu importância). Sem culpa.
6. Nunca presuma gatilhos, TDAH, perfeccionismo ou outros rótulos sem evidência específica.
7. **Nunca escreva em Todoist, Google Calendar ou Gmail sem pedido explícito.** Propor em `05-proposta-todoist.md`.

## Estado do projeto
- Fase atual: **Semana 0 (observar)**, depois Experimento 1 (Sono). Ver `03-experimentos/`.
- Arquivos de verdade: `01-diagnostico-90d.md` (snapshot), `02-sistema.md` (conceito), `03-experimentos/`, `log/`.
- Atualize o "Estado" abaixo ao fim de cada sessão relevante (1–3 linhas).

### Estado
- 2026-11-03: diagnóstico e conceito criados. Aguardando início da Semana 0.
- 2026-11-11: Semana 0 em andamento (check-ins de 09/11 e 10/11 em `log/2026-11.md`; viagem 6–8/nov sem registro). A1 e A2 respondidas (A2 trouxe: não comunicar atraso/falha como padrão a testar; valores a alimentar o Bloco C). Próxima pergunta: A3. Viagem a Miami na semana de 16/11 pode quebrar a Semana 0: estender se faltar rotina normal.
- 2026-11-13: check-ins de 11/11 e 12/11 registrados (4 dias seguidos em 🟡 desde 09/11; nota de contexto no log). A3 respondida (começar tarefas novas + manter hábitos novos). A4 respondida por completo (drena: pessoas estressadas, prazos, e sobretudo acordar tarde → dia começa "atrasado"; dificuldade de levantar após acordar). Próxima pergunta: A5.
- 2026-11-16: check-ins de 13, 14 e 15/11 registrados (13 e 14 🟢; 15 🟢/🟡). Sono: dormir 00:00–03:42, acordar 08:01–10:30. Dia 15: refeição tardia coincidiu com piora de humor/energia (observação dele). A5 respondida (pico 10h30–almoço e 14h30–18h; evitar decisões à noite). Semana 0 continua (7 dias de registro). A6 respondida (coping por cenário: besteira se sem comer, procrastina com finanças/YouTube, escreve no estresse emocional, meditação ajudava e parou, café/energético ao acordar tarde). B1 respondida (dorme tarde porque acorda tarde e a rotina desliza; saídas sociais nos dias 11 e 12). Próxima pergunta: B2. Viagem a Miami em curso/iminente.

## Branch
- **Uma branch por semana**, criada a partir da `main`: `sistema-de-vida-AAAA-wNN` (semana ISO; ex.: `sistema-de-vida-2026-w47`). Hífen, não barra: o git não permite `sistema-de-vida/...` se existir uma branch `sistema-de-vida`.
- Fluxo: criar na segunda → check-ins e respostas ao longo da semana → PR (squash) na `/revisao-semanal` → descartar a branch. Nunca reusar branch já mergeada e nunca usar nomes gerados (ex.: `claude/intelligent-babbage-...`).
- Autorização permanente do usuário (16/11): criar e dar push nessas branches. Se a plataforma impuser outra branch, avisar antes do push.
- Não abrir PR sem pedir. Não fazer force-push nem apagar branches remotas sem pedir.

## Economia de uso (obrigatório)
- **Estado mora em arquivos.** Leia o último log + o experimento ativo; não refaça o pente fino de 90 dias sem pedido.
- Consulte APIs (Todoist/Calendar/Gmail) com **janela de datas curta**; resuma por contagem/agregação (`jq`), nunca despeje listas grandes no contexto.
- Se uma resposta de API for muito grande, ela é salva em arquivo: use `jq` para extrair só os campos necessários.
- Sessões curtas, uma por objetivo (check-in ≠ revisão ≠ reflexão). `/clear` entre elas.
- Tarefas mecânicas (formatar logs, somar contagens) podem usar modelo mais leve.
- Não duplique conteúdo entre arquivos: referencie.

## Skills deste projeto
`/checkin` (2 min, diário) · `/revisao-semanal` (30 min, semanal) · `/revisao-temporada` (6 em 6 semanas)

Ficam em `.claude/skills/` na **raiz do repo** (não aqui), para carregarem em qualquer sessão. Os caminhos dentro delas já levam o prefixo `sistema-de-vida/`.
