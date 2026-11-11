#!/usr/bin/env python3
"""Portão de qualidade da skill visagismo-oculos. Sai com código 1 se houver item BLOQUEANTE.

Uso:
  python3 qa.py dados.json [--html apresentacao.html] [--online]

Confere dados.json (fonte única da verdade) e, opcionalmente, a apresentação e os links.
Formato do dados.json: references/dados.md.
"""
import argparse, datetime as dt, json, os, re, ssl, sys, urllib.parse, urllib.request, urllib.error

ERROS, AVISOS, OKS = [], [], []
CONF = {"ok", "warn", "unk"}
PAPEIS = {"curinga", "alternativa", "complemento", "referencia"}


def erro(m): ERROS.append(m)
def aviso(m): AVISOS.append(m)
def ok(m): OKS.append(m)


def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def dentro(v, faixa, tol=0):
    return v is not None and faixa and faixa[0] - tol <= v <= faixa[1] + tol


def alvo_do(prod, D):
    base = dict(D.get("alvo") or {})
    extra = (D.get("alvo_por_formato") or {}).get(prod.get("formato", ""), {})
    base.update(extra)
    return base


def checar_dados(D):
    c = D.get("cliente") or {}
    for k in ("nome", "data", "tipo", "entrada", "publico", "orcamento_max", "cidade", "estilo"):
        if c.get(k) in (None, "", []):
            erro(f"cliente.{k} vazio: a skill precisa perguntar isso antes de pesquisar.")
    tipo = c.get("tipo")
    if tipo not in ("sol", "grau"):
        erro("cliente.tipo deve ser 'sol' ou 'grau'.")
    if c.get("entrada") not in ("A", "B"):
        erro("cliente.entrada deve ser 'A' (sem óculos) ou 'B' (com a armação atual e medidas).")
    if c.get("entrada") == "B" and not D.get("armacao_atual"):
        erro("Entrada B sem armacao_atual (lente, ponte, haste).")
    if tipo == "grau" and c.get("orcamento_inclui_lentes") is None:
        erro("Grau: falta cliente.orcamento_inclui_lentes (o teto é só da armação ou armação + lentes?).")
    teto = c.get("orcamento_max") or 0
    try:
        hoje = dt.date.fromisoformat(c.get("data", ""))
    except ValueError:
        hoje = None
        erro("cliente.data deve ser AAAA-MM-DD.")

    alvo = D.get("alvo") or {}
    for k in ("lente", "ponte", "haste"):
        f = alvo.get(k)
        if not (isinstance(f, list) and len(f) == 2 and f[0] <= f[1]):
            erro(f"alvo.{k} deve ser [min, max].")

    rx = D.get("receita")
    if tipo == "grau" and not rx:
        aviso("Grau sem receita: espessura, índice e descentração ficam ❓. Diga isso no slide de lente.")
    max_esf, esf_sinal = 0, 0.0
    if rx:
        for olho in ("od", "oe"):
            e = (rx.get(olho) or {}).get("esf")
            if e is not None and abs(float(e)) > max_esf:
                max_esf, esf_sinal = abs(float(e)), float(e)
        cil = max(abs(float((rx.get(o) or {}).get("cil") or 0)) for o in ("od", "oe"))
    else:
        cil = 0

    prods = D.get("produtos") or []
    if not prods:
        erro("Nenhum produto em dados.produtos.")
    ids = set()
    papeis = [p.get("papel") for p in prods]
    if "curinga" not in papeis:
        erro("Falta um produto com papel 'curinga'.")
    for p in prods:
        nome = f"{p.get('marca','?')} {p.get('codigo','?')}"
        ids.add(p.get("id"))
        for k in ("id", "papel", "marca", "modelo", "codigo", "formato", "url", "publico", "lido_em"):
            if not p.get(k):
                erro(f"{nome}: campo '{k}' vazio.")
        if p.get("papel") not in PAPEIS:
            erro(f"{nome}: papel '{p.get('papel')}' inválido ({', '.join(sorted(PAPEIS))}).")
        for k in ("conf_preco", "conf_medidas"):
            if p.get(k) not in CONF:
                erro(f"{nome}: {k} precisa ser ok | warn | unk.")
        # público (lição: o Polaroid 'feminino')
        if p.get("publico") and c.get("publico") and p["publico"] not in (c["publico"], "unissex"):
            erro(f"{nome}: produto '{p['publico']}' para cliente '{c['publico']}'.")
        # medidas no alvo
        a = alvo_do(p, D)
        ponte_alvo = a.get("ponte")
        fora = []
        for k, tol in (("lente", 0), ("ponte", 0), ("haste", 0)):
            v = p.get(k)
            f = a.get(k) if k != "ponte" else ponte_alvo
            if v is None:
                fora.append(f"{k} desconhecida")
            elif not dentro(v, f, tol):
                fora.append(f"{k} {v} fora de {f[0]}–{f[1]}" if f else f"{k} sem alvo")
        if fora:
            if p.get("papel") == "referencia" or p.get("justificativa_fora_alvo"):
                aviso(f"{nome}: {', '.join(fora)} (justificado: {p.get('justificativa_fora_alvo') or 'referência'}).")
            else:
                erro(f"{nome}: {', '.join(fora)} e sem justificativa_fora_alvo.")
        if p.get("largura_total") and alvo.get("largura_total") and not dentro(p["largura_total"], alvo["largura_total"], 2):
            aviso(f"{nome}: largura total {p['largura_total']} fora de {alvo['largura_total']}.")
        # preço
        preco = p.get("preco")
        if p.get("papel") != "referencia":
            if not isinstance(preco, (int, float)):
                erro(f"{nome}: preço ausente.")
            elif teto and preco > teto:
                erro(f"{nome}: {brl(preco)} acima do teto de {brl(teto)}.")
        # data de leitura
        try:
            lido = dt.date.fromisoformat(p.get("lido_em", ""))
            if hoje and (hoje - lido).days > 7:
                aviso(f"{nome}: preço lido em {lido}, há mais de 7 dias. Releia antes de entregar.")
        except ValueError:
            erro(f"{nome}: lido_em deve ser AAAA-MM-DD.")
        if p.get("estoque") in (None, ""):
            aviso(f"{nome}: estoque não informado (use 'disponivel', 'esgotado' ou 'incerto').")
        # sol
        if tipo == "sol":
            if p.get("uv400") == "nao":
                erro(f"{nome}: sem proteção UV400.")
            elif p.get("uv400") != "ok":
                aviso(f"{nome}: UV400 não confirmado na página ({p.get('uv400')}). Mande conferir o selo na loja.")
            if p.get("papel") == "curinga" and "degrad" in (p.get("lente_tipo") or "").lower():
                aviso(f"{nome}: lente degradê no curinga protege menos no sol forte.")
        # grau
        if tipo == "grau" and rx:
            dp = (rx.get("dp") or (D.get("medidas") or {}).get("alvo", {}).get("dp_usada"))
            if dp and p.get("lente") and p.get("ponte"):
                dec = (p["lente"] + p["ponte"] - float(dp)) / 2
                efeito = "borda temporal grossa" if esf_sinal < 0 else "centro grosso e blank maior"
                msg = f"{nome}: descentração {dec:.1f} mm/olho com esférico {esf_sinal:+.2f}: {efeito}."
                if dec > 4 and max_esf >= 3:
                    (aviso if p.get("papel") == "referencia" else erro)(msg + " Prefira lente ou ponte menor (A + ponte perto da DP).")
                elif dec > 3 and max_esf >= 2:
                    aviso(msg + " Peça lente de índice maior.")
            if rx.get("adicao") and p.get("papel") != "referencia":
                h = p.get("altura")
                if h is None:
                    aviso(f"{nome}: multifocal sem altura da lente na página (precisa ≥ 30 mm). Marque ❓ e mande medir.")
                elif h < 30:
                    erro(f"{nome}: altura {h} mm < 30 mm para multifocal.")
            aro = (p.get("aro") or "").lower()
            if max_esf >= 4 and any(t in aro for t in ("sem aro", "parafus", "nylon", "fio")):
                erro(f"{nome}: armação '{aro}' com esférico {esf_sinal:+.2f}: a borda da lente fica exposta e grossa.")
            if cil >= 2 and (p.get("curvatura") or 0) >= 6:
                aviso(f"{nome}: cilíndrico {cil:.2f} em armação curva (base {p.get('curvatura')}): risco de distorção.")

    for cb in D.get("combos") or []:
        itens = cb.get("itens", [])
        faltam = [i for i in itens if i not in ids]
        if faltam:
            erro(f"Combo '{cb.get('nome')}': itens inexistentes {faltam}.")
            continue
        soma = round(sum(next(p["preco"] for p in prods if p["id"] == i) for i in itens), 2)
        if abs(soma - float(cb.get("total", -1))) > 0.005:
            erro(f"Combo '{cb.get('nome')}': total {cb.get('total')} ≠ soma {soma:.2f}.")
        else:
            ok(f"Combo '{cb.get('nome')}' soma {brl(soma)}.")

    for k, v in (D.get("diagnostico") or {}).items():
        if isinstance(v, dict) and "valor" in v and v.get("conf") not in CONF:
            erro(f"diagnostico.{k}: selo de confiança ausente (ok | warn | unk).")

    rev = D.get("revisao") or []
    if not rev:
        erro("Sem revisão registrada: a v0 não passou pela autocrítica.")
    fontes = {r.get("fonte") for r in rev}
    for f in ("autocritica", "critico"):
        if f not in fontes:
            erro(f"Revisão sem entrada de fonte '{f}'. Rode {'as 3 lentes' if f == 'autocritica' else 'o subagente crítico'} e registre (mesmo que 'sem objeções').")
    for r in rev:
        if r.get("severidade") == "bloqueante" and r.get("status") != "resolvida":
            erro(f"Objeção bloqueante em aberto: {r.get('objecao')}")
    return tipo, prods


