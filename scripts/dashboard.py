#!/usr/bin/env python3
"""Gera o dashboard HTML da validacao a partir de um JSON.

Uso:
    python3 dashboard.py --input resultado.json --output validacao.html

O JSON aceita (todos os campos sao opcionais menos 'notas'):

{
  "ideia": "Link de dieta para pacientes",
  "frase": "O paciente usa um link para ver a dieta do dia...",
  "notas": {"dor":8,"recorrencia":9,"pagador":7,"simplicidade":9,"canal":10,"substituicao":8},
  "justificativas": {"dor": "Pacientes perdem o PDF toda semana"},
  "filtros": [{"nome":"Problema unico","passa":true,"nota":"..."}],
  "score": 85,
  "veredito": "CONSTROI COM CORTE",
  "motivo": "...",
  "risco": "O maior risco e ...",
  "armadilha": "Sindrome do 'e tambem'",
  "telas": [{"nome":"Dieta do dia","acao":"Ver e marcar como feito"}],
  "nao_faz": ["Login com senha", "App nativo"],
  "cobranca": {"rota":"A","preco":"R$ 350/mes","frase":"..."},
  "teste_7_dias": ["Dia 1-2: falar com 5 pacientes", "..."],
  "primeiro_passo": "Mandar mensagem para 5 pacientes hoje",
  "pesquisa": ["Concorrentes: X, Y", "Preco praticado: R$ 49 a R$ 199"]
}
"""

import argparse
import html
import json
import sys
from datetime import date

ROTULOS = {
    "dor": "Dor",
    "recorrencia": "Recorrência",
    "pagador": "Pagador",
    "simplicidade": "Simplicidade",
    "canal": "Canal",
    "substituicao": "Substituição",
}
ORDEM = ["dor", "recorrencia", "pagador", "simplicidade", "canal", "substituicao"]

