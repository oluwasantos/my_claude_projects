# renda-extra/

Projeto de renda extra online. Fase atual: **duas ideias na mesa, nenhuma validação começou. Escolher UMA para validar primeiro.**

| # | Ideia | Arquivo |
|---|---|---|
| 1 | Dossiê visagista de óculos para óticas (B2B) | este README |
| 2 | Infoproduto: GA4 + BigQuery para marketing (pack de queries → curso → empresas) | [`ideia-2-infoproduto-dados.md`](ideia-2-infoproduto-dados.md) |

Legenda de confiança: ✅ confirmado · ⚠️ estimativa · ❓ não sei / falta checar.

---

## 1. A ideia: "Visagista de bolso" para óticas

**Em uma frase:** vender o dossiê visagista que a skill `/visagismo-oculos` já gera (fotos do rosto → medidas, diagnóstico, provador, modelos reais) como **serviço para óticas independentes**, que usam o relatório para vender armação melhor e mais cara.

**Por que esta e não outra:**
- **O produto já existe.** A skill está pronta e testada no seu próprio caso (✅ `.claude/skills/visagismo-oculos/`). Quase toda ideia de "negócio de 1 milhão" morre antes de ter o produto; esta começa com ele.
- **Quem paga tem dinheiro e dor clara.** A ótica ganha na armação. Um cliente que sai convencido de que aquele modelo "é o rosto dele" compra mais rápido, compra mais caro e devolve menos. O relatório é ferramenta de venda, não um mimo.
- **B2B escala melhor que B2C.** Vender R$ 79 por vez para pessoa física exige marketing constante. Uma ótica assinando todo mês é receita recorrente.
- **Barreira de cópia razoável:** o diferencial é o processo (medida, regras de caimento, provador em escala, crítico independente, catálogo real com preço), não um prompt solto.

### Duas portas de entrada (do menor para o maior risco)

| Porta | O que é | Preço | Para quê |
|---|---|---|---|
| **A · B2C manual** | Você roda a skill para pessoas que mandam fotos (Instagram/WhatsApp) | R$ 49–99 por dossiê ⚠️ | Validar se alguém paga e afinar o produto. Não é onde está o milhão. |
| **B · B2B ótica** | A ótica manda as fotos do cliente; você devolve o dossiê com **o catálogo daquela ótica** | R$ 199–499/mês por loja, com cota de dossiês ⚠️ | O negócio de verdade. |
| C · Software (depois) | Um app onde a própria ótica sobe as fotos e recebe o dossiê sozinha | — | Só quando B provar demanda. Não construir antes. |

---

## 2. A conta do "1 milhão" (sem enfeite)

- US$ 1.000.000 ≈ **R$ 5,3–5,8 milhões** ⚠️ (câmbio não checado hoje).
- Caminhos para chegar lá com a porta B (todos ⚠️, são contas, não previsões):

| Meta | Lojas pagando | Ticket/mês | Receita/ano |
|---|---|---|---|
| Renda extra boa | 20 | R$ 300 | R$ 72 mil |
| Vira emprego | 100 | R$ 350 | R$ 420 mil |
| ~US$ 1 mi em receita anual | ~1.300 | R$ 350 | ~R$ 5,5 mi |
| ~US$ 1 mi em **valor de empresa** | ~250–400 | R$ 350 | ~R$ 1–1,7 mi/ano, vendida a múltiplo de receita recorrente ⚠️ |

**Leitura honesta:** o milhão de dólares em faturamento anual exige **mais de mil óticas** e um software (porta C), com time. Isso é possível, não provável, e leva anos. O alvo realista dos primeiros 12 meses é **renda extra de R$ 3–6 mil/mês** (10–20 lojas). Se isso acontecer, a escada para cima está clara.

❓ Número de óticas no Brasil e quantas são independentes: não pesquisado ainda. É o primeiro dado a buscar, porque define o teto.

---

## 3. Riscos (e o que fazer com cada um)

| Risco | Gravidade | Mitigação |
|---|---|---|
| **LGPD:** foto de rosto é dado pessoal (e pode ser tratada como sensível) | Alta | Termo de consentimento simples; fotos apagadas após a entrega; nada no repo (regra que já existe na skill). Consultar um advogado antes da porta B ❓ |
| Medida por foto é imprecisa | Média | Já marcada como ⚠️ na skill; vender como "orientação para provar", nunca como medida técnica |
| Custo por dossiê (tempo + uso do Claude) | Média | Medir nos 10 primeiros; o preço B2B tem que cobrir isso com folga |
| Ótica grande ou rede lançar algo parecido / provador virtual | Média | Focar em óticas independentes; o diferencial é o diagnóstico explicado, não só "ver o óculos no rosto" |
| Você não ter tempo | Alta | Validação desenhada para ~4 h/semana (abaixo) |

---

## 4. Validação em 30 dias (barata, com critério de parada)

| Semana | Passo | Critério para seguir |
|---|---|---|
| 1 | Rodar a skill em **5 pessoas conhecidas** (de graça). Cronometrar cada uma. | Pelo menos 4 de 5 dizem que mudaria a escolha delas |
| 2 | Oferecer a **10 pessoas** a R$ 49 (Instagram/WhatsApp) | Pelo menos 3 pagam |
| 3 | Levar 2 dossiês prontos a **5 óticas independentes em BH** e mostrar | Pelo menos 1 aceita piloto pago de 1 mês |
| 4 | Piloto com essa ótica usando o catálogo dela | A ótica renova ou indica outra |

**Parar ou girar se:** ninguém pagar na semana 2 **e** nenhuma ótica topar o piloto na semana 3. Custo total da validação ⚠️: perto de zero além do seu tempo.

---

## 5. Próximos passos

1. Responder a pergunta em aberto (abaixo).
2. Buscar o número de óticas no Brasil / em BH (❓).
3. Escrever o termo de consentimento das fotos (rascunho).
4. Começar a semana 1.

### Pergunta em aberto
Quantas horas por semana você consegue dar a isto, de verdade, e tem algum valor que topa investir no começo?
