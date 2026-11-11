# Autocrítica e reavaliação

Regra da skill: **a primeira versão nunca chega ao usuário.** O que ele recebe passou por pelo menos uma rodada completa (3 lentes, máquinas e crítico externo), sem nenhum item bloqueante em aberto.

## A rodada (repita até zerar bloqueantes; no máximo 3 rodadas)

1. **Releia como outra pessoa.** Feche o raciocínio que levou à v0 e abra só `dados.json` e as capturas. Passe pelas 3 lentes abaixo e anote cada objeção.
2. **Máquinas:**
   - `python3 scripts/qa.py dados.json --html apresentacao.html --online`;
   - `node scripts/render.js apresentacao.html shots/` e **olhe** `shots/folha-390.png` e `shots/folha-1280.png`.
3. **Crítico com contexto limpo:** lance o subagente com o prompt da seção final. Ele não viu sua conversa, então pega o que você normalizou.
4. **Consolide** as objeções em `dados.revisao` (`rodada`, `fonte`: autocritica | qa | critico, `severidade`, `objecao`, `decisao`, `status`).
   - Corrija todas as bloqueantes e as importantes que tiverem solução.
   - Se recusar uma objeção, a `decisao` diz por quê.
5. **Recompile** a apresentação e rode de novo o `qa.py` e o `render.js`.
6. **Se após 3 rodadas ainda houver bloqueante,** não esconda.
   - Escreva no slide de pontos fracos e na mensagem final.
   - Pergunte ao usuário o que ele prefere. Exemplo: "não achei ponte 20 abaixo de R$ 400: aceita 18 com plaquetas ou sobe o teto?".

## Lente 1 · Visagista (a técnica está certa para ESTE rosto?)

- Cada regra do diagnóstico aponta para algo **visível na foto anotada**? Se a regra veio de uma tabela genérica sem evidência na foto, corte ou rebaixe para ⚠️.
- Alguma recomendação **contradiz** o próprio diagnóstico? Ex.: rosto longo + retângulo baixo; mandíbula angulosa + quadrado de canto duro; ponte nasal baixa + acetato de ponte 17.
- A **escala** confere? A largura total do produto (estimada como 2A + DBL + 12) cai na largura-alvo?
- A **cor** foi lida em mais de uma foto? O subtom pode estar errado por causa da luz? Se sim, ⚠️ e uma alternativa neutra.
- **Grau:**
  - a descentração está ok para a receita?
  - a altura serve para multifocal?
  - o índice sugerido é coerente?
  - o aro esconde a borda?
- **Sol:** UV400 confirmado? A lente do curinga serve para a ocasião mais exigente que o cliente citou?
- **Provador:**
  - cada armação está centrada nas pupilas e com a barra de cima na linha da sobrancelha?
  - o recorte da foto do produto ficou limpo, sem branco preso na ponte ou nas plaquetas, sem halo e sem pedaço de haste lateral?
  - o cartão diz se é foto da loja, sua foto real ou desenho?
  - o "frente ≈" do cartão é o mesmo dos slides de produto?
  - o veredito (encaixa/sobra/estreita) contradiz algum texto?
  - um modelo que "sobra" está sendo vendido como ideal?
- **Advogado do diabo:** para cada produto, escreva o melhor argumento **contra**. Se você não tem resposta, troque o produto.

## Lente 2 · Cliente (ele vai se reconhecer e conseguir agir?)

- O modelo tem **o público e o estilo** que ele pediu? Algum detalhe pode soar "muito feminino", "muito masculino" ou "too much"?
- Alguém sem conhecimento técnico entende cada slide? Jargão (DBL, boxing, vértice) só aparece com explicação em 5 palavras.
- **Teste dos 5 segundos:** o slide de decisão responde "o que eu compro e onde provo?" em 5 segundos?
- Dá para **agir hoje**? O link abre, o código é exato e a loja fica na cidade dele (ou entrega)?
- O tom é de especialista franco, não de vendedor. Sem promessas ("vai ficar perfeito"), sem superlativos vazios.
- A foto foi usada com respeito? Enquadramento do rosto, sem expor fundo pessoal desnecessário, rótulos que descrevem medidas e não julgam ("nariz grande" → "ponte larga, pede ponte 20+").

## Lente 3 · QA de dados (está tudo certo e rastreável?)