CORES = {
    "CONSTROI": ("#0f7b3f", "#e6f4ec", "Construa"),
    "CONSTRÓI": ("#0f7b3f", "#e6f4ec", "Construa"),
    "CONSTROI COM CORTE": ("#8a6100", "#fdf3dc", "Construa, mas corte"),
    "CONSTRÓI COM CORTE": ("#8a6100", "#fdf3dc", "Construa, mas corte"),
    "REFORMULA": ("#9a4a00", "#fdece0", "Reformule o recorte"),
    "DESCARTA": ("#98221f", "#fbe9e8", "Não vale como produto"),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
background:#f4f5f7;color:#1c1e21;line-height:1.55;padding:32px 16px}
.wrap{max-width:820px;margin:0 auto}
.card{background:#fff;border-radius:14px;padding:26px 28px;margin-bottom:18px;
border:1px solid #e4e6eb}
h1{font-size:26px;line-height:1.25;margin-bottom:6px}
h2{font-size:15px;text-transform:uppercase;letter-spacing:.07em;color:#65676b;margin-bottom:16px}
h3{font-size:16px;margin:18px 0 8px}
.sub{color:#65676b;font-size:15px}
.frase{background:#f0f2f5;border-left:4px solid #b0b3b8;padding:14px 16px;
border-radius:0 8px 8px 0;margin-top:16px;font-size:16px}
.verdict{display:flex;align-items:center;gap:24px;flex-wrap:wrap}
.donut{width:118px;height:118px;border-radius:50%;display:grid;place-items:center;flex:0 0 auto}
.donut-in{width:88px;height:88px;background:#fff;border-radius:50%;display:grid;place-items:center}
.donut-in b{font-size:30px;line-height:1}
.donut-in span{font-size:11px;color:#65676b}
.badge{display:inline-block;padding:7px 15px;border-radius:999px;font-weight:700;font-size:15px}
.vtext{flex:1;min-width:240px}
.vtext p{margin-top:8px;color:#3a3b3c}
.eixo{display:flex;align-items:center;gap:12px;margin-bottom:11px;flex-wrap:wrap}
.eixo .nome{width:120px;font-weight:600;font-size:14px;flex:0 0 auto}
.bar{flex:1;min-width:130px;height:9px;background:#e4e6eb;border-radius:99px;overflow:hidden}
.bar i{display:block;height:100%;border-radius:99px}
.eixo .n{width:42px;text-align:right;font-variant-numeric:tabular-nums;
font-size:13px;color:#65676b;flex:0 0 auto}
.just{width:100%;padding-left:132px;font-size:13px;color:#65676b;margin-top:-6px}
ul{list-style:none}
li{padding:7px 0 7px 26px;position:relative;border-bottom:1px solid #f0f2f5}
li:last-child{border-bottom:0}
li.ok:before{content:'\\2713';position:absolute;left:2px;color:#0f7b3f;font-weight:700}
li.no:before{content:'\\2715';position:absolute;left:2px;color:#98221f;font-weight:700}
li.dot:before{content:'\\2022';position:absolute;left:6px;color:#8a8d91}
li.cut{color:#65676b;text-decoration:line-through;text-decoration-color:#c9ccd1}
li.cut:before{content:'\\2715';position:absolute;left:2px;color:#c0c3c7;text-decoration:none}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
.tela{background:#f7f8fa;border:1px solid #e4e6eb;border-radius:10px;padding:14px}
.tela .num{font-size:11px;color:#8a8d91;font-weight:700;letter-spacing:.08em}
.tela .tn{font-weight:700;margin:3px 0 5px}
.tela .ta{font-size:13px;color:#65676b}
.warn{background:#fdf3dc;border:1px solid #f0dcae;border-radius:10px;padding:14px 16px}
.step{background:#0f7b3f;color:#fff;border-radius:14px;padding:24px 28px}
.step h2{color:#bfe3cd}
.step .big{font-size:19px;font-weight:600;margin-top:4px}
.foot{text-align:center;color:#8a8d91;font-size:12px;padding:8px 0 24px}
table{width:100%;border-collapse:collapse;font-size:14px}
td{padding:9px 0;border-bottom:1px solid #f0f2f5;vertical-align:top}
td:first-child{width:88px;font-weight:700;color:#65676b;white-space:nowrap}
tr:last-child td{border-bottom:0}
@media(max-width:560px){.eixo .nome{width:100px}.just{padding-left:0}body{padding:16px 10px}
.card{padding:20px 18px}}
"""


def e(s):
    return html.escape(str(s)) if s is not None else ""


def cor_nota(n):
    if n >= 8:
        return "#0f7b3f"
    if n >= 6:
        return "#c99700"
    if n >= 4:
        return "#d97706"
    return "#98221f"


def build(d):
    notas = d.get("notas", {})
    just = d.get("justificativas", {})
    score = d.get("score")
    if score is None:
        vals = [notas.get(k, 0) for k in ORDEM]
        score = round(sum(vals) / 60 * 100) if vals else 0

    veredito = d.get("veredito", "REFORMULA")
    cor, fundo, legenda = CORES.get(veredito.upper(), ("#65676b", "#f0f2f5", ""))

    p = []
    a = p.append

    a("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'>")
    a("<meta name='viewport' content='width=device-width,initial-scale=1'>")
    a("<title>Validação · " + e(d.get("ideia", "micro-aplicação")) + "</title>")
    a("<style>" + CSS + "</style></head><body><div class='wrap'>")

    # Cabecalho
    a("<div class='card'>")
    a("<div class='sub'>Validação de micro-aplicação · " + e(d.get("data", date.today().strftime("%d/%m/%Y"))) + "</div>")
    a("<h1>" + e(d.get("ideia", "Sua ideia")) + "</h1>")
    if d.get("frase"):
        a("<div class='frase'>" + e(d["frase"]) + "</div>")
    a("</div>")

    # Veredito
    a("<div class='card'><div class='verdict'>")
    ang = int(score * 3.6)
    a("<div class='donut' style=\"background:conic-gradient(" + cor + " " + str(ang) +
      "deg,#e4e6eb 0deg)\"><div class='donut-in'><b>" + str(score) + "</b><span>de 100</span></div></div>")
    a("<div class='vtext'>")
    a("<div class='badge' style='background:" + fundo + ";color:" + cor + "'>" + e(veredito) + "</div>")
    if legenda:
        a("<p><strong>" + e(legenda) + "</strong></p>")
    if d.get("motivo"):
        a("<p>" + e(d["motivo"]) + "</p>")
    a("</div></div></div>")

    # Filtros
    filtros = d.get("filtros") or []
    if filtros:
        a("<div class='card'><h2>Filtros de corte</h2><ul>")
        for f in filtros:
            cls = "ok" if f.get("passa") else "no"
            nota = f.get("nota") or ""
            extra = " <span class='sub'>— " + e(nota) + "</span>" if nota else ""
            a("<li class='" + cls + "'>" + e(f.get("nome", "")) + extra + "</li>")
        a("</ul></div>")

    # Eixos
    if notas:
        a("<div class='card'><h2>Nota por eixo</h2>")
        for k in ORDEM:
            if k not in notas:
                continue
            n = int(notas[k])
            a("<div class='eixo'><div class='nome'>" + ROTULOS[k] + "</div>")
            a("<div class='bar'><i style='width:" + str(n * 10) + "%;background:" + cor_nota(n) + "'></i></div>")
            a("<div class='n'>" + str(n) + "/10</div>")
            if just.get(k):
                a("<div class='just'>" + e(just[k]) + "</div>")
            a("</div>")
        a("</div>")

    # Risco / armadilha
    if d.get("risco") or d.get("armadilha"):
        a("<div class='card'><h2>Maior risco</h2>")
        if d.get("risco"):
            a("<p>" + e(d["risco"]) + "</p>")
        if d.get("armadilha"):
            a("<div class='warn' style='margin-top:14px'><strong>Armadilha à vista:</strong> " +
              e(d["armadilha"]) + "</div>")
        a("</div>")

    # Pesquisa
    if d.get("pesquisa"):
        a("<div class='card'><h2>O que achamos no mercado</h2><ul>")
        for item in d["pesquisa"]:
            a("<li class='dot'>" + e(item) + "</li>")
        a("</ul></div>")

    # Teste 7 dias
    if d.get("teste_7_dias"):
        a("<div class='card'><h2>Teste de 7 dias (antes de programar)</h2><table>")
        for item in d["teste_7_dias"]:
            if isinstance(item, dict):
                a("<tr><td>" + e(item.get("dia", "")) + "</td><td>" + e(item.get("acao", "")) + "</td></tr>")
            else:
                txt = str(item)
                if ":" in txt[:14]:
                    dia, acao = txt.split(":", 1)
                    a("<tr><td>" + e(dia) + "</td><td>" + e(acao.strip()) + "</td></tr>")
                else:
                    a("<tr><td></td><td>" + e(txt) + "</td></tr>")
        a("</table></div>")

    # Escopo
    if d.get("telas") or d.get("nao_faz"):
        a("<div class='card'><h2>Escopo da v1</h2>")
        if d.get("telas"):
            a("<h3>As telas</h3><div class='grid'>")
            for i, t in enumerate(d["telas"], 1):
                if isinstance(t, dict):
                    nome, acao = t.get("nome", ""), t.get("acao", "")
                else:
                    nome, acao = str(t), ""
                a("<div class='tela'><div class='num'>TELA " + str(i) + "</div>")
                a("<div class='tn'>" + e(nome) + "</div>")
                if acao:
                    a("<div class='ta'>" + e(acao) + "</div>")
                a("</div>")
            a("</div>")
        if d.get("nao_faz"):
            a("<h3>Não entra na v1</h3><ul>")
            for item in d["nao_faz"]:
                a("<li class='cut'>" + e(item) + "</li>")
            a("</ul>")
        a("</div>")

    # Cobranca
    c = d.get("cobranca")
    if c:
        a("<div class='card'><h2>Como cobrar</h2><table>")
        if c.get("rota"):
            a("<tr><td>Rota</td><td>" + e(c["rota"]) + "</td></tr>")
        if c.get("preco"):
            a("<tr><td>Preço</td><td><strong>" + e(c["preco"]) + "</strong></td></tr>")
        if c.get("frase"):
            a("<tr><td>Fala</td><td>“" + e(c["frase"]) + "”</td></tr>")
        a("</table></div>")

    # Primeiro passo
    if d.get("primeiro_passo"):
        a("<div class='card step'><h2>Segunda-feira você faz isso</h2>")
        a("<div class='big'>" + e(d["primeiro_passo"]) + "</div></div>")

    a("<div class='foot'>Gerado pela skill validador-microapp</div>")
    a("</div></body></html>")
    return "".join(p)


def main():
    ap = argparse.ArgumentParser(description="Gera dashboard HTML da validacao")
    ap.add_argument("--input", "-i", required=True, help="arquivo JSON de entrada ('-' para stdin)")
    ap.add_argument("--output", "-o", required=True, help="arquivo HTML de saida")
    args = ap.parse_args()

    try:
        if args.input == "-":
            data = json.load(sys.stdin)
        else:
            with open(args.input, encoding="utf-8") as f:
                data = json.load(f)
    except (OSError, json.JSONDecodeError) as err:
        print("Erro ao ler o JSON: " + str(err), file=sys.stderr)
        return 1

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(build(data))

    print("Dashboard gerado: " + args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
