#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testa o formulario de cadastro da home.

    python3 -m http.server 8099 &
    python3 tools/testa_formulario.py
"""
import sys

from playwright.sync_api import sync_playwright

BASE = "http://localhost:8099"
EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
BOTAO = ".cadastro-caixa button[type=submit]"

falhas = []


def checa(nome, condicao, detalhe=""):
    print(f"  {'OK    ' if condicao else 'FALHOU'} {nome} {detalhe}")
    if not condicao:
        falhas.append(nome)


def main() -> int:
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        pg = nav.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(BASE + "/#cadastro", wait_until="networkidle")
        pg.wait_for_timeout(1500)

        def estado():
            return pg.text_content(".cadastro-estado").strip()

        pg.click(BOTAO); pg.wait_for_timeout(400)
        invalidos = pg.evaluate("document.querySelectorAll('[aria-invalid=\"true\"]').length")
        checa("vazio/bloqueado", "Confira os campos" in estado() and invalidos == 2)

        pg.fill("#cad-nome", "Gabriel Goto"); pg.fill("#cad-email", "gabriel@")
        pg.click(BOTAO); pg.wait_for_timeout(300)
        checa("email-invalido", pg.get_attribute("#cad-email", "aria-invalid") == "true")

        pg.fill("#cad-email", "gabriel@exemplo.com")
        pg.click(BOTAO); pg.wait_for_timeout(300)
        checa("sem-consentimento", pg.get_attribute(".consentimento", "data-invalido") == "true")

        pg.check("#cad-aceite"); pg.click(BOTAO); pg.wait_for_timeout(400)
        checa("destino-vazio/recusa", "não configurado" in estado())

        pg.route("**/fake-ok", lambda r: r.fulfill(status=200, body='{"ok":true}',
                                                   content_type="application/json"))
        pg.evaluate("window.CADASTRO_ENDPOINT = '/fake-ok'")
        pg.click(BOTAO); pg.wait_for_timeout(900)
        checa("envio-ok", "Cadastro recebido" in estado() and pg.input_value("#cad-nome") == "")

        pg.route("**/fake-erro", lambda r: r.fulfill(status=500, body="erro"))
        pg.evaluate("window.CADASTRO_ENDPOINT = '/fake-erro'")
        pg.fill("#cad-nome", "Teste"); pg.fill("#cad-email", "t@t.com"); pg.check("#cad-aceite")
        pg.click(BOTAO); pg.wait_for_timeout(900)
        # Em erro o formulario nao pode ser limpo: redigitar afasta a pessoa.
        checa("erro-servidor", "Não foi possível" in estado()
              and pg.input_value("#cad-nome") == "Teste")

        enviou = []
        pg.route("**/fake-bot", lambda r: (enviou.append(1), r.fulfill(status=200, body="{}")))
        pg.evaluate("window.CADASTRO_ENDPOINT = '/fake-bot'")
        pg.evaluate("document.querySelector('#cad-site').value = 'http://spam.exemplo'")
        pg.click(BOTAO); pg.wait_for_timeout(700)
        checa("armadilha-robo", not enviou and "Obrigado" in estado())

        checa("armadilha-fora-do-teclado",
              pg.get_attribute("#cad-site", "tabindex") == "-1"
              and pg.evaluate("document.querySelector('.armadilha')"
                              ".getBoundingClientRect().left < -1000"))
        nav.close()

    print("\n" + ("tudo passou" if not falhas else f"FALHAS -> {falhas}"))
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
