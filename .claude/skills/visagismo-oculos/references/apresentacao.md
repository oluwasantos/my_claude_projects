# A apresentação

Base: `assets/template.html`. Referência de qualidade já aprovada pelo usuário: `oculos-de-sol/apresentacao.html` (sol, sem foto). A nova versão acrescenta fotos anotadas, perfil, slide de lente, "O que revisei" e "Pontos fracos".

## Montagem

1. `cp <SKILL>/assets/template.html <CASO>/apresentacao.html`. Nunca edite o template para um cliente.
2. Tema: `t-sol` (boutique noturna, faixa tartaruga) ou `t-grau` (ateliê claro, faixa de antirreflexo).
3. Apague os blocos `data-so` do outro tipo (o slide `#lente` e os 2 itens do checklist).
4. Duplique os blocos `REPETIR` conforme o caso; um slide por produto.
5. Gere as fotos anotadas com `anotar.py` e cole o fragmento no lugar de `{{FOTO_ANOTADA_FRENTE}}` e `{{FOTO_ANOTADA_PERFIL}}`.
   - Sem perfil útil: apague o slide `#perfil`.
   - Sem autorização para mostrar foto: use o rosto esquemático de `oculos-de-sol/apresentacao.html`.
6. `<title>`: nome curto, ex.: "Dossiê Óculos Ana". 2 a 4 palavras, sem explicação.
7. Réguas e barras de preço são preenchidas pelos atributos `data-*`; o JS desenha. Não calcule porcentagens à mão.
8. Remova os comentários `<!-- -->` de instrução que sobrarem, se quiser um HTML limpo (o `qa.py` os ignora).

## Slides (ordem e conteúdo)

| # | id | O que precisa dizer | Fonte no dados.json |
|---|---|---|---|
| 1 | `capa` | Tese em uma linha + a notação-alvo (`55□19–21 145+`) + forma ilustrada | `alvo`, `diagnostico.estrategia` |
| 2 | `briefing` | O pedido nas palavras do cliente: tipo, ocasiões, orçamento, estilo, barba/cabelo, armação atual ou receita | `cliente`, `armacao_atual`, `receita` |
| 3 | `rosto` | 4 a 6 fatos com selo + foto de frente anotada (medidas, linha da sobrancelha, armação ideal simulada) | `diagnostico`, `medidas` |
| 3b | `perfil` | Ponte nasal, projeção, onde a haste dobra; foto de perfil anotada | `medidas` |
| 4 | `regua` | Alvo de lente/ponte/haste; com entrada B, a armação atual marcada "hoje" e a leitura dela | `alvo`, `armacao_atual` |
| 5 | `forma` | 1–2 formas "sim" e 1–2 "evitar", cada uma com o porquê ligado ao rosto | `diagnostico.regras/evitar` |
| 6 | `cor` | Subtom e contraste, 6 amostras (inclua 1 "evitar") | `diagnostico.cor` |
| 7 | `lente` | Sol: UV400, categoria, polarizada, cor da lente. Grau: tabela da receita, índice, descentração, altura | `receita` |
| 8 | `estrategia` | 1 curinga ou curinga + complemento, com a ocasião de cada um | `diagnostico.estrategia` |
| 8b | `provador` | Cada modelo recomendado no rosto do cliente, em escala, com "frente ≈ N mm" e o veredito; a armação atual como referência. Lede diz o que comparar | `provador.py` (produtos, medidas, pontos) |
| 9+ | `<id do produto>` | Ilustração na cor real, nome, código, preço igual ao do dados, barra do teto, medidas com selo, por que entra, o que perde, estoque, link | `produtos[]` |
| — | `revisei` | 3 a 6 decisões da autocrítica (ver `autocritica.md`) | `revisao`, `descartados` |
| — | `fracos` | 3 a 5 limites honestos (escala estimada, luz e cor, estoque, policarbonato vs acetato…) e como conferir | `medidas.alertas`, produtos |
| — | `checklist` | 6 testes na loja (sol: polarização + UV; grau: medidas pela ótica + lente na armação) | tipo |
| — | `decisao` | "O que comprar e onde provar" em 5 segundos; passos; legenda dos selos; links | `produtos`, `combos` |

## Provador

- Gerado por `scripts/provador.py` a partir do `dados.json`, do `medidas.json` e do `pontos.json`. A foto entra **uma vez** e cada cartão a reusa (`<use href="#prov-foto">`): 5 cartões custam ≈ 90 KB.
- **Largura:** `largura_total` da página quando existe; senão 2·lente + ponte + 12, marcada "(estimada)".
- **Aparência:**
  - cor do aro por `cor_css`, ou inferida de `cor`;
  - espessura pelo material: metal ≈ 1,3 mm, acetato/policarbonato ≈ 4,5 mm;
  - lente tingida pelo `lente_tipo`, translúcida para os olhos aparecerem.
- **Rótulos:** `rotulo` troca o papel no cartão (ex.: "O que você quis provar", "Plano B"); `nome_curto` troca o nome (padrão: forma + número do código, como "Aviador 4000").
- **Veredito:** frente − têmporas. |d| ≤ 3 mm encaixa; acima, "sobra ≈ X mm"; abaixo, "estreita ≈ X mm". O texto dos slides de produto tem de bater com o veredito.
- É simulação: tamanho e formato fiéis à escala; cor, brilho e perspectiva aproximados. A legenda fixa do template diz isso; não a apague.
- Sem foto de frente com escala (sem íris nítida nem armação conhecida), apague o slide `#provador`.

## Texto

- Português do Brasil, segunda pessoa ("seu rosto", "você"), frases curtas, sem jargão sem explicação.
- **Títulos que afirmam:** "Altura na lente, curva nos cantos", não "Formato ideal".
- **Selos em todo fato:** chip `c-ok` (lido ou medido com armação conhecida), `c-warn` (estimativa, visual, foto), `c-unk` (não achei). Texto curto no chip: "medido", "visual", "da foto", "relato", "lido 11/11".
- **Medidas do rosto com "≈"** e margem uma vez no slide da régua ("±5%, pela íris").
- **Preços:** `R$ 199,99` (vírgula decimal, espaço depois de R$), com a data de leitura.
- Nada de "v0", "rascunho", "primeira versão".

## Fotos

- Enquadre do ombro para cima (`recorte` no spec do `anotar.py`). Não mostre fundo pessoal sem necessidade.
- `lado_max` 1000–1200 e `qualidade` 75–80 deixam cada foto com ~100–250 KB. A apresentação inteira deve ficar < 6 MB.
- **Anotações:**
  - 3–4 medidas na frente: têmporas, maçãs, comprimento, ponte;
  - 1 guia: a linha da sobrancelha;
  - a armação ideal simulada (`armacao.pupilas` + `largura_px` = largura-alvo em mm ÷ mm por px).
  - Rótulo neutro e técnico, sem julgamento estético.
- **Legenda:** de onde vem a escala, e "a armação é uma simulação do formato".
- Antes de colar, gere a prévia (`--preview`) e capture com `render.js`. Rótulos sobrepostos ou fora da foto: ajuste `pos` ou o recorte.

## Entrega

1. Publique com a ferramenta Artifact (`file_path` = `<CASO>/apresentacao.html`, `icon: "glasses"`). A descrição é uma frase sem dados pessoais sensíveis. Para atualizar depois, republique o mesmo caminho.
2. Envie o arquivo com SendUserFile (`display: "render"`).
3. A mensagem no chat tem até 5 linhas:
   - a recomendação;
   - onde provar;
   - o link;
   - 1 ponto fraco principal;
   - a pergunta "o que achou?" para a rodada de retorno.
