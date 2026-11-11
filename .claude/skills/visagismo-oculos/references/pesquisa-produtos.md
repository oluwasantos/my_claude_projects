# Pesquisa de modelos reais

Fase 4. Saem de 3 a 5 modelos reais, cada um com medidas, preço, data e link que **abre o produto**. Nada inventado: se não achou, escreva ❓ e diga o que falta.

## Antes de buscar, escreva a ficha-alvo

Formato (1 a 2 opções), medidas (lente/ponte/haste, largura total se houver), material, cor, cor da lente (sol) ou exigências da receita (grau), público, teto de preço, cidade.

## Onde buscar

1. **Loja oficial da marca** (preferida). Exemplos brasileiros a verificar a cada caso, sem garantia de estoque ou preço: Chilli Beans, Ray-Ban, Oakley, Zerezes, Livo, Evoke, HB, Mormaii, Atitude, Ana Hickmann, Vogue Eyewear, Carrera e Polaroid (via distribuidor oficial).
2. **Grande varejista ou ótica de rede** que mostre medidas na página do produto.
3. **Marketplace** só se a vendedora for a loja oficial da marca. Nunca use link de busca, listagem ou "produto similar".

Use WebSearch para achar a página e **leia a página** (WebFetch ou o agente `web-fetch`) para extrair medidas, preço à vista e parcelado, público e material. O que não estiver escrito na página não é ✅.

## Regras de entrada na lista

- **Medidas dentro do alvo.** Fora do alvo só com `justificativa_fora_alvo` explícita. Exemplo: "haste 142, pedir ajuste".
  - A ponte do acetato é a medida menos negociável. Na revisão real, vários quadrados saíram por ponte de 17 mm para um nariz que pedia 19–21.
- **Preço ≤ teto** (à vista). O papel `referencia` pode passar do teto: é um "gabarito de formato" para provar, nunca para comprar. Dê o código exato (ex.: `RB2132 · 55 · 901`).
- **Público** igual ao do cliente ou unissex.
- **Página que abre o produto.** O `qa.py --online` testa. Se o site bloqueia robôs, confira com WebFetch e registre.
- **Estoque.** "Esgotado" na página pode ser texto fixo do site. Registre `estoque: "incerto"` e mande checar pelo CEP ou ligar para a loja.
- **Foto de frente do produto (para o provador).** Ache na página a imagem do produto em 1000 px ou mais e **olhe** cada uma antes de escolher: o nome do arquivo não diz a vista.
  - No caso real, a `--1-` era a frente no 5317 e no 3614, mas a lateral no 5127, cuja frente era a `--2-`.
  - O 4000 não tinha foto de frente, mas o 4351 (mesma armação 62□15 142, mesma cor) tinha. Use a foto dele e registre `foto_frente_origem: "foto da mesma armação (código 4351)"`.
  - Registre a URL escolhida em `foto_frente_url`. Só foto da loja oficial, usada só nesta apresentação privada.
- **Nos slides de produto,** continue com a ilustração SVG do formato, na cor real, e o link para a loja.
- **Confira o formato pela foto:** o 5127, tratado como quadrado suave, era um wayfarer.

## Montar a lista final

- **Curinga** (1, às vezes 2 lado a lado), **alternativa de preço** (se houver), **complemento** (se o cliente quer dois) e, opcionalmente, **referência** para provar.
- Prefira modelos que possam ser provados **numa única visita**: mesma marca ou mesma rede na cidade do cliente.
- Para cada produto escreva "por que entra" e "o que você perde". Os pontos fracos assumidos aumentam a confiança.
- **Descartados** vão para `dados.descartados` com motivo curto (ponte estreita, acima do teto, esgotado, sem medidas na página, público). O slide "O que revisei" usa essa lista.

## Lições do caso real (oculos-de-sol/, nov/2026)

| Erro na v1 | Regra que virou |
|---|---|
| Polaroid 4108/S de categoria feminina | Checar público na página |
| Tartaruga estampada "too much" | Para estilo discreto, oferecer a versão sólida do mesmo formato |
| Links de marketplace e de busca que não abriam | Só link de produto da loja oficial, testado |
| "Esgotado" em todas as páginas | Estoque sempre ⚠️ e instrução de checar pelo CEP |
| Busca genérica de Ray-Ban | Código exato (modelo · tamanho · cor) para pedir na ótica |
