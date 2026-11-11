# Medidas: das fotos aos milímetros

Leia na fase 2. O objetivo é sair com o **alvo de compra** (lente □ ponte · haste, mais a largura total) e saber o quanto confiar nele.

## Notação do óptico (sistema *boxing*, ISO 8624)

`55□19 145` = **lente** (A, largura horizontal da lente, mm) □ **ponte** (DBL, distância entre as lentes) · **haste** (comprimento total).
- **B** = altura da lente. Raramente vem gravada; procure na página da loja. Importa para rosto longo e para multifocal.
- **Largura total da frente** ≈ 2A + DBL + ~12 mm de blocos laterais. Varia de 8 a 16 mm conforme o desenho: o wayfarer tem bloco largo, o metal tem bloco estreito. Quando a loja informa a largura total, use a da loja.

## Marcar os pontos

1. `python3 scripts/grade.py FOTO --saida grade.png` mostra a foto com grade em px. Olhe a imagem.
2. Para cada região, amplie: `--recorte x0,y0,x1,y1 --zoom 3`. Olhos e íris, ponte nasal, têmporas, orelha no perfil.
3. Escreva `pontos.json` (formato no cabeçalho do `medir.py`). Coordenadas são sempre da foto original girada pelo EXIF.
4. **Confira:** `grade.py FOTO --pontos pontos.json --vista frente`. Corrija qualquer cruz fora do lugar antes de medir.

| Ponto | Onde marcar |
|---|---|
| `pupila_d/e` | Centro da pupila |
| `iris_d/e` | As duas bordas **horizontais** da íris (limbo), na altura da pupila |
| `temporas` | Largura do rosto na altura das têmporas (logo acima da linha dos olhos, onde a haste passa) |
| `zigomas` | Ponto mais largo das maçãs |
| `mandibula` | Ângulos da mandíbula (gônio). Com barba cheia, estime pelo contorno do osso, não do pelo |
| `linha_cabelo` / `queixo` | Linha do cabelo no centro da testa (com calvície, onde a testa encontraria a linha original) / ponta do queixo (osso, não a barba) |
| `ponte_nasal` | Largura do nariz onde as plaquetas ou a ponte apoiam: ≈ 5–10 mm abaixo da linha dos cantos internos dos olhos |
| `sobrancelha` / `bochecha` | Na vertical da pupila: borda de baixo da sobrancelha / topo da maçã |
| Perfil: `cornea`, `orelha` | Ápice da córnea / raiz superior da orelha, onde a haste dobra |
| Perfil: `pupila`, `queixo` | Para transferir a escala da frente para o perfil |
| Com óculos: `lente_d/e` | Bordas interna e externa **visíveis** da lente (o canal do aro esconde ~0,5 mm de cada lado: aceitável) |

## Escala (de px para mm), da melhor para a pior

1. **DP da receita ou medida pela ótica** (`receita.dp`) dá a escala da frente. ✅ para a escala, ⚠️ para as medidas derivadas.
2. **Armação atual conhecida** (entrada B): A e A+DBL na foto com óculos dão mm/px e daí a DP. A DP leva a escala para a foto sem óculos. Margem típica de ±3%.
3. **Íris:** diâmetro horizontal visível ≈ **11,7 mm** em adultos (±0,5 mm). Margem de ±5%. Sempre ⚠️.
4. **Nada disso:** só proporções, sem mm. Diga isso no slide da régua e peça uma foto melhor se o alvo de medida for decisivo.

Na entrada B, o `medir.py` compara a escala pela DP com a escala pela íris. Divergência > 8% indica marcação ruim ou foto distorcida: remarque antes de seguir.

O perfil não tem escala própria: o `medir.py` a transfere pela distância vertical pupila → queixo medida na frente.

## Fórmulas (as do `medir.py`)

- **Largura-alvo da frente:** W = têmporas (ou 0,97 × maçãs se as têmporas não aparecem).
  - Grau: W ± 2 mm.
  - Sol: W até W + 4 mm (lente maior protege mais).
- **Lente:** A ≈ (largura-alvo − ponte − 12) / 2, ±1 mm. Aviador: +4 a +6 mm, porque o desenho em gota precisa de mais largura.
- **Ponte (acetato):** largura do nariz no apoio, até +2 mm, limitada a 14–24. Metal com plaquetas: a ponte nominal importa menos.
- **Haste:** córnea → orelha + 12 (vértice) + 35 (queda atrás da orelha), arredondado para os tamanhos comerciais (135/140/145/150).
- **Altura máxima da lente:** sobrancelha → topo da maçã − 2 mm.
- **Descentração por olho (grau):** (A + DBL − DP) / 2. Ver `grau-vs-sol.md`.

## Leitura qualitativa da armação atual (entrada B)

É a calibração mais valiosa: o cliente já vive com essa armação. Observe e registre:
- **Dobradiças** por dentro do contorno das têmporas = estreita. Muito por fora = larga.
- **Olho no centro** da lente ou deslocado para dentro/fora.
- **Ponte** apoia por igual, desce ou fica "flutuando". Marcas vermelhas no nariz na foto indicam ponte estreita.
- **Lente encosta na bochecha?** Sobra altura?
- **Haste** reta até a orelha ou forçando para baixo, que indica haste curta.

Exemplo real: com `51□21 140` em panto, as dobradiças ficavam por dentro das têmporas e a haste era curta. A ponte de 21 apoiava bem. Alvo: lente 54–56, ponte 19–21, haste 145–150.

## Fontes de erro (cite as que valerem no slide de pontos fracos)

- **Selfie de perto** (< 50 cm): a grande angular aumenta o nariz e estreita as laterais. Peça foto a 1–1,5 m com zoom de 2×, câmera na altura dos olhos.
- **Cabeça girada:** as distâncias pupila → borda do rosto diferem > 8% entre os lados. Cabeça inclinada: o `medir.py` corrige o giro no plano, não a rotação.
- **Cabelo cobrindo as têmporas**, barba cobrindo a mandíbula, óculos na cabeça, maquiagem de contorno.
- **Foto de perfil** que não está a 90°: a córnea → orelha encolhe.

**Tolerâncias práticas:**
- lente: ±2 mm é aceitável;
- ponte em acetato: ±1 mm;
- haste: o comprimento não se ajusta, só a curvatura;
- uma haste de 140 num alvo de 145 serve se a ótica ajustar a curva.
