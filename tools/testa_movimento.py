#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testa o movimento do site. Criterio unico e severo: ao fim de cada cenario,
nenhum elemento do grupo de entrada pode continuar com opacity: 0.

    python3 -m http.server 8099 &
    python3 tools/testa_movimento.py
"""
import sys

from playwright.sync_api import sync_playwright

BASE = "http://localhost:8099"
EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SEL = (".secao .filete,.titulo-secao,.marco,.card,.depoimento,.ficha > div,"
       ".texto-institucional p,.sobre-grid > div,.galeria-item,.cta-ilhabela h2,"
       ".cta-ilhabela p,.cta-ilhabela .btn,.secao-cinza > .wrap > p,.cadastro-caixa")
# O site tem scroll-behavior: smooth; scrollTo animado mediria no meio do movimento.
IR = "(y) => window.scrollTo({top: y, behavior: 'instant'})"

falhas = []


def checa(nome, condicao, detalhe=""):
    print(f"  {'OK    ' if condicao else 'FALHOU'} {nome} {detalhe}")
    if not condicao:
        falhas.append(nome)


def escondidos(pg):
    return pg.evaluate(
        f"() => [...document.querySelectorAll({SEL!r})]"
        ".filter(el => getComputedStyle(el).opacity === '0').length")


def altura_header(pg):
    return pg.evaluate("Math.round(document.querySelector('.topo .wrap')"
                       ".getBoundingClientRect().height)")


def main() -> int:
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])

        for caminho in ["/", "/paraiso-da-enseada/", "/paraiso-da-lagoa/"]:
            nome = caminho.strip("/") or "home"
            print(f"--- {nome} ---")
            pg = nav.new_page(viewport={"width": 1440, "height": 900})
            erros = []
            pg.on("pageerror", lambda e: erros.append(str(e)))
            pg.goto(BASE + caminho, wait_until="networkidle")
            pg.wait_for_timeout(900)
            checa(f"{nome}/sem-erro-js", not erros, str(erros[:1]))

            pg.evaluate(IR, 999999)
            pg.wait_for_timeout(1500)
            n = escondidos(pg)
            checa(f"{nome}/salto-ao-fim", n == 0, f"({n} invisiveis)")

            pg.evaluate(IR, 0)
            pg.wait_for_timeout(400)
            for _ in range(16):
                pg.mouse.wheel(0, 600)
                pg.wait_for_timeout(110)
            pg.wait_for_timeout(1200)
            n = escondidos(pg)
            checa(f"{nome}/scroll-gradual", n == 0, f"({n} invisiveis)")

            pg.evaluate(IR, 0); pg.wait_for_timeout(650); a = altura_header(pg)
            pg.evaluate(IR, 500); pg.wait_for_timeout(650); c = altura_header(pg)
            pg.evaluate(IR, 0); pg.wait_for_timeout(650); v = altura_header(pg)
            checa(f"{nome}/header", a == 104 and c == 72 and v == 104, f"({a}->{c}->{v})")
            pg.close()

        print("--- degradacao ---")
        for extra, nome in [({"java_script_enabled": False}, "sem-javascript"),
                            ({"reduced_motion": "reduce"}, "reduced-motion")]:
            ctx = nav.new_context(viewport={"width": 1440, "height": 900}, **extra)
            pg = ctx.new_page()
            pg.goto(BASE + "/paraiso-da-lagoa/", wait_until="load")
            pg.wait_for_timeout(1000)
            n = escondidos(pg)
            checa(nome, n == 0, f"({n} invisiveis)")
            ctx.close()

        nav.close()

    print("\n" + ("tudo passou" if not falhas else f"FALHAS -> {falhas}"))
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
