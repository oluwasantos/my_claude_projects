---
name: nome-sessao
description: Gera o nome da sessão no formato projeto_yyyymmdd_titulo (tudo minúsculo, separado por "_") para o usuário colar em /rename antes de dar /clear. Use quando o usuário pedir nome de sessão, ou ao encerrar/limpar uma sessão.
argument-hint: "[dica opcional de título]"
disable-model-invocation: true
---

# Nome de sessão

Gera **um nome de sessão** para o usuário usar com `/rename` e depois `/clear`.

## Formato

```
projeto_yyyymmdd_titulo
```

- **tudo minúsculo**, partes separadas por `_`
- só letras `a-z`, números e `_` (sem acentos, `ç` vira `c`, sem espaços, hífens ou pontuação)

## Como montar cada parte

1. **projeto**: o projeto em que a sessão trabalhou.
   - Se a sessão foi sobre uma pasta/projeto específico (ex.: o "Projeto ativo" do `CLAUDE.md`, ou a subpasta onde os arquivos foram editados), use o nome dessa pasta.
   - Senão, use o nome do repositório (último trecho do caminho da raiz do repositório git).
2. **yyyymmdd**: a data de hoje, obtida com o comando `date +%Y%m%d`. Nunca adivinhar a data.
3. **titulo**: 2 a 5 palavras que resumem o que **foi feito ou decidido** na sessão (não o assunto do primeiro pedido). Substantivos e verbos curtos, sem artigos e preposições desnecessárias. Se o usuário passou um argumento (`$ARGUMENTS`), use-o como ponto de partida do título.

## Normalizar

Passe o texto montado (as três partes separadas por espaço) por este comando para garantir minúsculas, sem acentos e com `_`:

```bash
python3 -c "import sys,re,unicodedata as u;t=u.normalize('NFKD',' '.join(sys.argv[1:])).encode('ascii','ignore').decode().lower();print(re.sub(r'[^a-z0-9]+','_',t).strip('_'))" "viagem-1-ano-namoro 20261106 Fecha financeiro e passagens"
```

## Saída

Responda em pt-BR, curto: o nome principal em bloco de código, 2 variações só do título, e os comandos prontos para colar.

````
viagem_1_ano_namoro_20261106_fecha_financeiro_e_passagens
````

Alternativas de título: `acerto_pix_e_cancelamento`, `financeiro_fechado`

Depois, rode você mesmo:

```
/rename viagem_1_ano_namoro_20261106_fecha_financeiro_e_passagens
/clear
```

## Regras

- Não execute `/rename` nem `/clear`: são comandos do usuário. Só entregue o nome e os comandos.
- Não altere arquivos nem faça commit.
- Se faltar contexto para o título (sessão vazia), pergunte em uma linha o que resumir.
