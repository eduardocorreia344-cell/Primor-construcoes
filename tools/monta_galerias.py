# -*- coding: utf-8 -*-
"""Preenche window.FOTOS, hero e og:image das duas vitrines.

Catalogacao feita olhando a folha de contato gerada. E uma leitura minha,
nao a confirmacao do Gabriel — ele corrige pelo catalogo.csv.
"""
import json, re
from pathlib import Path
from PIL import Image

# (numero, area, legenda)  — ordem de exibicao ja definida aqui.
ENSEADA = [
    ("017", "Portaria",       "Portaria"),
    ("001", "Piscina",        "Piscina e fachada"),
    ("007", "Piscina",        "Deck entre as piscinas"),
    ("002", "Piscina",        "Raia"),
    ("003", "Piscina",        "Raia e deck"),
    ("005", "Piscina",        "Prainha"),
    ("006", "Piscina",        "Piscina e paisagismo"),
    ("008", "Piscina",        "Piscina e espaco gourmet"),
    ("009", "Piscina",        "Deck"),
    ("010", "Piscina",        "Piscina"),
    ("011", "Piscina",        "Prainha e raia"),
    ("016", "Piscina",        "Piscina"),
    ("012", "Espaco gourmet", "Espaco gourmet"),
    ("013", "Espaco gourmet", "Bancada e mesa comunitaria"),
    ("014", "Jardins",        "Circulacao e paisagismo"),
    ("015", "Jardins",        "Varandas e jardim"),
    ("019", "Vista aerea",    "Vista aerea do conjunto"),
    ("018", "Vista aerea",    "Vista aerea das piscinas"),
    ("004", "Vista aerea",    "Vista aerea"),
]

LAGOA = [
    ("003", "Piscina",        "Deck entre as piscinas"),
    ("002", "Piscina",        "Piscina"),
    ("004", "Piscina",        "Piscina e fachada"),
    ("005", "Piscina",        "Prainha e raia"),
    ("006", "Piscina",        "Piscina e paisagismo"),
    ("010", "Piscina",        "Deck e espreguicadeiras"),
    ("008", "Playground",     "Playground"),
    ("013", "Espaco gourmet", "Espaco gourmet"),
    ("014", "Espaco gourmet", "Bancada e churrasqueira"),
    ("009", "Unidades",       "Varanda com brise de madeira"),
    ("011", "Unidades",       "Fachada e jardim"),
    ("012", "Unidades",       "Fachada e jardim"),
    ("007", "Jardins",        "Circulacao e paisagismo"),
    ("001", "Vista aerea",    "Vista aerea"),
]

PAGINAS = [
    ("paraiso-da-enseada", "Paraiso da Enseada", ENSEADA, "001"),
    ("paraiso-da-lagoa",   "Paraiso da Lagoa",   LAGOA,   "003"),
]


def gerar_og(slug: str, numero: str) -> None:
    """Recorta 1200x630 da foto de capa para o compartilhamento social."""
    src = Image.open(f"{slug}/fotos/{numero}.webp")
    alvo = 1200 / 630
    l, a = src.size
    if l / a > alvo:                      # mais larga: corta os lados
        nova_l = int(a * alvo)
        cx = (l - nova_l) // 2
        rec = src.crop((cx, 0, cx + nova_l, a))
    else:                                 # mais alta: corta topo/base
        nova_a = int(l / alvo)
        cy = (a - nova_a) // 3            # 1/3 favorece o ceu
        rec = src.crop((0, cy, l, cy + nova_a))
    rec.resize((1200, 630), Image.LANCZOS).save(f"{slug}/fotos/og.jpg", "JPEG",
                                                quality=84, optimize=True)


for slug, nome, catalogo, capa in PAGINAS:
    fotos = [
        {"thumb": f"/{slug}/fotos/{n}-thumb.webp",
         "full":  f"/{slug}/fotos/{n}.webp",
         "alt":   f"{area} do {nome}",
         "legenda": legenda}
        for n, area, legenda in catalogo
    ]
    js = json.dumps(fotos, ensure_ascii=True, indent=4).replace("\n", "\n  ")

    p = Path(slug) / "index.html"
    s = p.read_text(encoding="utf-8")

    # 1) window.FOTOS
    s = re.sub(r"window\.FOTOS = \[\];", f"window.FOTOS = {js};", s, count=1)
    s = re.sub(r"  /\* Preencher APOS a catalogacao manual.*?\*/\n", "", s,
               count=1, flags=re.S)

    # 2) hero
    s = s.replace(
        f'  /* CONFIRMAR: trocar pela foto de capa escolhida na catalogacao.\n'
        f'     .hero-vitrine {{ background-image: url("/{slug}/fotos/001.webp"); }} */',
        f'  .hero-vitrine {{ background-image: url("/{slug}/fotos/{capa}.webp"); }}')

    # 3) preload da capa
    s = s.replace(
        f'<!-- CONFIRMAR: apos catalogar as fotos, adicionar o preload da foto de capa:\n'
        f'     <link rel="preload" as="image" fetchpriority="high" href="/{slug}/fotos/001.webp"> -->',
        f'<link rel="preload" as="image" fetchpriority="high" href="/{slug}/fotos/{capa}.webp">')

    # 4) og:image
    s = s.replace(
        '<!-- CONFIRMAR: apontar para uma foto real do empreendimento (1200x630), nao a logo. -->\n', '')

    p.write_text(s, encoding="utf-8")
    gerar_og(slug, capa)
    print(f"{slug}: {len(fotos)} fotos na galeria, capa {capa}, og.jpg gerado")
