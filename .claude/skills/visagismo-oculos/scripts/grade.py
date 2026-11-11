#!/usr/bin/env python3
"""Sobrepõe uma grade de coordenadas (em px da foto original) para ler pontos do rosto com precisão.

Uso:
  python3 grade.py FOTO --saida grade.png [--passo 50] [--recorte x0,y0,x1,y1] [--zoom 2]
                   [--pontos pontos.json --vista frente]

- As coordenadas impressas são SEMPRE da foto original já girada pelo EXIF
  (a mesma referência que medir.py e anotar.py usam).
- --recorte + --zoom: amplia uma região (olhos, ponte nasal, orelha) mantendo os rótulos na referência original.
- --pontos: desenha os pontos já marcados (cruz + nome) para conferir a marcação antes de medir.
- Imprime no terminal o tamanho da foto e o passo usado.
"""
import argparse, json, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps


def carregar(caminho):
    try:
        img = Image.open(caminho)
    except Exception as e:  # HEIC sem plugin, arquivo corrompido etc.
        sys.exit(f"ERRO: não consegui abrir {caminho}: {e}. Se for HEIC, peça a foto em JPG ou PNG.")
    return ImageOps.exif_transpose(img).convert("RGB")


def fonte(tam):
    try:
        return ImageFont.load_default(size=tam)
    except TypeError:
        return ImageFont.load_default()


def achatar_pontos(obj, prefixo=""):
    """Transforma {nome: [x,y] | [[x,y],[x,y]]} numa lista de (rótulo, (x,y))."""
    saida = []
    for nome, v in obj.items():
        if isinstance(v, list) and v and isinstance(v[0], (int, float)):
            saida.append((prefixo + nome, (float(v[0]), float(v[1]))))
        elif isinstance(v, list) and v and isinstance(v[0], list):
            for i, p in enumerate(v):
                saida.append((f"{prefixo}{nome}[{i}]", (float(p[0]), float(p[1]))))
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("foto")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--passo", type=int, default=0, help="px entre linhas (0 = automático)")
    ap.add_argument("--recorte", default="", help="x0,y0,x1,y1 na foto original")
    ap.add_argument("--zoom", type=float, default=1.0)
    ap.add_argument("--pontos", default="", help="pontos.json (formato do medir.py)")
    ap.add_argument("--vista", default="frente", help="chave da vista dentro de pontos.json")
    ap.add_argument("--largura-max", type=int, default=1600)
    a = ap.parse_args()

    img = carregar(a.foto)
    W, H = img.size
    x0, y0, x1, y1 = 0, 0, W, H
    if a.recorte:
        x0, y0, x1, y1 = [int(float(v)) for v in a.recorte.split(",")]
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(W, x1), min(H, y1)
        img = img.crop((x0, y0, x1, y1))

    # escala de exibição: zoom pedido, limitado pela largura máxima
    esc = a.zoom
    if img.width * esc > a.largura_max:
        esc = a.largura_max / img.width
    if esc != 1:
        img = img.resize((max(1, round(img.width * esc)), max(1, round(img.height * esc))), Image.LANCZOS)

    passo = a.passo
    if passo <= 0:
        alvo = min(x1 - x0, y1 - y0) / 16  # ~16 divisões no lado menor
        for p in (5, 10, 20, 25, 50, 100, 200, 250, 500):
            if p >= alvo:
                passo = p
                break
        else:
            passo = 500

    d = ImageDraw.Draw(img, "RGBA")
    f = fonte(max(11, int(13 * max(1, esc) ** 0.5)))
    rot_cada = 2 if (x1 - x0) / passo > 24 else 1

    def px(xo, yo):
        return ((xo - x0) * esc, (yo - y0) * esc)

    k = 0
    xs = (x0 // passo + 1) * passo
    for xv in range(int(xs), int(x1), passo):
        X, _ = px(xv, 0)
        forte = (xv % (passo * 5) == 0)
        d.line([(X, 0), (X, img.height)], fill=(255, 230, 0, 150 if forte else 80), width=2 if forte else 1)
        if k % rot_cada == 0:
            d.text((X + 2, 2), str(xv), font=f, fill=(255, 255, 0, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
        k += 1
    k = 0
    ys = (y0 // passo + 1) * passo
    for yv in range(int(ys), int(y1), passo):
        _, Y = px(0, yv)
        forte = (yv % (passo * 5) == 0)
        d.line([(0, Y), (img.width, Y)], fill=(0, 230, 255, 150 if forte else 80), width=2 if forte else 1)
        if k % rot_cada == 0:
            d.text((2, Y + 2), str(yv), font=f, fill=(0, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
        k += 1

    if a.pontos:
        with open(a.pontos, encoding="utf-8") as fh:
            dados = json.load(fh)
        vista = dados.get(a.vista, {})
        pts = achatar_pontos(vista.get("pontos", vista))
        r = max(6, 8 * esc)
        alt = f.size + 4 if hasattr(f, "size") else 16
        for i, (nome, (xo, yo)) in enumerate(pts):
            if not (x0 <= xo <= x1 and y0 <= yo <= y1):
                continue
            X, Y = px(xo, yo)
            d.line([(X - r, Y), (X + r, Y)], fill=(255, 40, 40, 255), width=2)
            d.line([(X, Y - r), (X, Y + r)], fill=(255, 40, 40, 255), width=2)
            dy = (i % 3) * alt  # escalona rótulos de pontos vizinhos
            d.text((X + r + 2, Y - r - 2 - dy), nome, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(160, 0, 0, 255))

    img.save(a.saida)
    print(f"foto {W}x{H}px · recorte ({x0},{y0})-({x1},{y1}) · passo {passo}px · escala de exibição {esc:.2f} → {a.saida}")


if __name__ == "__main__":
    main()
