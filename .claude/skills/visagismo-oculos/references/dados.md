# dados.json: a fonte única da verdade

Tudo que aparece na apresentação sai daqui. O `qa.py` confere este arquivo e compara com o HTML. Exemplo completo (caso real de sol, entrada B): `assets/exemplo-dados.json`.

Selos (`conf`): `ok` = ✅ lido na página, informado pelo cliente ou medido na armação · `warn` = ⚠️ estimativa (toda medida de foto) · `unk` = ❓ não achei.

```jsonc
{
  "cliente": {
    "nome": "Ana",                      // como ela quer ser chamada na capa
    "data": "2026-11-11",
    "tipo": "sol",                      // sol | grau
    "entrada": "A",                     // A = sem óculos · B = com a armação atual e medidas
    "publico": "feminino",              // masculino | feminino | unissex (o que o cliente quer usar)
    "orcamento_max": 400,               // por armação, em R$
    "orcamento_inclui_lentes": null,    // só grau: true | false (obrigatório no grau)
    "cidade": "Belo Horizonte",
    "estilo": "clássico, discreto",
    "ocasioes": ["trabalho", "praia"],
    "quantidade": "1 curinga ou 2 complementares",
    "observacoes": "barba cheia; cabelo muda pouco"
  },
  "receita": null,                      // grau: {"od":{"esf":-2.5,"cil":-0.75,"eixo":180},"oe":{...},"adicao":null,"dp":63,"fonte":"receita de 03/2026"}
  "armacao_atual": null,                // entrada B: {"lente":51,"ponte":21,"haste":140,"ponte_ok":true,"formato":"panto","material":"acetato","cor":"preto fosco","leitura":"estreita; ponte apoia bem; haste curta"}
  "medidas": { },                       // cole a saída inteira do medir.py
  "alvo": {"lente":[54,56], "ponte":[19,21], "haste":[145,150], "largura_total":[137,141]},
  "alvo_por_formato": {"aviador": {"lente":[58,62], "ponte":[14,18], "haste":[140,150]}},
  "diagnostico": {
    "formato_rosto": {"valor":"retangular/oblongo, mandíbula marcada", "conf":"warn"},
    "largura":       {"valor":"larga nas têmporas e maçãs", "conf":"warn"},
    "nariz":         {"valor":"ponte baixa a média", "conf":"warn"},
    "pele":          {"valor":"subtom quente, contraste alto", "conf":"warn"},
    "regras":  ["lente com boa altura", "cantos suaves", "barra de cima na linha da sobrancelha"],
    "evitar":  ["retângulo baixo e estreito", "ponte 16–17 em acetato"],
    "cores":   {"sim":["havana sólido","preto","dourado escuro"], "evitar":["prata fria"]},
    "estrategia": "1 curinga quadrado suave marrom + aviador dourado como complemento"
  },
  "produtos": [
    {
      "id": "curinga-1", "papel": "curinga",          // curinga | alternativa | complemento | referencia
      "marca": "Chilli Beans", "modelo": "Quadrado Polarizado Marrom", "codigo": "OC.CL.5317.0202",
      "formato": "softsq",                           // chave da biblioteca do template; liga com alvo_por_formato
      "url": "https://…/p",
      "lente": 56, "ponte": 20, "haste": 145, "altura": null, "largura_total": null,
      "material": "policarbonato", "aro": "fechado", "curvatura": null,
      "cor": "marrom sólido", "lente_tipo": "polarizada marrom", "uv400": "ok",   // uv400: ok | unk | nao
      "preco": 199.99, "parcelado": "4x R$ 54,99",
      "conf_preco": "ok", "conf_medidas": "ok", "lido_em": "2026-11-11",
      "publico": "masculino", "estoque": "incerto",  // disponivel | esgotado | incerto
      "justificativa_fora_alvo": null,
      "porque": "as três medidas no alvo; marrom sólido", "perde": "policarbonato tem acabamento menos nobre",
      "cor_css": "#5b3922",       // opcional: cor do aro no provador (ou "url(#p-tartaruga)"); sem ele, sai de "cor"
      "nome_curto": null,         // opcional: nome no cartão do provador (padrão: forma + número do código)
      "rotulo": null              // opcional: papel no cartão (ex.: "Plano B", "O que você quis provar")
    }
  ],
  "combos": [{"nome":"curinga + aviador", "itens":["curinga-1","complemento"], "total":499.97}],
  "descartados": [{"modelo":"CB 4016.0202", "motivo":"ponte 17: escorrega"}],
  "revisao": [
    {"rodada":1, "fonte":"autocritica", "severidade":"importante", "objecao":"…", "decisao":"…", "status":"resolvida"},
    {"rodada":1, "fonte":"critico", "severidade":"cosmetico", "objecao":"…", "decisao":"…", "status":"resolvida"},
    {"rodada":2, "fonte":"cliente", "severidade":"importante", "objecao":"'muito feminino'", "decisao":"saiu", "status":"resolvida"}   // reação do cliente, nas palavras dele
  ]
}
```

Notas:
- `alvo.ponte` é a faixa para acetato. Para metal com plaquetas, use `alvo_por_formato` (ex.: aviador 14–18).
- Produto `referencia` pode passar do teto e do alvo; o `qa.py` só avisa.
- `revisao` precisa de pelo menos uma entrada `autocritica` e uma `critico`. Uma bloqueante com `status` diferente de `resolvida` impede a entrega.
