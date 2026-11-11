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
import argparse, base64, io, json, math, os, re, ssl, sys, urllib.request
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anotar import FORMAS, abrir_foto, recortar_codificar, centro_angulo, transform_armacao, escrever_previa, esc  # noqa: E402

BLOCO_MM = 12.0
OPAC = {"degrade": .95, "degrade-marrom": .95, "clara": .55}  # o degradê já traz a transparência no gradiente; lente sólida ≈ .75
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
        return float(p["largura_total"]), p.get("origem_largura", "lida na página")
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


# ---------- foto real do produto ----------

def baixar(url, destino):
    """Baixa a foto do produto (com o CA do proxy, se houver) e guarda em cache."""
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        return destino
    ctx = ssl.create_default_context()
    for f in (os.environ.get("SSL_CERT_FILE"), os.environ.get("REQUESTS_CA_BUNDLE"), "/root/.ccr/ca-bundle.crt"):
        if f and os.path.exists(f):
            try:
                ctx.load_verify_locations(f)
            except Exception:
                pass
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/124"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r, open(destino, "wb") as fh:
        fh.write(r.read(15_000_000))
    return destino


def sem_fundo(caminho):
    """Tira o fundo claro da foto de catálogo (flood fill a partir das bordas) e recorta na armação.
    Pixels claros DENTRO da armação (reflexo, lente degradê) continuam: só o fundo ligado à borda sai."""
    im = Image.open(caminho).convert("RGB")
    L = im.convert("L")
    marca = L.point(lambda v: 255 if v >= 236 else 0)
    w, h = marca.size
    passo = max(8, min(w, h) // 60)
    for x in range(0, w, passo):
        for y in (0, h - 1):
            if marca.getpixel((x, y)) == 255:
                ImageDraw.floodfill(marca, (x, y), 128)
    for y in range(0, h, passo):
        for x in (0, w - 1):
            if marca.getpixel((x, y)) == 255:
                ImageDraw.floodfill(marca, (x, y), 128)
    # fundo = o que se liga à borda + o branco puro preso dentro da armação (entre as barras da ponte,
    # atrás das plaquetas). Lente degradê e reflexos não chegam a esse branco e continuam.
    preso = L.point(lambda v: 255 if v >= 246 else 0)
    fundo = Image.composite(Image.new("L", im.size, 255), preso, marca.point(lambda v: 255 if v == 128 else 0))
    fundo = fundo.filter(ImageFilter.MaxFilter(3))
    borda_suave = L.point(lambda v: max(0, min(255, int((250 - v) * 9))))  # antisserrilhado na borda
    alfa = Image.composite(borda_suave, Image.new("L", im.size, 255), fundo)
    rgba = im.copy()
    rgba.putalpha(alfa)
    caixa = alfa.point(lambda v: 255 if v > 70 else 0).getbbox()
    if not caixa:
        sys.exit(f"ERRO: não achei a armação em {caminho} (fundo não é claro?).")
    return rgba.crop(caixa)


def compor(base, prod, cx, cy, ang, largura_px, ancora_y=0.45):
    """Cola a armação (RGBA) com a largura dada, o ponto (meio, ancora_y·altura) na pupila média, inclinada como a cabeça."""
    w = max(4, round(largura_px))
    h = max(2, round(prod.height * w / prod.width))
    pr = prod.resize((w, h), Image.LANCZOS)
    sombra = Image.new("RGBA", pr.size, (0, 0, 0, 0))
    sombra.putalpha(pr.getchannel("A").point(lambda v: int(v * 0.30)).filter(ImageFilter.GaussianBlur(max(1, w / 110))))
    t = math.radians(ang)
    oy = (ancora_y - 0.5) * h
    dx, dy = -math.sin(t) * oy, math.cos(t) * oy
    out = base.convert("RGBA")
    for camada, desloc in ((sombra, w / 140), (pr, 0)):
        r = camada.rotate(-ang, resample=Image.BICUBIC, expand=True)
        x = round(cx - r.width / 2 - dx)
        y = round(cy - r.height / 2 - dy + desloc)
        out.alpha_composite(r, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))
    return out.convert("RGB")


