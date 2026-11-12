# Ideia 4 · App na Shopify App Store para lojas dos EUA

Legenda: ✅ confirmado (fonte oficial ou mais de uma fonte) · ⚠️ estimativa / fonte secundária · ❓ não sei / falta checar. **Nada aqui é consultoria jurídica ou contábil.**

Critérios do usuário: vender **nos EUA**, sendo cidadão brasileiro **sem visto de trabalho**, com **pouca regulação**, barreira financeira baixa e escalável.

---

## 1. O formato primeiro (é ele que resolve o problema do visto)

**Vender software para empresas americanas por um marketplace que cobra, entrega e repassa o dinheiro.** O melhor encaixe é a **Shopify App Store**:

| Problema | Como o formato resolve |
|---|---|
| Achar cliente nos EUA sem estar lá | O lojista procura "returns", "size chart" etc. **dentro** da loja de apps. É o ponto fraco das ideias anteriores (aquisição) resolvido pela vitrine. |
| Cobrar em dólar | Cobrança via Shopify Billing; a Shopify repassa ao parceiro ⚠️ (confirmar meio de repasse para o Brasil) |
| Imposto sobre venda nos EUA (sales tax) | A Shopify cobra o lojista; você não emite nota nos EUA ⚠️ (confirmar nos termos de parceiro) |
| Taxa | **0% sobre o primeiro US$ 1 milhão de receita acumulada, 15% acima disso** ✅ (changelog oficial da Shopify; cadastro único de US$ 19) |
| Regulação | Ferramenta B2B de e-commerce: sem saúde, finanças, imóveis, crianças. Só precisa cumprir as regras de privacidade da Shopify (webhooks obrigatórios de dados) ⚠️ |

**Plano B do formato** (se não for app Shopify): SaaS próprio vendido por um *merchant of record* (Paddle, Lemon Squeezy), que vira o vendedor legal e cuida do imposto. Custo ⚠️ ~5% + US$ 0,50 por venda; Paddle diz que dispensa CNPJ ⚠️.

### Visto, empresa e imposto (o mínimo para não se enrolar)
- **Visto:** vender a clientes americanos **trabalhando do Brasil** é exportar serviço/software; visto de trabalho trata de trabalhar **em solo americano** ⚠️. Na viagem a Miami, não trate o app como trabalho feito lá (visto de turista) ⚠️.
- **Não abrir LLC nos EUA no começo.** LLC de estrangeiro tem obrigação anual (Form 5472) com multa alta se esquecer ⚠️. Só faz sentido com receita relevante.
- **Nos EUA:** a Shopify/o MoR vai pedir o formulário **W-8BEN** (declara que você não é residente fiscal americano) ⚠️.
- **No Brasil:** a receita é tributada aqui. Pessoa física → carnê-leão mensal; com volume, empresa no Simples, que tem benefícios para exportação de serviço ⚠️. **Falar com um contador antes da primeira venda.** ❓ Também checar se o contrato de trabalho atual permite atividade paralela.

---

## 2. A hipótese de app: "Why Returns" (por que devolvem)

**Para quem:** lojas de **roupa e calçado** dos EUA na Shopify. Devolução é o maior ralo de margem desse setor ⚠️.

**O que faz:** lê os motivos de devolução/troca, as avaliações e as mensagens de clientes, e agrupa por produto e tamanho:
> "Calça X, tamanho M: 38% das devoluções dizem 'ficou pequena'. Sugestão: aviso 'veste pequeno, peça um número acima' na página."

E gera o texto da nota de caimento para colar na página do produto.

**Por que essa:**
- ROI fácil de vender: "se evitar 5 devoluções por mês, o app se paga".
- Dados já estão na Shopify (pedidos, devoluções, avaliações) ⚠️ (confirmar o que a API de devoluções expõe).
- Usa IA no que ela faz bem (ler texto livre e agrupar), não em algo regulado.

**Atenção honesta:** concorrência ❓ **não pesquisada**. Existem apps grandes de gestão de devolução que podem já ter relatório de motivos. A **primeira tarefa** é ler as avaliações 1–3 estrelas dos 10 apps de "returns" e "size chart" e anotar o que os lojistas reclamam que falta. Se a hipótese morrer, o mesmo método aponta outra dor dentro do mesmo formato.

## 3. Preço e conta do "1 milhão"

| Plano | Preço ⚠️ |
|---|---|
| Free | até 50 pedidos/mês analisados |
| Growth | US$ 29/mês |
| Pro | US$ 79/mês (várias lojas, alertas semanais) |

- US$ 1 mi/ano = US$ 83,3 mil/mês ≈ **1.700 lojas a US$ 49 de ticket médio**. Na Shopify esse primeiro milhão **sai sem comissão** ✅.
- Se construir pelo **Polsia**, ele leva ~20% ⚠️ e ❓ não sei se ele consegue publicar app na Shopify (exige conta de parceiro em seu nome e revisão manual da Shopify). **Alternativa:** construir com o próprio Claude Code, que você já usa, e guardar os 20%.

| Cenário | Lojas pagantes | Receita/mês |
|---|---|---|
| Paga as contas do projeto | 10 × US$ 29 | US$ 290 (≈ R$ 1,6 mil ⚠️) |
| Renda extra boa | 100 × US$ 45 | US$ 4,5 mil (≈ R$ 25 mil ⚠️) |
| ~US$ 1 mi/ano | ~1.700 × US$ 49 | US$ 83 mil |

**Leitura honesta:** dólar ajuda muito: 100 lojas já é renda relevante em real. Mas app novo começa com zero avaliações e aparece mal na busca; os primeiros 6 meses costumam ser lentos ⚠️.

## 4. Validação em 30 dias

| Semana | Passo | Critério para seguir |
|---|---|---|
| 1 | Ler avaliações ruins dos 10 apps da categoria; cadastro de parceiro Shopify (US$ 19); falar com contador | A dor "não sei por que devolvem" aparece; nenhum app barato resolve bem |
| 2 | Landing page em inglês + MVP que lê um CSV de devoluções exportado (sem integração ainda) | Funciona com dados de exemplo |
| 3 | Oferecer análise grátis a 20 lojistas (fóruns/comunidades de Shopify, Reddit, X) | ≥ 5 mandam o CSV |
| 4 | Entregar o relatório e perguntar "pagaria US$ 29/mês para receber isso toda semana?" | ≥ 2 dizem sim com cartão (pré-venda) |

**Parar ou girar se:** < 5 lojistas mandarem dados na semana 3. Custo ⚠️: US$ 19 + horas.