def checar_html(caminho, tipo, prods):
    with open(caminho, encoding="utf-8") as fh:
        h = fh.read()
    tam = len(h.encode()) / 1e6
    if tam > 15:
        erro(f"HTML com {tam:.1f} MB: acima do limite de publicação. Reduza lado_max/qualidade das fotos.")
    elif tam > 6:
        aviso(f"HTML com {tam:.1f} MB: pesado no celular. Reduza as fotos.")
    sem_coment = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    resto = re.findall(r"\{\{[A-Z0-9_ *]+\}\}", sem_coment)
    if resto:
        erro(f"Slots não preenchidos: {sorted(set(resto))[:12]}")
    outro = {"sol": "grau", "grau": "sol"}.get(tipo)
    if outro and re.search(rf'data-so="{outro}"', sem_coment):
        erro(f"Sobrou bloco data-so=\"{outro}\" numa apresentação de {tipo}.")
    if len(re.findall(r'id="lente"', sem_coment)) > 1:
        erro("Há dois slides id=\"lente\" (sol e grau): apague o que não é do tipo.")
    for sid in ("capa", "rosto", "revisei", "fracos", "checklist", "decisao"):
        if f'id="{sid}"' not in sem_coment:
            erro(f"Slide obrigatório ausente: #{sid}.")
    t = re.search(r"<title>(.*?)</title>", h[:8192], re.S)
    if not t or not t.group(1).strip():
        erro("Sem <title> nos primeiros 8 KB.")
    elif len(t.group(1).split()) > 6:
        aviso(f"Título longo demais para um nome: '{t.group(1).strip()}'.")
    for m in re.finditer(r'<(?:img|image|source)\b[^>]*?\b(?:src|href)="([^"]+)"', sem_coment):
        if not m.group(1).startswith("data:"):
            erro(f"Imagem não embutida (bloqueada no artifact ou caminho local): {m.group(1)[:80]}")
    for m in re.finditer(r'<script\b[^>]*\bsrc="([^"]+)"', sem_coment):
        if not re.match(r"https://(cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net/npm/|unpkg\.com|cdn\.tailwindcss\.com|code\.jquery\.com)", m.group(1)):
            erro(f"Script de host não permitido: {m.group(1)}")
    if re.search(r"\bv0\b|rascunho", re.sub(r"<[^>]+>", " ", sem_coment), re.I):
        aviso("O texto menciona 'v0' ou 'rascunho'. A primeira versão não deve aparecer para o cliente.")
    for p in prods:
        nome = f"{p.get('marca')} {p.get('codigo')}"
        if p.get("codigo") and p["codigo"] not in h:
            erro(f"{nome}: código não aparece na apresentação.")
        if isinstance(p.get("preco"), (int, float)) and p.get("papel") != "referencia":
            if brl(p["preco"]) not in h.replace(" ", " "):
                erro(f"{nome}: preço {brl(p['preco'])} do dados.json não aparece igual na apresentação.")
        if p.get("url") and p["url"] not in h:
            erro(f"{nome}: link do dados.json não está na apresentação.")
        # o slide do produto não pode prometer o que os dados não dizem (ex.: "polarizado" num degradê)
        sec = re.search(r'<section[^>]*id="%s".*?</section>' % re.escape(p.get("id", "")), sem_coment, re.S)
        if sec:
            negacao = r"(não diz|nao diz|sem|não é|nao e|não declara|nao declara)\s+(a\s+)?polariz\w*(\s+declarada)?"
            texto = re.sub(negacao, " ", re.sub(r"<[^>]+>", " ", sec.group(0)).lower())
            lt = re.sub(negacao, " ", (p.get("lente_tipo") or "").lower())
            if "polariz" in texto and "polariz" not in lt:
                erro(f"{nome}: o slide diz 'polarizado', mas lente_tipo é '{p.get('lente_tipo')}'.")
            if "uv400" in texto and p.get("uv400") != "ok":
                erro(f"{nome}: o slide diz 'UV400', mas uv400 = '{p.get('uv400')}'.")
    ok(f"HTML conferido ({tam:.2f} MB).")


