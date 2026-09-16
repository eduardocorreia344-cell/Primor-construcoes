# -*- coding: utf-8 -*-
"""Gera as duas paginas de vitrine a partir de um template unico."""
from pathlib import Path

TPL = Path("/tmp/vitrine.tpl").read_text(encoding="utf-8")

DEP_CIRO = """
        <figure class="depoimento">
          <blockquote>
            Apos pesquisarmos inumeros villages em Itacimirim, adquirimos uma unidade no
            Paraiso da Enseada, construido pela Primor. Posso dizer que foi uma excelente
            escolha, pois o imovel foi construido com muito cuidado, utilizado material de
            acabamento de primeira, projeto arquitetonico de muito bom gosto, sem falar nos
            responsaveis pela empresa, que sao muito solicitos e sempre disponiveis pra sanar
            qualquer problema mesmo algum tempo apos entregue o imovel. Confio e indico
            qualquer empreendimento da Primor.
          </blockquote>
          <footer>
            <cite>Ciro <span class="pendente">CONFIRMAR sobrenome</span></cite>
            <p class="origem">Proprietario &middot; Paraiso da Enseada</p>
          </footer>
        </figure>"""

DEP_JAIRO = """
        <figure class="depoimento">
          <blockquote>
            Tivemos uma experiencia incrivel com a Primor, quando resolvemos investir na
            aquisicao de uma unidade no condominio Paraiso da Lagoa, em Itacimirim. Tudo
            muito bem feito, materia prima de muita qualidade e bom gosto. Encontramos
            flexibilidade na negociacao e o atendimento e um encantamento a parte! Estamos
            felizes e muito satisfeitos com a aquisicao!
          </blockquote>
          <footer>
            <cite>Jairo e Rosana <span class="pendente">CONFIRMAR sobrenome</span></cite>
            <p class="origem">Proprietarios &middot; Paraiso da Lagoa</p>
          </footer>
        </figure>"""

DEP_PHILIPE = """
        <figure class="depoimento">
          <blockquote>
            Primor, construtora que preza pela qualidade e acabamento nos minimos detalhes.
            O que mais me deixou satisfeito e impressionado foi o fato do proprietario da
            construtora estar sempre na obra, cuidando para que tudo saia como o cliente espera.
          </blockquote>
          <footer>
            <cite>Philipe Ralejo</cite>
            <p class="origem">Proprietario &middot; Paraiso da Lagoa</p>
          </footer>
        </figure>"""

PAGINAS = [
    {
        "slug": "paraiso-da-enseada",
        "nome": "Paraiso da Enseada",
        "ano": "2018",
        "unidades": "16",
        "depoimentos": DEP_CIRO,
    },
    {
        "slug": "paraiso-da-lagoa",
        "nome": "Paraiso da Lagoa",
        "ano": "2021",
        "unidades": "32",
        "depoimentos": DEP_JAIRO + "\n" + DEP_PHILIPE,
    },
]

for p in PAGINAS:
    html = TPL
    for chave, valor in p.items():
        html = html.replace("__" + chave.upper() + "__", valor)
    destino = Path(p["slug"]) / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")
    print("gerado:", destino)
