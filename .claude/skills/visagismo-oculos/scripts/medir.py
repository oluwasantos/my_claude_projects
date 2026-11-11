#!/usr/bin/env python3
"""Converte pontos marcados nas fotos (px) em medidas do rosto (mm) e faixas-alvo de armação.

Uso:
  python3 medir.py pontos.json [--saida medidas.json]

Toda medida tirada de foto sai com conf "warn" (⚠️ estimativa). Medidas digitadas pelo usuário
(armação atual) são "ok". Fórmulas e limites em references/medidas.md.

pontos.json (todas as vistas são opcionais, menos "frente"):
{
  "tipo": "sol" | "grau",
  "frente": {"pontos": {
      "pupila_d": [x,y], "pupila_e": [x,y],
      "iris_d": [[x,y],[x,y]], "iris_e": [[x,y],[x,y]],     # bordas horizontais da íris (limbo)
      "temporas": [[x,y],[x,y]], "zigomas": [[x,y],[x,y]], "mandibula": [[x,y],[x,y]],
      "linha_cabelo": [x,y], "queixo": [x,y],
      "ponte_nasal": [[x,y],[x,y]],                         # largura do nariz onde a ponte apoia
      "sobrancelha": [x,y], "bochecha": [x,y]               # na vertical da pupila: borda de baixo da sobrancelha / topo da maçã
  }},
  "perfil": {"pontos": {"pupila": [x,y], "queixo": [x,y], "cornea": [x,y], "orelha": [x,y]}},
  "com_oculos_frente": {"pontos": {
      "lente_d": [[x,y],[x,y]], "lente_e": [[x,y],[x,y]],   # bordas interna e externa visíveis de cada lente
      "pupila_d": [x,y], "pupila_e": [x,y],
      "aro_total": [[x,y],[x,y]], "temporas": [[x,y],[x,y]]
  }},
  "armacao_atual": {"lente": 51, "ponte": 21, "haste": 140},
  "receita": {"dp": 64}                                     # opcional; DP medida pela ótica vence a da foto
}
"""
import argparse, json, math, sys

IRIS_MM = 11.7       # diâmetro horizontal visível da íris (HVID) médio de adultos, ±0,5 mm
BLOCO_MM = 12.0      # largura total ≈ 2×lente + ponte + ~12 mm de blocos laterais (varia 8–16)
VERTEX_MM = 12.0     # distância córnea → plano da lente
QUEDA_MM = 35.0      # trecho da haste que desce atrás da orelha


