#!/usr/bin/env python3
"""Gera a foto anotada (fragmento <figure class="photo">) para colar na apresentação.

Uso:
  python3 anotar.py spec.json --saida frente.fig.html [--preview frente.preview.html --tema sol|grau]

spec.json (coordenadas em px da foto ORIGINAL, já girada pelo EXIF, as mesmas do grade.py):
{
  "foto": "frente.jpg",
  "recorte": [x0, y0, x1, y1],            # opcional: enquadrar o rosto (recomendado: ombros para cima)
  "lado_max": 1100, "qualidade": 78,      # opcional: tamanho do JPEG embutido
  "medidas": [ {"de": [x,y], "ate": [x,y], "rotulo": "têmporas ≈ 142 mm", "pos": "acima", "tipo": "med"} ],
  "guias":   [ {"de": [x,y], "ate": [x,y], "rotulo": "linha da sobrancelha"} ],
  "marcos":  [ {"xy": [x,y], "rotulo": "ponte nasal", "pos": "direita"} ],
  "armacao": {"forma": "softsq", "pupilas": [[x,y],[x,y]], "largura_px": 520, "lente": "marrom"},
  "alt": "Foto de frente com as medidas do rosto e a armação ideal simulada",
  "legenda": "Medidas estimadas pela íris (±5%). A armação é uma simulação do formato."
}
- "pos": acima | abaixo | esquerda | direita (lado do rótulo). "tipo": med (padrão) | alerta.
- "armacao": a forma simulada, na escala certa. largura_px = largura total da frente em mm ÷ (mm por px).
  "pupilas" alinha e inclina a forma pela linha dos olhos. Sem pupilas, use "centro": [x,y] e "angulo" (graus).
  "lente" (opcional) = g15 | marrom | cinza | degrade | clara: tinge as lentes de leve.
- Formas: softsq aviador panto redondo retangular wayfarer gatinho clubmaster geometrico oval.
O fragmento usa os <symbol> do template: só funciona colado no deck (ou no --preview).
"""
import argparse, base64, html, io, json, math, os, re, sys
from PIL import Image, ImageOps


def _registrar_heif():
    """iPhone e Android salvam em HEIC. Pillow lê via pillow-heif (pip install pillow-heif)."""
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
        return True
    except ImportError:
        return False

AQUI = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(AQUI, "..", "assets", "template.html")
FORMAS = {"softsq", "aviador", "panto", "redondo", "retangular", "wayfarer", "gatinho", "clubmaster", "geometrico", "oval"}
LENTES = {"g15", "marrom", "cinza", "degrade", "degrade-marrom", "clara"}


def esc(t):
    return html.escape(str(t), quote=True)


# ---- funções comuns (usadas também pelo provador.py) ----

def abrir_foto(foto):
    """Abre a foto (JPG, PNG ou HEIC) já girada pelo EXIF, a mesma referência de coordenadas do grade.py."""
    if foto.lower().endswith((".heic", ".heif")) and not _registrar_heif():
        sys.exit("ERRO: foto HEIC e pillow-heif não instalado. Rode: pip install pillow-heif (ou converta para JPG).")
    try:
        return ImageOps.exif_transpose(Image.open(foto)).convert("RGB")
    except Exception as e:
        sys.exit(f"ERRO: não consegui abrir {foto}: {e}")


def recortar_codificar(img, recorte=None, lado_max=1100, qualidade=78):
    """Recorta, reduz e codifica em JPEG base64. Devolve (b64, W, H, P, k, kb), onde P converte coordenadas da foto original."""
    W0, H0 = img.size
    x0, y0, x1, y1 = recorte or [0, 0, W0, H0]
    x0, y0, x1, y1 = max(0, int(x0)), max(0, int(y0)), min(W0, int(x1)), min(H0, int(y1))
    img = img.crop((x0, y0, x1, y1))
    k = min(1.0, lado_max / max(img.size))
    if k < 1:
        img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=int(qualidade), optimize=True, progressive=True)

    def P(p):
        return ((float(p[0]) - x0) * k, (float(p[1]) - y0) * k)
    return base64.b64encode(buf.getvalue()).decode(), img.width, img.height, P, k, len(buf.getvalue()) / 1024


