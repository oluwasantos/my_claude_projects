#!/usr/bin/env python3
"""Provador: cada óculos recomendado desenhado na foto de frente do cliente, em escala real.

Uso (da pasta do caso):
  python3 provador.py dados.json medidas.json pontos.json --foto fotos/frente.jpg \\
      --saida rascunho/provador.fig.html [--preview rascunho/provador.preview.html] [--sem-atual] [--com-referencia]

Para cada produto (curinga, complemento, alternativa; referência só com --com-referencia) e para a
armação atual (entrada B), desenha o formato da biblioteca do template na largura real da frente:
  frente (mm) = largura_total lida na página ou 2·lente + ponte + 12 (estimada)
  frente (px) = frente (mm) ÷ escala da foto de frente (medidas.escala.frente_mm_por_px_*)
centrada e inclinada pela linha das pupilas. Aro com a cor (cor_css ou cor) e a espessura do material;
lente tingida pelo lente_tipo. Veredito: frente − têmporas (≤ 3 mm encaixa).

Saída: <div class="provador"> com a foto embutida uma vez e um cartão (data-produto) por modelo.
É simulação: tamanho e formato fiéis à escala da foto; cor, brilho e perspectiva aproximados.
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anotar import FORMAS, abrir_foto, recortar_codificar, centro_angulo, transform_armacao, escrever_previa, esc  # noqa: E402

BLOCO_MM = 12.0
PAPEL_ROTULO = {"curinga": "Curinga", "complemento": "Complemento", "alternativa": "Alternativa",
                "referencia": "Referência para provar", "atual": "Seus óculos de hoje"}
ORDEM = {"curinga": 0, "complemento": 1, "alternativa": 2, "referencia": 3, "atual": 4}
FORMATO_TEXTO = {"panto": "panto", "redond": "redondo", "aviad": "aviador", "wayfarer": "wayfarer", "gatinho": "gatinho",
                 "club": "clubmaster", "retang": "retangular", "oval": "oval", "geom": "geometrico", "hexag": "geometrico",
                 "quadrad": "softsq"}


def cor_de(p):
    if p.get("cor_css"):
        return p["cor_css"]
    c = (p.get("cor") or "").lower()
    for chave, val in (("tartaruga", "url(#p-tartaruga)"), ("havana", "url(#p-tartaruga)"), ("dourad", "#c9a24c"),
                       ("ouro", "#c9a24c"), ("marrom", "#5b3922"), ("preto", "#151312"), ("ônix", "#2a2a2c"),
                       ("onix", "#2a2a2c"), ("prata", "#b9bdc3"), ("grafite", "#4a4d52"), ("azul", "#2b3a55"),
                       ("verde", "#3c4a3a"), ("vinho", "#5a1f2a"), ("bege", "#c8b49a"), ("nude", "#c8b49a"),
                       ("cristal", "rgba(230,235,240,.55)"), ("transparente", "rgba(230,235,240,.55)")):
        if chave in c:
            return val
    return "#333333"


def lente_de(p, tipo_caso):
    t = (p.get("lente_tipo") or "").lower()
    if "degrad" in t:
        return "degrade-marrom" if "marrom" in t else "degrade"
    for chave, val in (("g-15", "g15"), ("g15", "g15"), ("verde", "g15"), ("cinza", "cinza"), ("fum", "cinza"), ("marrom", "marrom")):
        if chave in t:
            return val
    return "clara" if tipo_caso == "grau" or p.get("papel") == "atual" else "cinza"


def espessura_mm(p):
    m = (p.get("material") or "").lower()
    if any(x in m for x in ("aço", "aco", "metal", "titân", "titan", "inox", "alumín", "alumin", "monel")):
        return 1.3
    return 4.5


def frente_mm(p):
    if p.get("largura_total"):
        return float(p["largura_total"]), "lida"
    return 2 * float(p["lente"]) + float(p["ponte"]) + BLOCO_MM, "estimada"


FORMA_NOME = {"softsq": "Quadrado", "aviador": "Aviador", "panto": "Panto", "redondo": "Redondo", "retangular": "Retangular",
              "wayfarer": "Wayfarer", "gatinho": "Gatinho", "clubmaster": "Clubmaster", "geometrico": "Geométrico", "oval": "Oval"}


def nome_de(p):
    """Nome curto para o cartão: nome_curto, ou "<forma> <número do código>" (ex.: Aviador 4000)."""
    if p.get("nome_curto"):
        return p["nome_curto"]
    num = [x for x in re.split(r"[.\s·]+", p.get("codigo", "")) if x.isdigit() and len(x) >= 3]
    if num:
        return f"{FORMA_NOME.get(p.get('formato'), p.get('modelo', ''))} {num[0]}"
    return p.get("modelo", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dados"); ap.add_argument("medidas"); ap.add_argument("pontos")
    ap.add_argument("--foto", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--preview", default="")
    ap.add_argument("--sem-atual", action="store_true")
    ap.add_argument("--com-referencia", action="store_true")
    ap.add_argument("--lado-max", type=int, default=760)
    a = ap.parse_args()
    D = json.load(open(a.dados, encoding="utf-8"))
    M = json.load(open(a.medidas, encoding="utf-8"))
    F = json.load(open(a.pontos, encoding="utf-8"))["frente"]["pontos"]
    tipo = D["cliente"]["tipo"]

    esc_ = M.get("escala", {})
    fonte = esc_.get("frente_fonte", "")
    s = (esc_.get("frente_mm_por_px_temporas") if fonte.startswith("têmporas") else None) \
        or (esc_.get("frente_mm_por_px_dp") if fonte.startswith("DP") else None) or esc_.get("frente_mm_por_px_iris")
    if not s:
        sys.exit("ERRO: medidas.json sem escala da foto de frente. Sem escala não há provador em tamanho real.")
    temporas = (M.get("medidas", {}).get("largura_temporas") or {}).get("mm")

    # recorte: da testa ao queixo, com folga lateral
    pd, pe = F["pupila_d"], F["pupila_e"]
    cxo = (pd[0] + pe[0]) / 2
    tw = abs(F["temporas"][1][0] - F["temporas"][0][0]) if F.get("temporas") else abs(pe[0] - pd[0]) * 2
    topo = F.get("linha_cabelo", [cxo, min(pd[1], pe[1]) - tw * 0.6])[1]
    base = F.get("queixo", [cxo, max(pd[1], pe[1]) + tw * 0.9])[1]
    alt = base - topo
    rec = [cxo - tw * 0.72, topo - alt * 0.10, cxo + tw * 0.72, base + alt * 0.03]
    img = abrir_foto(a.foto)
    b64, W, H, P, k, kb = recortar_codificar(img, rec, a.lado_max, 78)
    cx, cy, ang = centro_angulo(P(pd), P(pe))

    itens = [dict(p) for p in D.get("produtos", []) if p.get("papel") != "referencia" or a.com_referencia]
    at = D.get("armacao_atual")
    if at and not a.sem_atual and at.get("lente") and at.get("ponte"):
        forma = next((v for kk, v in FORMATO_TEXTO.items() if kk in (at.get("formato") or "").lower()), "softsq")
        medida = (M.get("medidas", {}).get("armacao_atual_largura_total") or {}).get("mm")
        itens.append({"id": "atual", "papel": "atual", "nome_curto": f"{at['lente']}□{at['ponte']} {at.get('haste', '')}".strip(),
                      "formato": forma, "lente": at["lente"], "ponte": at["ponte"], "largura_total": round(medida) if medida else None,
                      "material": at.get("material", ""), "cor": at.get("cor", ""), "lente_tipo": "clara"})
    itens.sort(key=lambda p: ORDEM.get(p.get("papel"), 9))

    cards, linhas = [], []
    for p in itens:
        forma = p.get("formato", "softsq")
        if forma not in FORMAS:
            sys.exit(f"ERRO: {p.get('id')}: formato '{forma}' não está na biblioteca ({', '.join(sorted(FORMAS))}).")
        mm, origem = frente_mm(p)
        tr, sc = transform_armacao(cx, cy, ang, mm / s * k)
        # 1 mm em unidades do símbolo = 300 / frente_mm
        aro = espessura_mm(p) * 300.0 / mm
        halo = aro + 0.8 * 300.0 / mm
        cor = cor_de(p)
        lente = lente_de(p, tipo)
        if temporas:
            d = mm - temporas
            if abs(d) <= 3:
                chip, veredito = "c-ok", "encaixa"
            elif d > 0:
                chip, veredito = "c-warn", f"sobra ≈ {d:.0f} mm"
            else:
                chip, veredito = "c-warn", f"estreita ≈ {-d:.0f} mm"
        else:
            chip, veredito = "c-unk", "sem medida do rosto"
        nome = nome_de(p)
        star = " star" if p.get("papel") == "curinga" else ""
        cards.append(
            f'<figure class="prov-card{star}" data-produto="{esc(p.get("id"))}">\n'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Simulação de {esc(nome)} no rosto, em escala">'
            f'<use href="#prov-foto"/>'
            f'<g transform="{tr}">'
            f'<use href="#l-{forma}" width="300" height="110" style="fill:url(#lg-{lente});opacity:.58"/>'
            f'<use href="#f-{forma}" width="300" height="110" style="fill:none;stroke:rgba(255,255,255,.28);stroke-width:{halo:.2f};stroke-linejoin:round"/>'
            f'<use href="#f-{forma}" width="300" height="110" style="fill:none;stroke:{cor};stroke-width:{aro:.2f};stroke-linejoin:round;stroke-linecap:round"/>'
            f'</g></svg>\n'
            f'<figcaption><span class="eyebrow">{esc(p.get("rotulo") or PAPEL_ROTULO.get(p.get("papel"), p.get("papel")))}</span>'
            f'<b class="mono">{esc(nome)}</b>'
            f'<span class="mono">frente ≈ {mm:.0f} mm{"" if origem == "lida" else " (estimada)"}</span>'
            f'<span class="chip {chip}">{esc(veredito)}</span></figcaption>\n</figure>')
        linhas.append(f"  {p.get('id'):<16} {forma:<10} frente {mm:5.1f} mm ({origem}) · {veredito}")

    frag = (f'<div class="provador">\n<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            f'<image id="prov-foto" href="data:image/jpeg;base64,{b64}" width="{W}" height="{H}"/></defs></svg>\n'
            + "\n".join(cards) + "\n</div>\n")
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(frag)
    print(f"{a.saida}: {len(cards)} cartões · foto {W}x{H}px ({kb:.0f} KB, embutida uma vez) · fragmento {len(frag)/1024:.0f} KB")
    print(f"escala {s:.4f} mm/px ({fonte}) · têmporas ≈ {temporas:.0f} mm" if temporas else f"escala {s:.4f} mm/px ({fonte})")
    print("\n".join(linhas))
    if a.preview:
        escrever_previa(frag, tipo, a.preview, "Prévia do provador")
        print(f"prévia: {a.preview}")


if __name__ == "__main__":
    main()