def recorte_img(img, rec, lado_max):
    W0, H0 = img.size
    x0, y0, x1, y1 = [int(v) for v in rec]
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W0, x1), min(H0, y1)
    c = img.crop((x0, y0, x1, y1))
    k = min(1.0, lado_max / max(c.size))
    if k < 1:
        c = c.resize((round(c.width * k), round(c.height * k)), Image.LANCZOS)
    return c


def jpeg_b64(img, q=80):
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode(), len(buf.getvalue()) / 1024


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dados"); ap.add_argument("medidas"); ap.add_argument("pontos")
    ap.add_argument("--foto", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--preview", default="")
    ap.add_argument("--sem-atual", action="store_true")
    ap.add_argument("--com-referencia", action="store_true")
    ap.add_argument("--lado-max", type=int, default=760)
    ap.add_argument("--foto-oculos", default="", help="foto de frente COM a armação atual: vira o cartão 'seus óculos de hoje' (foto real)")
    ap.add_argument("--pasta-produtos", default="rascunho/produtos", help="cache das fotos de produto baixadas")
    ap.add_argument("--so-desenho", action="store_true", help="ignora foto_frente_url e desenha todas as armações")
    a = ap.parse_args()
    D = json.load(open(a.dados, encoding="utf-8"))
    M = json.load(open(a.medidas, encoding="utf-8"))
    PJ = json.load(open(a.pontos, encoding="utf-8"))
    F = PJ["frente"]["pontos"]
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
    rosto = recorte_img(img, rec, a.lado_max)
    cx, cy, ang = centro_angulo(P(pd), P(pe))
    guias = ""
    if F.get("temporas"):  # tracejado nas têmporas: a sobra ou a falta fica visível
        for t in F["temporas"]:
            x, _ = P(t)
            guias += f'<line x1="{x:.1f}" y1="{H*0.14:.1f}" x2="{x:.1f}" y2="{H*0.62:.1f}" style="stroke:rgba(255,255,255,.8);stroke-width:{max(1.5, W/260):.1f};stroke-dasharray:{W/90:.1f} {W/120:.1f}"/>'

    itens = [dict(p) for p in D.get("produtos", []) if p.get("papel") != "referencia" or a.com_referencia]
    at = D.get("armacao_atual")
    if at and not a.sem_atual and at.get("lente") and at.get("ponte"):
        forma = next((v for kk, v in FORMATO_TEXTO.items() if kk in (at.get("formato") or "").lower()), "softsq")
        medida = (M.get("medidas", {}).get("armacao_atual_largura_total") or {}).get("mm")
        itens.append({"id": "atual", "papel": "atual", "nome_curto": f"{at['lente']}□{at['ponte']} {at.get('haste', '')}".strip(),
                      "formato": forma, "lente": at["lente"], "ponte": at["ponte"], "largura_total": round(medida) if medida else None,
                      "material": at.get("material", ""), "cor": at.get("cor", ""), "lente_tipo": "clara", "origem_largura": "medida na foto"})
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
        # veredito de largura: a mesma faixa-alvo do dossiê (alvo.largura_total); sem ela, ±3 mm das têmporas
        faixa = (D.get("alvo") or {}).get("largura_total")
        if faixa:
            lo, hi = faixa
        elif temporas:
            lo, hi = temporas - 3, temporas + 3
        else:
            lo = hi = None
        if lo is None:
            chip, veredito = "c-unk", "sem medida do rosto"
        elif lo <= round(mm) <= hi:
            chip, veredito = "c-ok", "largura no alvo"
        elif mm > hi:
            chip, veredito = "c-warn", f"sobra ≈ {mm - (temporas or hi):.0f} mm"
        else:
            chip, veredito = "c-warn", f"estreita ≈ {(temporas or lo) - mm:.0f} mm"
        # outras medidas fora do alvo do formato (ex.: ponte), para o chip verde não enganar
        avisos = []
        if p.get("papel") != "atual":
            alvo_p = dict(D.get("alvo") or {}); alvo_p.update((D.get("alvo_por_formato") or {}).get(forma, {}))
            for campo in ("ponte", "haste", "lente"):
                f, v = alvo_p.get(campo), p.get(campo)
                if f and v is not None and not (f[0] <= v <= f[1]):
                    avisos.append(f"{campo} {v}")
        nome = nome_de(p)
        star = " star" if p.get("papel") == "curinga" else ""
        modo, corpo = "desenho", None
        if p.get("papel") == "atual" and a.foto_oculos and PJ.get("com_oculos_frente") and esc_.get("com_oculos_mm_por_px"):
            # a foto real com os óculos de hoje, enquadrada igual às outras (mesma escala e centro nas pupilas)
            B = PJ["com_oculos_frente"]["pontos"]
            r = s / esc_["com_oculos_mm_por_px"]
            bx, by = (B["pupila_d"][0] + B["pupila_e"][0]) / 2, (B["pupila_d"][1] + B["pupila_e"][1]) / 2
            fx, fy = (pd[0] + pe[0]) / 2, (pd[1] + pe[1]) / 2
            recB = [bx + (rec[0] - fx) * r, by + (rec[1] - fy) * r, bx + (rec[2] - fx) * r, by + (rec[3] - fy) * r]
            fotoB = recorte_img(abrir_foto(a.foto_oculos), recB, a.lado_max * 2).resize((W, H), Image.LANCZOS)
            pb64, _ = jpeg_b64(fotoB)
            corpo = f'<image href="data:image/jpeg;base64,{pb64}" width="{W}" height="{H}"/>{guias}'
            modo = "sua foto real"
        elif p.get("foto_frente_url") and not a.so_desenho:
            os.makedirs(a.pasta_produtos, exist_ok=True)
            ext = os.path.splitext(p["foto_frente_url"].split("?")[0])[1] or ".jpg"
            arq = baixar(p["foto_frente_url"], os.path.join(a.pasta_produtos, f"{p.get('id')}{ext}"))
            comp = compor(rosto, sem_fundo(arq), cx, cy, ang, mm / s * k, float(p.get("ancora_y", 0.45)))
            pb64, _ = jpeg_b64(comp)
            corpo = f'<image href="data:image/jpeg;base64,{pb64}" width="{W}" height="{H}"/>{guias}'
            modo = "foto da loja"
        if corpo is None:
            corpo = (f'<use href="#prov-foto"/>{guias}'
                     f'<g transform="{tr}">'
                     f'<use href="#l-{forma}" width="300" height="110" style="fill:url(#lg-{lente});opacity:{OPAC.get(lente, .75)}"/>'
                     f'<use href="#f-{forma}" width="300" height="110" style="fill:none;stroke:rgba(255,255,255,.28);stroke-width:{halo:.2f};stroke-linejoin:round"/>'
                     f'<use href="#f-{forma}" width="300" height="110" style="fill:none;stroke:{cor};stroke-width:{aro:.2f};stroke-linejoin:round;stroke-linecap:round"/>'
                     f'</g>')
            if p.get("papel") != "atual":
                modo = "desenho (a loja não tem foto de frente)"
        cards.append(
            f'<figure class="prov-card{star}" data-produto="{esc(p.get("id"))}" data-modo="{esc(modo)}">\n'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(nome)} no rosto, em escala ({esc(modo)})">'
            + corpo + '</svg>\n'
            f'<figcaption><span class="eyebrow">{esc(p.get("rotulo") or PAPEL_ROTULO.get(p.get("papel"), p.get("papel")))}</span>'
            f'<b class="mono">{esc(nome)}</b>'
            f'<span class="mono">frente ≈ {mm:.0f} mm ({origem})</span>'
            f'<span class="mono">{esc(modo)}</span>'
            f'<span class="chip {chip}">{esc(veredito)}</span>'
            + "".join(f'<span class="chip c-warn">{esc(x)} fora do alvo</span>' for x in avisos)
            + '</figcaption>\n</figure>')
        linhas.append(f"  {p.get('id'):<16} {modo[:12]:<12} {forma:<10} frente {mm:5.1f} mm ({origem}) · {veredito}" + (f" · {', '.join(avisos)} fora do alvo" if avisos else ""))

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
