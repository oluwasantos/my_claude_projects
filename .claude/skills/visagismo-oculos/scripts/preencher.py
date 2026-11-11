#!/usr/bin/env python3
"""Funções para montar a apresentação a partir do template, num script do caso (rascunho/montar.py).

Uso típico (rodando da pasta do caso):
    import sys; sys.path.insert(0, "<SKILL>/scripts")
    from preencher import carregar_template, repetir, slots, manter_tipo, manter_modo, brl, faltando
    t = carregar_template()
    t = repetir(t, "produto", [ {...slots do produto 1...}, {...} ])   # duplica o bloco REPETIR:produto
    t = repetir(t, "fato-rosto", [ {"FATO_K": "Formato", "FATO_V": "...", "FATO_SELO": "foto"}, ... ])
    t = manter_tipo(t, "sol")                                            # apaga os blocos data-so do outro tipo
    t = manter_modo(t, "foto")                                           # legenda do provador: "foto" ou "desenho"
    t = slots(t, {"TITULO_PAGINA": "...", "FOTO_ANOTADA_FRENTE": open("rascunho/frente.fig.html").read(), ...})
    print(faltando(t)); open("apresentacao.html", "w").write(t)

Mantém os números iguais ao dados.json: use brl(p["preco"]) para todo preço.
"""
import os, re

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "template.html")


def carregar_template():
    with open(TEMPLATE, encoding="utf-8") as fh:
        return fh.read()


def brl(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def repetir(t, nome, itens):
    """Troca o bloco <!-- REPETIR:nome --> ... <!-- /REPETIR:nome --> por uma cópia preenchida por item."""
    m = re.search(r"<!-- REPETIR:%s\b[^>]*-->(.*?)<!-- /REPETIR:%s -->" % (re.escape(nome), re.escape(nome)), t, re.S)
    if not m:
        raise KeyError(f"bloco REPETIR:{nome} não existe no template")
    saida = []
    for it in itens:
        b = m.group(1)
        for k, v in it.items():
            b = b.replace("{{" + k + "}}", str(v))
        saida.append(b)
    return t[:m.start()] + "".join(saida) + t[m.end():]


def slots(t, valores):
    for k, v in valores.items():
        t = t.replace("{{" + k + "}}", str(v))
    return t


def manter_tipo(t, tipo):
    """Apaga slides e itens marcados com data-so do outro tipo e remove o atributo dos que ficam."""
    outro = {"sol": "grau", "grau": "sol"}[tipo]
    t = re.sub(r'\n<!-- [^\n]*\(SÓ %s\)[^\n]*-->\n<section[^>]*data-so="%s".*?</section>\n' % (outro.upper(), outro), "\n", t, flags=re.S)
    t = re.sub(r'\s*<div data-so="%s">.*?</div></div>' % outro, "", t, flags=re.S)
    return t.replace(' data-so="%s"' % tipo, "")


def manter_modo(t, modo):
    """Provador: mantém a legenda do modo usado no provador.py (foto ou desenho) e apaga a outra."""
    outro = {"foto": "desenho", "desenho": "foto"}[modo]
    t = re.sub(r'\s*<p class="hint" data-modo="%s">.*?</p>' % outro, "", t, flags=re.S)
    return t.replace(' data-modo="%s"' % modo, "", 1)


def faltando(t):
    sem = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    return sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", sem)))