def d(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def media(v):
    v = [x for x in v if x is not None]
    return sum(v) / len(v) if v else None


def r5_baixo(x):
    return int(5 * math.floor(x / 5))


def faixa(c, meia):
    return [int(round(c - meia)), int(round(c + meia))]


def eixo_rosto(pts):
    """Vetor unitário da linha dos olhos (horizontal do rosto) e o perpendicular (vertical do rosto)."""
    a, b = pts.get("pupila_d"), pts.get("pupila_e")
    if not (a and b):
        return (1.0, 0.0), (0.0, 1.0), 0.0
    if a[0] > b[0]:
        a, b = b, a
    L = d(a, b)
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    return (ux, uy), (-uy, ux), math.degrees(math.atan2(uy, ux))


def proj(p, q, u):
    return abs((q[0] - p[0]) * u[0] + (q[1] - p[1]) * u[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pontos")
    ap.add_argument("--saida", default="")
    a = ap.parse_args()
    with open(a.pontos, encoding="utf-8") as fh:
        J = json.load(fh)

    tipo = J.get("tipo", "sol")
    F = J.get("frente", {}).get("pontos", {})
    P = J.get("perfil", {}).get("pontos", {})
    B = J.get("com_oculos_frente", {}).get("pontos", {})
    atual = J.get("armacao_atual") or {}
    rx = J.get("receita") or {}
    alertas, escala, M = [], {}, {}

    def put(nome, mm, fonte, conf="warn"):
        if mm is not None:
            M[nome] = {"mm": round(mm, 1), "conf": conf, "fonte": fonte}

    if not F:
        sys.exit("ERRO: faltam os pontos da foto de frente.")
    u, v, ang = eixo_rosto(F)
    if abs(ang) > 4:
        alertas.append(f"Cabeça inclinada {ang:.1f}° na foto de frente: as medidas foram projetadas no eixo do rosto, mas confira.")

    # 1) escala da foto COM óculos (armação conhecida)
    s_B, dp_mm = None, None
    if B and atual.get("lente") and atual.get("ponte"):
        A, DBL = float(atual["lente"]), float(atual["ponte"])
        ests = []
        for lado in ("lente_d", "lente_e"):
            if B.get(lado):
                ests.append(A / d(*B[lado]))
        if B.get("lente_d") and B.get("lente_e"):
            cd = [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2) for p, q in (B["lente_d"], B["lente_e"])]
            ests.append((A + DBL) / d(cd[0], cd[1]))
        if ests:
            s_B = media(ests)
            disp = (max(ests) - min(ests)) / s_B * 100
            escala["com_oculos_mm_por_px"] = round(s_B, 5)
            escala["com_oculos_dispersao_pct"] = round(disp, 1)
            if disp > 6:
                alertas.append(f"As estimativas de escala pela armação discordam {disp:.0f}%: rosto girado ou bordas mal marcadas. Remarque as lentes.")
            if B.get("pupila_d") and B.get("pupila_e"):
                dp_mm = d(B["pupila_d"], B["pupila_e"]) * s_B
                put("dp_foto", dp_mm, "pupilas na foto com óculos × escala da armação")
            if B.get("aro_total"):
                put("armacao_atual_largura_total", d(*B["aro_total"]) * s_B, "aro na foto com óculos")
            if B.get("temporas"):
                put("temporas_foto_com_oculos", d(*B["temporas"]) * s_B, "têmporas na foto com óculos")

    # 2) escala da foto de frente: DP transferida (se houver) e íris (sempre que marcada)
    s_iris = None
    iris = [d(*F[k]) for k in ("iris_d", "iris_e") if F.get(k)]
    if iris:
        s_iris = IRIS_MM / media(iris)
        escala["frente_mm_por_px_iris"] = round(s_iris, 5)
    s_dp = None
    dp_ref = rx.get("dp") or dp_mm
    if dp_ref and F.get("pupila_d") and F.get("pupila_e"):
        s_dp = float(dp_ref) / d(F["pupila_d"], F["pupila_e"])
        escala["frente_mm_por_px_dp"] = round(s_dp, 5)
    s_F = s_dp or s_iris
    if s_dp and s_iris:
        dif = abs(s_dp - s_iris) / s_dp * 100
        escala["frente_divergencia_dp_iris_pct"] = round(dif, 1)
        if dif > 8:
            alertas.append(f"Escala pela DP e pela íris divergem {dif:.0f}%. Usei a DP; confira a marcação da íris ou peça foto mais próxima e nítida.")
    escala["frente_fonte"] = "DP (receita)" if rx.get("dp") else ("DP da foto com óculos" if s_dp else ("íris 11,7 mm" if s_iris else "nenhuma"))
    if not s_F:
        alertas.append("Sem escala (nem íris nem armação conhecida): só proporções, sem mm. Peça a foto com os olhos nítidos ou a armação atual com medidas.")

    # 3) medidas de frente
    def larg(chave):
        return proj(*F[chave], u) * s_F if (s_F and F.get(chave)) else None

    put("largura_temporas", larg("temporas"), "frente")
    put("largura_zigomas", larg("zigomas"), "frente")
    put("largura_mandibula", larg("mandibula"), "frente")
    put("ponte_nasal", larg("ponte_nasal"), "frente")
    if s_F and F.get("linha_cabelo") and F.get("queixo"):
        put("comprimento_rosto", proj(F["linha_cabelo"], F["queixo"], v) * s_F, "frente (linha do cabelo → queixo)")
    if s_F and F.get("pupila_d") and F.get("pupila_e") and "dp_foto" not in M:
        put("dp_foto", d(F["pupila_d"], F["pupila_e"]) * s_F, "pupilas × escala da íris")
    if s_F and F.get("sobrancelha") and F.get("bochecha"):
        put("altura_livre_lente", proj(F["sobrancelha"], F["bochecha"], v) * s_F, "sobrancelha → topo da maçã, na vertical da pupila")

    # 4) proporções e pistas de formato (só pistas: a classificação final é visual)
    prop, pistas = {}, []
    zig = M.get("largura_zigomas", {}).get("mm")
    tem = M.get("largura_temporas", {}).get("mm")
    mand = M.get("largura_mandibula", {}).get("mm")
    comp = M.get("comprimento_rosto", {}).get("mm")
    if not s_F and F.get("zigomas"):  # proporções funcionam sem escala
        zp = proj(*F["zigomas"], u)
        if F.get("linha_cabelo") and F.get("queixo"):
            prop["comprimento/zigomas"] = round(proj(F["linha_cabelo"], F["queixo"], v) / zp, 2)
        if F.get("mandibula"):
            prop["mandibula/zigomas"] = round(proj(*F["mandibula"], u) / zp, 2)
        if F.get("temporas"):
            prop["temporas/zigomas"] = round(proj(*F["temporas"], u) / zp, 2)
    else:
        if zig and comp: prop["comprimento/zigomas"] = round(comp / zig, 2)
        if zig and mand: prop["mandibula/zigomas"] = round(mand / zig, 2)
        if zig and tem: prop["temporas/zigomas"] = round(tem / zig, 2)
    cz, mz, tz = prop.get("comprimento/zigomas"), prop.get("mandibula/zigomas"), prop.get("temporas/zigomas")
    if cz:
        pistas.append("rosto longo (comprimento ≥ 1,45× a largura)" if cz >= 1.45 else
                      ("rosto curto/largo (comprimento < 1,25× a largura)" if cz < 1.25 else "comprimento médio"))
    if mz:
        pistas.append("mandíbula larga (≥ 0,90 das maçãs): quadrado ou retangular" if mz >= 0.9 else
                      ("mandíbula afinada (< 0,78 das maçãs): oval, coração ou diamante" if mz < 0.78 else "mandíbula intermediária"))
    if tz:
        pistas.append("testa estreita (< 0,85 das maçãs): diamante ou triângulo" if tz < 0.85 else
                      ("testa larga (≥ 0,97 das maçãs): coração ou quadrado" if tz >= 0.97 else "testa proporcional"))

    # 5) haste pelo perfil (escala transferida pela distância vertical pupila → queixo)
    if s_F and P.get("pupila") and P.get("queixo") and F.get("pupila_d") and F.get("queixo"):
        pup_med = ((F["pupila_d"][0] + F["pupila_e"][0]) / 2, (F["pupila_d"][1] + F["pupila_e"][1]) / 2) if F.get("pupila_e") else F["pupila_d"]
        vert_mm = proj(pup_med, F["queixo"], v) * s_F
        s_P = vert_mm / abs(P["queixo"][1] - P["pupila"][1])
        escala["perfil_mm_por_px"] = round(s_P, 5)
        if P.get("cornea") and P.get("orelha"):
            ce = abs(P["orelha"][0] - P["cornea"][0]) * s_P
            put("cornea_orelha", ce, "perfil (horizontal córnea → raiz da orelha)")

    # 6) alvos
    alvo, nota = {}, []
    W = tem or (zig * 0.97 if zig else None)
    n = M.get("ponte_nasal", {}).get("mm")
    dbl = [max(14, int(round(n))), min(24, int(round(n)) + 2)] if n else None
    if W:
        largura = {"grau": [W - 2, W + 2], "sol": [W, W + 4]}[tipo]
        alvo["largura_total"] = [int(round(x)) for x in largura]
        dbl_mid = (dbl[0] + dbl[1]) / 2 if dbl else 19
        A = ((sum(largura) / 2) - dbl_mid - BLOCO_MM) / 2
        alvo["lente"] = faixa(A, 1)
        if tipo == "sol":
            alvo["lente_aviador"] = [alvo["lente"][0] + 4, alvo["lente"][1] + 6]
    if dbl:
        alvo["ponte_acetato"] = dbl
        nota.append("Ponte: em acetato a medida precisa casar com o nariz; com plaquetas ajustáveis (metal) importa menos.")
    ce = M.get("cornea_orelha", {}).get("mm")
    if ce:
        h = ce + VERTEX_MM + QUEDA_MM
        alvo["haste"] = [r5_baixo(h), r5_baixo(h) + 5]
    altura = M.get("altura_livre_lente", {}).get("mm")
    if altura:
        alvo["altura_lente_max"] = int(math.floor(altura - 2))
    dp_final = float(rx["dp"]) if rx.get("dp") else (M.get("dp_foto", {}).get("mm"))
    if dp_final:
        alvo["dp_usada"] = round(dp_final, 1)
        alvo["dp_fonte"] = "receita/ótica" if rx.get("dp") else "foto (⚠️ confirmar na ótica)"

    # 7) leitura da armação atual
    leitura = {}
    if atual.get("lente") and atual.get("ponte"):
        tot = 2 * atual["lente"] + atual["ponte"] + BLOCO_MM
        leitura["largura_total_estimada"] = round(M.get("armacao_atual_largura_total", {}).get("mm", tot), 1)
        if W:
            dif = leitura["largura_total_estimada"] - W
            leitura["vs_rosto_mm"] = round(dif, 1)
            leitura["leitura"] = ("estreita para o rosto" if dif < -3 else ("larga para o rosto" if dif > 4 else "na largura do rosto"))
        if dp_final:
            dec = (atual["lente"] + atual["ponte"] - dp_final) / 2
            leitura["descentracao_por_olho_mm"] = round(dec, 1)
        if atual.get("haste") and alvo.get("haste"):
            leitura["haste_vs_alvo"] = atual["haste"] - alvo["haste"][0]

    res = {"tipo": tipo, "escala": escala, "medidas": M, "proporcoes": prop, "pistas_formato": pistas,
           "alvo": alvo, "armacao_atual": leitura, "notas": nota, "alertas": alertas,
           "aviso": "Medidas de foto são estimativas (⚠️). Margem típica: ±5% com íris, ±3% com armação conhecida."}
    txt = json.dumps(res, ensure_ascii=False, indent=2)
    if a.saida:
        with open(a.saida, "w", encoding="utf-8") as fh:
            fh.write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
