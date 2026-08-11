#!/usr/bin/env python3
"""Calcula a nota e o veredito de uma ideia de micro-aplicacao.

Mantem a nota consistente entre alunos diferentes.

Uso:
    python3 score.py --dor 8 --recorrencia 9 --pagador 7 \\
        --simplicidade 9 --canal 10 --substituicao 8 \\
        --filtros passa,passa,passa,passa,passa

    python3 score.py ... --json > resultado.json
"""

import argparse
import json
import sys

EIXOS = ["dor", "recorrencia", "pagador", "simplicidade", "canal", "substituicao"]

ROTULOS = {
    "dor": "Dor",
    "recorrencia": "Recorrencia",
    "pagador": "Pagador",
    "simplicidade": "Simplicidade",
    "canal": "Canal",
    "substituicao": "Substituicao",
}

NOMES_FILTROS = [
    "Problema unico",
    "Recorrencia",
    "Gambiarra atual",
    "Pagador claro",
    "Entregavel rapido",
]

# Eixos que, se baixos, limitam o veredito independente da nota total.
EIXOS_VETO = ["pagador", "substituicao"]
LIMITE_VETO = 4


def calcular(notas, filtros_passa):
    """Retorna dict com score, veredito e diagnostico."""
    for eixo in EIXOS:
        v = notas[eixo]
        if not (0 <= v <= 10):
            raise ValueError(f"Nota de '{eixo}' deve estar entre 0 e 10 (recebido {v})")

    bruto = sum(notas[e] for e in EIXOS)
    score = round(bruto / 60 * 100)

    reprovados = [n for n, ok in zip(NOMES_FILTROS, filtros_passa) if not ok]
    n_reprovados = len(reprovados)

    vetos = [e for e in EIXOS_VETO if notas[e] < LIMITE_VETO]

    # 1) Filtros mandam mais que a nota.
    if n_reprovados >= 2:
        veredito = "REFORMULA"
        motivo = (
            f"Falhou em {n_reprovados} filtros de corte ({', '.join(reprovados)}). "
            "A nota nao vale enquanto o recorte estiver errado."
        )
    else:
        if score >= 80:
            veredito, motivo = "CONSTROI", "Nota alta e filtros ok. Faca o teste de 7 dias e construa."
        elif score >= 60:
            veredito, motivo = "CONSTROI COM CORTE", "Boa ideia, mas grande demais. Corte para o nucleo antes de comecar."
        elif score >= 40:
            veredito, motivo = "REFORMULA", "O problema e real, o recorte esta errado."
        else:
            veredito, motivo = "DESCARTA", "Nao vale como produto. Pode virar funcionalidade ou servico manual."

        # 2) Veto por eixo critico baixo.
        if vetos and veredito in ("CONSTROI", "CONSTROI COM CORTE"):
            nomes = " e ".join(ROTULOS[e] for e in vetos)
            veredito = "REFORMULA"
            motivo = (
                f"Veto: o eixo {nomes} ficou abaixo de {LIMITE_VETO}. "
                "Sem pagador claro ou sem substituicao concreta, nao ha produto."
            )

        # 3) Um filtro reprovado derruba CONSTROI para CONSTROI COM CORTE.
        if n_reprovados == 1 and veredito == "CONSTROI":
            veredito = "CONSTROI COM CORTE"
            motivo = f"Falhou no filtro '{reprovados[0]}'. Conserte isso antes de construir."

    fortes = sorted(EIXOS, key=lambda e: -notas[e])[:2]
    fracos = sorted(EIXOS, key=lambda e: notas[e])[:2]

    return {
        "notas": {e: notas[e] for e in EIXOS},
        "score": score,
        "bruto": f"{bruto}/60",
        "veredito": veredito,
        "motivo": motivo,
        "filtros": [
            {"nome": n, "passa": bool(ok)}
            for n, ok in zip(NOMES_FILTROS, filtros_passa)
        ],
        "filtros_reprovados": reprovados,
        "pontos_fortes": [ROTULOS[e] for e in fortes],
        "pontos_fracos": [ROTULOS[e] for e in fracos],
        "vetos": [ROTULOS[e] for e in vetos],
    }


def _parse_filtros(texto):
    if not texto:
        return [True] * 5
    itens = [t.strip().lower() for t in texto.split(",")]
    if len(itens) != 5:
        raise ValueError("--filtros precisa de exatamente 5 valores separados por virgula")
    verdadeiros = {"passa", "sim", "s", "ok", "true", "1", "y"}
    return [i in verdadeiros for i in itens]


def main():
    p = argparse.ArgumentParser(description="Nota e veredito de micro-aplicacao")
    for eixo in EIXOS:
        p.add_argument(f"--{eixo}", type=int, required=True, help=f"Nota 0-10 para {ROTULOS[eixo]}")
    p.add_argument(
        "--filtros",
        default="",
        help="5 valores: passa|falha separados por virgula (ordem: problema unico, recorrencia, gambiarra, pagador, entregavel)",
    )
    p.add_argument("--ideia", default="", help="Nome curto da ideia")
    p.add_argument("--json", action="store_true", help="Saida em JSON")
    args = p.parse_args()

    notas = {e: getattr(args, e) for e in EIXOS}

    try:
        r = calcular(notas, _parse_filtros(args.filtros))
    except ValueError as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1

    if args.ideia:
        r["ideia"] = args.ideia

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    print()
    if args.ideia:
        print(f"  {args.ideia}")
        print()
    print("  Filtros de corte")
    for f in r["filtros"]:
        print(f"    [{'x' if f['passa'] else ' '}] {f['nome']}")
    print()
    print("  Notas")
    for e in EIXOS:
        barra = "#" * notas[e] + "." * (10 - notas[e])
        print(f"    {ROTULOS[e]:<14} {barra} {notas[e]}/10")
    print()
    print(f"  SCORE: {r['score']}/100   ({r['bruto']})")
    print(f"  VEREDITO: {r['veredito']}")
    print(f"  {r['motivo']}")
    print()
    print(f"  Mais fortes: {', '.join(r['pontos_fortes'])}")
    print(f"  Mais fracos: {', '.join(r['pontos_fracos'])}")
    if r["vetos"]:
        print(f"  Veto acionado em: {', '.join(r['vetos'])}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
