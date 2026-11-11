# Óculos de sol × óculos de grau

O tipo muda o alvo de medida, a pesquisa, o slide de lente e o checklist. Leia antes da fase 3.

## O que muda em uma linha

| | Sol | Grau |
|---|---|---|
| Função | Proteger (UV, ofuscamento) | Enxergar 12 h por dia com conforto |
| Tamanho | Lente 2–4 mm maior, cobre mais | Lente proporcional ao rosto **e à receita** |
| O que limita | Rosto e estilo | Rosto, estilo **e espessura/óptica da lente** |
| Peso e ajuste | Uso por horas | Uso o dia todo: peso, plaquetas e pressão importam muito |
| Formatos liberados | Aviador, oversized, envolvente (curvatura base 6–8) | Envolvente só com grau baixo; sem aro só com material e grau adequados |
| Orçamento | Normalmente o produto inteiro | **Pergunte:** o teto é só da armação ou armação + lentes? |
| Onde provar | Loja da marca ou ótica | Ótica que monte a lente e meça DP e altura na armação escolhida |

## Sol: proteção primeiro

- **UV400 / 100% UV** obrigatório. Escuro sem filtro UV dilata a pupila e piora a exposição. Confirme na página ou no selo da haste.
- **Categoria de filtro** (NBR ISO 12312-1):
  - categoria 2: luz média;
  - categoria 3: sol forte, o padrão de praia e de rua no Brasil;
  - categoria 4: neve e montanha, **proibida para dirigir**.
- **Polarizada:** corta o reflexo da água, do asfalto e do capô. Desvantagem: escurece algumas telas (celular girado, painel do carro). Para curinga de praia e estrada, prefira polarizada.
- **Cor da lente:**
  - verde **G-15**: a mais fiel às cores, clássica;
  - **cinza**: neutra, escurece mais, boa para sol forte;
  - **marrom/âmbar**: aumenta o contraste e aquece, combina com subtom quente;
  - **degradê**: cidade e direção, protege menos de baixo; não serve de curinga de praia;
  - **espelhada**: chama atenção, não é "discreta".
- **Cobertura:** lente mais alta e mais larga protege melhor. Para rosto longo isso se soma à regra visagista (altura na lente).
- **Sol com grau:**
  - armação curva (base 8) aceita grau limitado (em geral até ~±3, conforme o laboratório);
  - lente solar com grau custa bem mais;
  - alternativas: clip-on ou lente fotossensível no óculos de grau. Cite se a receita for alta.

## Grau: a receita manda na armação

**Leia a receita.**
- **Esférico (ESF):** − é miopia, + é hipermetropia.
- **Cilíndrico (CIL)** e **eixo:** astigmatismo.
- **Adição (AD):** presbiopia, leva a multifocal ou ocupacional.
- **DP:** distância pupilar. A DP medida pela ótica sempre vence a da foto.

**Espessura e tamanho.**
- **Miopia** (−): a lente é fina no centro e **grossa na borda**. Quanto maior a lente e maior a descentração, mais grossa a borda temporal.
  - Acima de −3: prefira lente menor ou média, formato com borda uniforme (redondo, oval, panto, quadrado suave) e acetato encorpado que esconda a borda.
  - Evite armação sem aro ou de fio de nylon acima de ~−4.
- **Hipermetropia** (+): a lente é **grossa no centro** e aumenta os olhos. Lente pequena reduz espessura e peso.
- **Índice da lente** (orientação; a ótica decide):
  - até ±2: 1.50 / 1.56 / 1.59 (policarbonato);
  - ±2 a ±4: 1.60–1.67;
  - acima de ±6: 1.74.
  - Armação sem aro e parafusada pede policarbonato ou Trivex.

**Descentração** por olho = (A + DBL − DP) / 2.
- Ideal ≤ 2–3 mm. O centro óptico fica perto da pupila e a borda fica uniforme.
- Mais de 4 mm com esférico ≥ 3 deixa a borda temporal grossa e pode exigir blank maior. O `qa.py` bloqueia esse caso.
- **Diâmetro mínimo do blank** ≈ maior diagonal da lente + 2 × descentração + 2 mm.

**Multifocal (progressiva).**
- Altura da lente **B ≥ 30–32 mm**. Montagem (pupila → borda de baixo) ≥ 18 mm. Confirme com o projeto de lente da ótica.
- Lente ocupacional ou de corredor curto aceita ~28 mm.
- Rosto curto com maçãs altas restringe a altura: cheque `alvo.altura_lente_max`.

**Cilíndrico alto** (≥ 2): evite curvatura frontal acentuada e armação muito larga com lente grande. Ambas distorcem a periferia.

**Conforto de uso diário.**
- Metal com **plaquetas ajustáveis** resolve a ponte baixa e distribui o peso.
- TR90 e titânio são leves. Acetato pesado com lente alta cansa o nariz.

**Tratamentos.**
- **Antirreflexo:** sempre.
- **Filtro de luz azul:** opcional. A evidência de benefício para a saúde ocular é fraca; não venda como necessário.
- **Fotossensível:** solução híbrida grau + sol.

**Estilo.** A armação de grau é o "rosto do dia a dia": aparece em reuniões e fotos. A mensagem visagista pesa mais que no sol. Vale propor **duas**: uma discreta e uma com personalidade, se o orçamento permitir.

## Sem receita (grau pedido, receita não enviada)

- Recomende pela visagismo e pelo alvo de medida, mas marque espessura, índice e descentração como ❓.
- No slide de lente, liste as perguntas para a ótica:
  - qual é o meu grau;
  - qual índice vocês recomendam nesta armação;
  - qual é a descentração;
  - a altura da lente basta para multifocal?