- Todo preço, medida e código da apresentação é **igual** ao `dados.json`? O `qa.py` confere preços, códigos e links.
- Somas dos combos, porcentagem do teto e datas de leitura.
- Selo de confiança em todo fato. Nenhuma estimativa apresentada como ✅.
- Medidas do rosto citadas com "≈" e a margem da escala (íris ±5%, armação ±3%).
- Nada inventado: nota de loja, avaliação, estoque, prazo, preço de lente que não foi lido.

## Bloqueantes (impedem a entrega)

1. Produto fora do alvo de medida sem justificativa.
2. Preço acima do teto ou soma errada.
3. Link que não abre o produto.
4. Público do modelo diferente do cliente.
5. Recomendação que contradiz o diagnóstico.
6. Estimativa apresentada como confirmada; dado inventado.
7. Grau: descentração alta com grau alto, multifocal com altura < 30, sem aro com miopia alta.
8. Sol: curinga sem UV400 confirmado ou visivelmente declarado.
9. Overflow horizontal, texto cortado ou ilegível no celular; slot `{{…}}` restante; slide do tipo errado (sol/grau).
10. Foto ou dado do cliente salvo dentro do repositório.

## Severidades

- **bloqueante:** lista acima.
- **importante:** muda a decisão ou a confiança do cliente. Exemplos: falta uma alternativa de preço; o perfil não foi usado; a cor tem leitura duvidosa.
- **cosmético:** polimento de texto ou layout que não muda a decisão. Resolva se for rápido.

## O slide "O que revisei" (o cliente vê o raciocínio, nunca a v0)

- Escolha de 3 a 6 decisões que **mudaram** na revisão ou que foram **confirmadas** contra uma dúvida real.
- Formato: chip (saiu / ajustado / confirmado) + título curto + 1 frase de porquê.
- Exemplos:
  - "Saiu: Quadrado 4016. A ponte de 17 mm escorregaria no seu nariz."
  - "Ajustado: a cor do curinga. Nas três fotos sua pele lê quente, então o preto virou havana escuro."
  - "Confirmado: a lente de 55. A largura das suas têmporas (≈ 138 mm) pede frente de 137–141."
- Não mostre a v0, nem "eu errei", nem a lista bruta de objeções.

## Prompt do subagente crítico

Use a ferramenta Agent (`subagent_type: general-purpose`, sem `model`, para herdar o modelo da sessão; prefira Opus em esforço alto). Preencha os caminhos. O crítico **não edita nada**: devolve objeções.

```
Você é um crítico independente: um óptico-visagista sênior com 20 anos de balcão, que revisa
o dossiê de um colega antes que ele chegue ao cliente. Seja exigente e concreto. Responda em pt-BR.

Leia, nesta ordem:
1. <SKILL>/references/autocritica.md (rubrica; use as seções "Lente 1/2/3" e "Bloqueantes")
2. <CASO>/dados.json (fonte da verdade: briefing, medidas, diagnóstico, produtos)
3. <CASO>/medidas.json (saída do medir.py: escalas, alertas)
4. As imagens <CASO>/shots/folha-390.png e <CASO>/shots/folha-1280.png
   (e slides avulsos em <CASO>/shots/390/ e /1280/ se precisar de detalhe)
5. As fotos anotadas: <CASO>/shots/1280/slide-03.png (frente) e o slide de perfil, se houver

Tarefa: encontre o que está errado, frágil ou mal comunicado para ESTE cliente.
- Verifique se cada afirmação sobre o rosto é visível nas fotos anotadas.
- Verifique contradições entre diagnóstico e produtos, e medidas fora do alvo.
- Verifique se o cliente (tipo, público, estilo, orçamento, cidade) se reconheceria nas escolhas.
- Procure problemas de layout nas capturas (texto cortado, sobreposição, contraste, foto mal enquadrada).
- Não proponha produtos novos sem dizer o critério; não invente preços.

Devolva SOMENTE uma lista JSON:
[{"severidade":"bloqueante|importante|cosmetico","lente":"visagista|cliente|qa|layout",
  "onde":"slide ou campo","objecao":"...","evidencia":"o que você viu","sugestao":"..."}]
Se não houver objeções, devolva [] e uma frase dizendo o que você conferiu.
```

Registre a resposta em `dados.revisao` com `fonte: "critico"`, mesmo que seja `[]`. O `qa.py` exige isso.
