# Visagismo aplicado a óculos

Leia inteiro na fase 3. Cada regra só vale se a foto mostrar o traço que a justifica. Na apresentação, toda afirmação sobre o rosto aponta para algo visível na foto anotada.

## 1. Os três princípios (nesta ordem)

1. **Escala.** O tamanho da armação acompanha o tamanho do rosto. A largura total da frente ≈ a largura nas têmporas. Traços marcados (sobrancelha grossa, mandíbula forte, barba) aguentam aro mais espesso; traços delicados pedem aro fino ou metal.
2. **Contraste de linhas.** A armação equilibra o que o rosto já tem de sobra. Rosto anguloso pede curva, rosto curvo pede ângulo, rosto longo pede altura na lente e horizontalidade, rosto curto pede lente mais baixa e linhas ascendentes.
3. **Mensagem.** No visagismo (linha de Philip Hallawell), a linha comunica:
   - linhas **horizontais** transmitem estabilidade e calma;
   - linhas **verticais** transmitem firmeza e elegância;
   - linhas **inclinadas para cima** transmitem dinamismo e alegria;
   - **curvas** transmitem acolhimento e sensibilidade.

   O estilo que o cliente pediu ("clássico, discreto", "criativo", "executivo") define qual mensagem reforçar. Quando o princípio 2 e o 3 brigam, procure a forma que atende os dois. Um exemplo é o quadrado de cantos suaves: horizontal e firme, mas sem somar ângulo.

## 2. Formatos de rosto

Use as pistas do `medir.py` (proporções) **e** o olhar sobre a foto. Rosto real é misto. Diga "retangular com mandíbula marcada", não force um rótulo puro. Selo sempre ⚠️.

| Formato | Como reconhecer | Favorece | Evitar |
|---|---|---|---|
| **Oval** | Comprimento ≈ 1,3–1,45× a largura das maçãs. Testa e mandíbula um pouco mais estreitas que as maçãs. Sem ângulos fortes | Quase tudo. Respeite a escala. Quadrado e retangular dão estrutura | Armação maior que o rosto, que esconde o equilíbrio |
| **Redondo** | Comprimento ≈ largura. Bochechas cheias, mandíbula macia | Retangular e quadrado, geométrico, wayfarer, ponte alta e fina, topo marcado | Redondo, oval pequeno, aro muito fino e baixo |
| **Quadrado** | Testa, maçãs e mandíbula quase iguais. Mandíbula angulosa | Redondo, oval, panto, aviador, cantos suaves. Barra de cima marcada | Quadrado de cantos duros e retângulo estreito |
| **Retangular/oblongo** | Comprimento ≥ 1,45× a largura. Laterais paralelas, mandíbula marcada | Lente com **boa altura**, quadrado suave, panto grande, aviador, hastes com detalhe lateral (alargam) | Retângulo **baixo e estreito**, armação pequena |
| **Coração** (triângulo invertido) | Testa larga, queixo estreito e fino | Peso embaixo: panto, redondo, aviador, sem aro embaixo; cores claras no topo | Barra de cima pesada, gatinho exagerado, enfeite no topo |
| **Triângulo** (pera) | Mandíbula mais larga que a testa | Peso em cima: clubmaster, gatinho suave, topo marcado e mais largo que a mandíbula | Armação estreita e baixa, peso embaixo |
| **Diamante** (losango) | Maçãs largas, testa e queixo estreitos | Oval, gatinho suave, sem aro, topo que alarga a testa | Armação mais estreita que as maçãs, geométrico pontudo |

## 3. Traços que mudam a escolha

- **Sobrancelha.** A barra de cima segue a sobrancelha e fica na linha dela ou logo abaixo. Ela nunca corta a sobrancelha ao meio nem a deixa inteira aparecendo por cima. Sobrancelha reta pede topo reto; arqueada pede topo que acompanhe o arco.
- **Distância entre os olhos** (compare a distância entre os cantos internos com a largura de um olho):
  - olhos **afastados** (distância > 1 olho): ponte escura ou dupla, que aproxima;
  - olhos **próximos** (< 1 olho): ponte fina e clara ou ponte *keyhole*, que afasta.
- **Nariz.**
  - **Ponte nasal baixa** (vê-se no perfil: a raiz do nariz quase na linha dos olhos): acetato só com ponte que case com o nariz. Prefira plaquetas ajustáveis, versão *low bridge fit* / *asian fit* ou apoio nasal embutido alto. Do contrário a armação escorrega e a lente encosta na bochecha.
  - **Nariz longo:** ponte mais baixa ou dupla encurta.
  - **Nariz curto:** ponte alta e clara alonga.