def centro_angulo(pa, pb):
    """Centro e inclinação (graus) da linha das pupilas, já em coordenadas de saída."""
    (ax, ay), (bx, by) = pa, pb
    if ax > bx:
        (ax, ay), (bx, by) = (bx, by), (ax, ay)
    return (ax + bx) / 2, (ay + by) / 2, math.degrees(math.atan2(by - ay, bx - ax))


def transform_armacao(cx, cy, ang, largura_px_saida):
    """Transform SVG que põe um símbolo f-*/l-* (300 unidades = largura total da frente) com a pupila média em (cx, cy)."""
    sc = largura_px_saida / 300.0
    return f"translate({cx:.1f} {cy:.1f}) rotate({ang:.2f}) scale({sc:.4f}) translate(-150 -50)", sc


def escrever_previa(frag, tema, saida, titulo="Prévia"):
    with open(TEMPLATE, encoding="utf-8") as fh:
        t = fh.read()
    estilo = re.search(r"<style>.*?</style>", t, re.S).group(0)
    defs = re.search(r"<!-- DEFS:INICIO.*?<!-- DEFS:FIM -->", t, re.S).group(0)
    pv = (f'<meta charset="utf-8"><title>{esc(titulo)}</title>\n{estilo}\n{defs}\n'
          f'<main class="deck t-{tema}"><section class="slide"><div class="wrap">\n{frag}</div></section></main>\n')
    with open(saida, "w", encoding="utf-8") as fh:
        fh.write(pv)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--preview", default="")
    ap.add_argument("--tema", default="sol", choices=["sol", "grau"])
    a = ap.parse_args()

    with open(a.spec, encoding="utf-8") as fh:
        s = json.load(fh)
    base = os.path.dirname(os.path.abspath(a.spec))
    # caminho da foto: absoluto, relativo à pasta atual (ex.: rodando da pasta do caso) ou relativo ao spec
    foto = s["foto"]
    if not os.path.isabs(foto) and not os.path.exists(foto):
        foto = os.path.join(base, foto)
    img = abrir_foto(foto)
    b64, W, H, P, k, kb = recortar_codificar(img, s.get("recorte"), int(s.get("lado_max", 1100)), int(s.get("qualidade", 78)))

    sw = max(2.0, W / 260)          # espessura da linha
    fs = max(14.0, W / 34)          # tamanho do rótulo
    tick = W / 70
    pad = fs * 0.5
    out = []

    def rotulo(x, y, texto, ancora="middle"):
        tw = len(texto) * fs * 0.6
        if ancora == "middle":
            x = min(max(x, tw / 2 + pad), W - tw / 2 - pad)
        elif ancora == "start":
            x = min(max(x, pad), W - tw - pad)
        else:
            x = min(max(x, tw + pad), W - pad)
        y = min(max(y, fs + pad), H - pad)
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs:.1f}" stroke-width="{fs*0.24:.1f}" text-anchor="{ancora}">{esc(texto)}</text>')

    def deslocamento(pos, dist):
        return {"acima": (0, -dist), "abaixo": (0, dist + fs * 0.75), "esquerda": (-dist, fs * 0.35), "direita": (dist, fs * 0.35)}.get(pos, (0, -dist))

    for g in s.get("guias", []):
        (ax, ay), (bx, by) = P(g["de"]), P(g["ate"])
        out.append(f'<line class="a-guia" x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke-width="{sw*0.8:.1f}"/>')
        if g.get("rotulo"):
            dx, dy = deslocamento(g.get("pos", "acima"), fs * 0.5)
            rotulo(bx + dx, by + dy, g["rotulo"], "end" if g.get("pos", "acima") != "direita" else "start")

    for m in s.get("medidas", []):
        (ax, ay), (bx, by) = P(m["de"]), P(m["ate"])
        cls = "a-alerta" if m.get("tipo") == "alerta" else "a-med"
        L = math.hypot(bx - ax, by - ay) or 1
        nx, ny = -(by - ay) / L, (bx - ax) / L  # normal
        linhas = [(ax, ay, bx, by), (ax - nx * tick, ay - ny * tick, ax + nx * tick, ay + ny * tick),
                  (bx - nx * tick, by - ny * tick, bx + nx * tick, by + ny * tick)]
        for (p, q, r, t) in linhas:
            out.append(f'<line class="a-halo" x1="{p:.1f}" y1="{q:.1f}" x2="{r:.1f}" y2="{t:.1f}" stroke-width="{sw*2.6:.1f}"/>')
        for (p, q, r, t) in linhas:
            out.append(f'<line class="{cls}" x1="{p:.1f}" y1="{q:.1f}" x2="{r:.1f}" y2="{t:.1f}" stroke-width="{sw:.1f}"/>')
        if m.get("rotulo"):
            mx, my = (ax + bx) / 2, (ay + by) / 2
            pos = m.get("pos", "acima")
            dx, dy = deslocamento(pos, tick + fs * 0.35)
            anc = "middle" if pos in ("acima", "abaixo") else ("end" if pos == "esquerda" else "start")
            rotulo(mx + dx, my + dy, m["rotulo"], anc)

    for mk in s.get("marcos", []):
        x, y = P(mk["xy"])
        r = max(4.0, W / 150)
        out.append(f'<circle class="a-marco" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" stroke-width="{sw:.1f}"/>')
        if mk.get("rotulo"):
            pos = mk.get("pos", "direita")
            dx, dy = deslocamento(pos, r + fs * 0.4)
            anc = "middle" if pos in ("acima", "abaixo") else ("end" if pos == "esquerda" else "start")
            rotulo(x + dx, y + dy, mk["rotulo"], anc)

    arm = s.get("armacao")
    if arm:
        forma = arm.get("forma", "softsq")
        if forma not in FORMAS:
            sys.exit(f"ERRO: forma '{forma}' não existe. Use uma de: {', '.join(sorted(FORMAS))}")
        if "pupilas" in arm:
            cx, cy, ang = centro_angulo(P(arm["pupilas"][0]), P(arm["pupilas"][1]))
        else:
            cx, cy = P(arm["centro"])
            ang = float(arm.get("angulo", 0))
        tr, sc = transform_armacao(cx, cy, ang, float(arm["largura_px"]) * k)
        stroke_simb = max(2.0, W / 230) / sc
        lente = arm.get("lente")
        g = [f'<g transform="{tr}">']
        if lente:
            if lente not in LENTES:
                sys.exit(f"ERRO: lente '{lente}' não existe. Use uma de: {', '.join(sorted(LENTES))}")
            g.append(f'<use class="a-lente" href="#l-{forma}" width="300" height="110" style="fill:url(#lg-{lente})"/>')
        g.append(f'<use class="a-halo" href="#f-{forma}" width="300" height="110" stroke-width="{stroke_simb*2.4:.2f}"/>')
        g.append(f'<use class="a-armacao" href="#f-{forma}" width="300" height="110" stroke-width="{stroke_simb:.2f}"/>')
        g.append("</g>")
        out.extend(g)

    alt = s.get("alt", "Foto do rosto com marcações de medida")
    leg = s.get("legenda", "")
    frag = (f'<figure class="photo">\n<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">\n'
            f'<image href="data:image/jpeg;base64,{b64}" width="{W}" height="{H}"/>\n<g class="anno">\n'
            + "\n".join(out) + "\n</g>\n</svg>\n"
            + (f"<figcaption>{esc(leg)}</figcaption>\n" if leg else "") + "</figure>\n")
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(frag)
    print(f"{a.saida}: {W}x{H}px · JPEG {kb:.0f} KB · fragmento {len(frag)/1024:.0f} KB")

    if a.preview:
        escrever_previa(frag, a.tema, a.preview, "Prévia da anotação")
        print(f"prévia: {a.preview} (capture com: node render.js {a.preview} <pasta>)")


if __name__ == "__main__":
    main()