def contexto_ssl():
    ctx = ssl.create_default_context()
    for f in (os.environ.get("SSL_CERT_FILE"), os.environ.get("REQUESTS_CA_BUNDLE"), "/root/.ccr/ca-bundle.crt"):
        if f and os.path.exists(f):
            try:
                ctx.load_verify_locations(f)
            except Exception:
                pass
    return ctx


def checar_links(prods):
    ctx = contexto_ssl()
    for p in prods:
        url, cod = p.get("url"), (p.get("codigo") or "")
        if not url:
            continue
        nome = f"{p.get('marca')} {cod}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
                                                   "Accept-Language": "pt-BR,pt;q=0.9"})
        try:
            with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
                final, corpo = r.geturl(), r.read(3_000_000).decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                erro(f"{nome}: link quebrado (HTTP {e.code}).")
            else:
                aviso(f"{nome}: HTTP {e.code} (o site pode bloquear robôs). Confira com WebFetch.")
            continue
        except Exception as e:
            aviso(f"{nome}: não consegui abrir ({type(e).__name__}). Confira com WebFetch.")
            continue
        norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
        caminho = urllib.parse.urlparse(final).path.strip("/")
        if (not caminho or re.search(r"notfound|nao-?encontrad|/404|erro", final, re.I)
                or re.search(r"[?&](q|busca|search|ft)=", final)):
            erro(f"{nome}: o link não abre o produto (redireciona para home, busca ou 'não encontrado': {final}).")
        elif cod and norm(cod) not in norm(corpo) and norm(cod) not in norm(final):
            aviso(f"{nome}: o código não aparece no HTML da página (pode ser renderizado por JS). Confira com WebFetch.")
        else:
            ok(f"{nome}: link abre o produto.")
        if re.search(r"esgotad|indispon[ií]vel|out of stock", corpo, re.I):
            aviso(f"{nome}: a página contém 'esgotado/indisponível'. Pode ser texto fixo; mande checar estoque pelo CEP ou na loja.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dados")
    ap.add_argument("--html", default="")
    ap.add_argument("--online", action="store_true")
    a = ap.parse_args()
    with open(a.dados, encoding="utf-8") as fh:
        D = json.load(fh)
    tipo, prods = checar_dados(D)
    if a.html:
        checar_html(a.html, tipo, prods)
    if a.online:
        checar_links(prods)
    for m in OKS:
        print(f"✓ {m}")
    for m in AVISOS:
        print(f"⚠ {m}")
    for m in ERROS:
        print(f"✗ BLOQUEANTE: {m}")
    print(f"\n{len(ERROS)} bloqueante(s) · {len(AVISOS)} aviso(s) · {len(OKS)} ok")
    sys.exit(1 if ERROS else 0)


if __name__ == "__main__":
    main()