- **Maçãs altas ou proeminentes.** Limitam a altura da lente (`alvo.altura_lente_max` do `medir.py`). Teste do sorriso obrigatório.
- **Assimetria** (sobrancelha ou olho mais alto). Armação com topo menos reto e cor média disfarça; aro muito reto e contrastante evidencia.
- **Barba e cabelo** contam como massa visual.
  - Cavanhaque com laterais raspadas alonga o terço inferior.
  - Barba cheia encorpa a mandíbula: pede armação com presença em cima.
  - Cabeça raspada ou calvície: testa ampla pede barra superior marcada.
  - Pergunte se a barba ou o cabelo mudam com frequência.
- **Idade e pele madura.** Cores que iluminam (havana claro, mel, metal quente) costumam favorecer mais que preto duro rente à pele. É sugestão, não regra: confira na foto.

## 4. Cor

**Subtom** (quente, frio ou neutro). A foto engana: balanço de branco e luz alteram a pele.
- Leia em mais de uma foto: veja reflexos na testa e nas maçãs, o tom dos lábios e o contraste com o fundo neutro.
- Selo ⚠️ sempre.
- Na dúvida, pergunte ao cliente: "dourado ou prateado fica melhor em você?".

| Subtom | Armação | Evitar como curinga |
|---|---|---|
| Quente | Havana, tartaruga, mel, marrom, dourado, oliva, vinho | Prata fria, cinza azulado, cristal gelo |
| Frio | Preto, cinza, prata, azul-marinho, ameixa, tartaruga fria ("blonde"/cinza) | Laranja, mel, dourado amarelo |
| Neutro | Quase tudo. Use contraste pessoal para decidir | Nada específico |

**Contraste pessoal** (diferença entre o tom da pele, do cabelo e dos olhos):
- **Alto contraste** (ex.: pele clara com cabelo escuro, ou pele retinta com olhos muito claros): aguenta armação de contraste alto (preto, tartaruga escura).
- **Baixo contraste:** tons próximos dos seus (havana médio, mel, cinza médio, metal fosco).

**Pele negra.**
- Havana escuro, dourado e preto funcionam pelo contraste com olhos e cabelo.
- Cristal e cores muito claras tendem a "sumir" ou a criar um aro claro artificial.
- Confirme na foto, sem generalizar.

**Estampas.** Tartaruga de alto contraste (manchas claras grandes) chama atenção. Para estilo "discreto", prefira **sólido** ou tartaruga escura de manchas pequenas. Lição real: o cliente achou a estampa tartaruga "too much" e preferiu o mesmo formato em marrom sólido.

## 5. Público e estilo (o que o cliente vai sentir no espelho)

- **Confirme o público do modelo** (masculino, feminino, unissex) na página da loja. O Polaroid PLD 4108/S, de categoria feminina, foi descartado pelo cliente como "muito feminino".
- Detalhes lidos como femininos: asa de gatinho pronunciada, borboleta oversized, metal com ornamento, cores rosé, lente degradê rosa. Lidos como masculinos: barra dupla grossa, aviador com barra dupla, aro reto pesado. Respeite o pedido, sem estereótipo além disso.
- Traduza o estilo pedido em atributos verificáveis:
  - **clássico/discreto:** sólido, formas consagradas (wayfarer, quadrado suave, panto, aviador), logo pequeno, cor sóbria;
  - **moderno:** geométrico, metal fino, cores translúcidas;
  - **criativo:** cor, espessura, formas incomuns;
  - **executivo:** metal ou acetato fino, preto, havana escuro ou titânio.
- "Too much" costuma vir de: logo grande, estampa contrastante, espelhado colorido, espessura exagerada. Na dúvida, ofereça a versão sóbria do mesmo formato.

## 6. Caimento ideal (o gabarito da foto anotada e do checklist)

- Largura total ≈ têmporas. Não aperta, não sobra mais de 1 dedo de cada lado.
- Olho na metade de cima da lente e levemente para dentro do centro horizontal.
- A barra de cima acompanha a sobrancelha. A lente não encosta na bochecha ao sorrir.
- A ponte apoia por igual sem marcar o nariz, e os óculos não descem ao inclinar a cabeça.
- A haste fica reta até a orelha e só então curva. Não pressiona a têmpora.
