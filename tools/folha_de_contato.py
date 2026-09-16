#!/usr/bin/env python3
"""
Folha de contato numerada + conversao para WebP.

Regra do projeto (secao 5 do briefing): nunca presumir a qual area do
empreendimento cada foto pertence. Este script NAO agrupa nada. Ele so
numera, converte e gera uma folha para catalogacao manual.

Uso:
    pip install Pillow
    python3 tools/folha_de_contato.py Paraiso_da_Enseada.zip paraiso-da-enseada
    python3 tools/folha_de_contato.py Paraiso_da_lagoa.zip   paraiso-da-lagoa

Saida em <destino>/:
    fotos/NNN.webp          foto completa (max 1600px, q80) — para o lightbox

As fotos do Drive sao screenshots de celular: a imagem fica numa faixa no
meio e o resto e tarja preta. O script detecta e corta essas tarjas antes
de converter, e avisa no relatorio quais fotos foram cortadas.
    fotos/NNN-thumb.webp    miniatura (max 520px, q78)      — para o card
    folha-de-contato.html   grade numerada para abrir no navegador
    folha-de-contato.jpg    mesma grade como imagem unica (mandar no WhatsApp)
    catalogo.csv            planilha para o Gabriel preencher a area de cada foto
"""
import csv
import os
import shutil
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

EXTENSOES = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".bmp", ".tif", ".tiff"}
LARGURA_FULL = 1600
LARGURA_THUMB = 520
COLUNAS_FOLHA = 4
CELULA_FOLHA = 460


def coletar(origem: Path, trabalho: Path) -> list[Path]:
    """Extrai o zip (ou copia a pasta) e devolve as fotos em ordem estavel."""
    if trabalho.exists():
        shutil.rmtree(trabalho)
    trabalho.mkdir(parents=True)

    if origem.is_file() and origem.suffix.lower() == ".zip":
        with zipfile.ZipFile(origem) as z:
            z.extractall(trabalho)
    elif origem.is_dir():
        shutil.copytree(origem, trabalho, dirs_exist_ok=True)
    else:
        sys.exit(f"ERRO: '{origem}' nao e um .zip nem uma pasta.")

    fotos = [
        p for p in trabalho.rglob("*")
        if p.is_file()
        and p.suffix.lower() in EXTENSOES
        and not p.name.startswith(("._", "."))
        and "__MACOSX" not in p.parts
    ]
    # Ordem estavel e previsivel: o numero da folha tem que bater sempre.
    fotos.sort(key=lambda p: p.name.lower())
    if not fotos:
        sys.exit(f"ERRO: nenhuma imagem encontrada em '{origem}'.")
    return fotos


def _maior_faixa(escuro: list[bool], minimo: int) -> tuple[int, int]:
    """Indices (inicio, fim) da maior sequencia continua de linhas nao escuras."""
    melhor = (0, len(escuro))
    melhor_tam = -1
    i = 0
    while i < len(escuro):
        if escuro[i]:
            i += 1
            continue
        j = i
        while j < len(escuro) and not escuro[j]:
            j += 1
        if j - i > melhor_tam:
            melhor_tam, melhor = j - i, (i, j)
        i = j
    return melhor if melhor_tam >= minimo else (0, len(escuro))


def cortar_tarjas(img: Image.Image, limiar: int = 24) -> Image.Image:
    """Remove tarjas pretas de screenshot (letterbox/pillarbox).

    As fotos vieram como screenshot de celular: a foto ocupa uma faixa no meio
    e o resto e tarja preta. Sem este corte a galeria publica retangulos pretos.

    Procura a MAIOR faixa continua de linhas nao escuras, em vez de aparar a
    partir da borda. A barra do indicador de home do iOS e uma faixa clara e
    fina dentro da tarja preta: aparando pela borda o corte pararia nela e
    sobraria quase toda a tarja. Pela maior faixa, a foto sempre vence.
    """
    cinza = img.convert("L")
    larg, alt = cinza.size
    px = cinza.load()

    passo_x = max(1, larg // 200)
    passo_y = max(1, alt // 200)

    linhas = [max(px[x, y] for x in range(0, larg, passo_x)) < limiar for y in range(alt)]
    topo, base = _maior_faixa(linhas, minimo=max(64, alt // 12))

    colunas = [max(px[x, y] for y in range(topo, base, passo_y)) < limiar for x in range(larg)]
    esq, dir_ = _maior_faixa(colunas, minimo=max(64, larg // 12))

    if (topo, esq, base, dir_) == (0, 0, alt, larg):
        return img

    # Guarda: tarja de screenshot e preto puro; foto escura de verdade (ceu
    # noturno, sombra) tem ruido e media bem acima de zero. Sem esta checagem
    # uma foto legitimamente escura seria recortada ate so sobrar o ponto claro.
    recorte = cinza.crop((esq, topo, dir_, base))
    soma_total = sum(i * n for i, n in enumerate(cinza.histogram()))
    soma_recorte = sum(i * n for i, n in enumerate(recorte.histogram()))
    pixels_fora = larg * alt - recorte.width * recorte.height
    if pixels_fora <= 0:
        return img
    media_tarja = (soma_total - soma_recorte) / pixels_fora
    if media_tarja > 6:
        return img

    return img.crop((esq, topo, dir_, base))


def abrir_corrigida(caminho: Path) -> Image.Image:
    """Abre a imagem ja com a rotacao do EXIF aplicada e em RGB."""
    img = Image.open(caminho)
    img = ImageOps.exif_transpose(img)
    return cortar_tarjas(img.convert("RGB"))


def converter(fotos: list[Path], destino: Path) -> list[dict]:
    pasta = destino / "fotos"
    pasta.mkdir(parents=True, exist_ok=True)
    registros = []

    for i, origem in enumerate(fotos, start=1):
        num = f"{i:03d}"
        bruta = ImageOps.exif_transpose(Image.open(origem)).convert("RGB")
        img = cortar_tarjas(bruta)
        cortou = img.size != bruta.size

        full = img.copy()
        full.thumbnail((LARGURA_FULL, LARGURA_FULL), Image.LANCZOS)
        full.save(pasta / f"{num}.webp", "WEBP", quality=80, method=6)

        thumb = img.copy()
        thumb.thumbnail((LARGURA_THUMB, LARGURA_THUMB), Image.LANCZOS)
        thumb.save(pasta / f"{num}-thumb.webp", "WEBP", quality=78, method=6)

        registros.append({
            "numero": num,
            "arquivo_original": origem.name,
            "largura": full.width,
            "altura": full.height,
        })
        marca = "  [tarja cortada]" if cortou else ""
        print(f"  {num}  {origem.name}  ->  {full.width}x{full.height}{marca}")

    return registros


def gerar_html(registros: list[dict], destino: Path, titulo: str) -> None:
    linhas = "\n".join(
        f'''    <figure>
      <img src="fotos/{r["numero"]}-thumb.webp" alt="Foto {r["numero"]}" loading="lazy">
      <figcaption><b>{r["numero"]}</b><span>{r["arquivo_original"]}</span></figcaption>
    </figure>'''
        for r in registros
    )
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Folha de contato — {titulo}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         background:#141518; color:#eee; margin:0; padding:28px; }}
  h1 {{ font-size:20px; margin:0 0 6px; }}
  p.aviso {{ color:#9aa0a6; font-size:14px; margin:0 0 26px; max-width:70ch; }}
  .grade {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:16px; }}
  figure {{ margin:0; background:#1e2024; border-radius:6px; overflow:hidden; }}
  figure img {{ width:100%; aspect-ratio:4/3; object-fit:cover; display:block; }}
  figcaption {{ padding:9px 11px; display:flex; align-items:baseline; gap:9px; }}
  figcaption b {{ font-size:19px; color:#ffcf5c; }}
  figcaption span {{ font-size:11px; color:#80868b; word-break:break-all; }}
</style>
</head>
<body>
<h1>Folha de contato — {titulo}</h1>
<p class="aviso">
  {len(registros)} fotos, sem nenhum agrupamento. Anote, para cada numero, a qual area
  ou ambiente do empreendimento a foto pertence (ex.: 007 = piscina, 012 = fachada,
  018 = planta baixa). Nada vai para o site antes dessa confirmacao.
</p>
<div class="grade">
{linhas}
</div>
</body>
</html>
"""
    (destino / "folha-de-contato.html").write_text(html, encoding="utf-8")


def gerar_jpg(registros: list[dict], destino: Path) -> None:
    """Folha de contato como imagem unica — pratica de mandar no WhatsApp."""
    pasta = destino / "fotos"
    cel = CELULA_FOLHA
    faixa = 58
    cols = COLUNAS_FOLHA
    linhas_n = (len(registros) + cols - 1) // cols

    folha = Image.new("RGB", (cols * cel, linhas_n * (cel + faixa)), "#141518")
    desenho = ImageDraw.Draw(folha)
    try:
        fonte = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34
        )
    except OSError:
        fonte = ImageFont.load_default()

    for i, r in enumerate(registros):
        col, lin = i % cols, i // cols
        x, y = col * cel, lin * (cel + faixa)

        foto = Image.open(pasta / f"{r['numero']}.webp")
        foto = ImageOps.fit(foto, (cel - 8, cel - 8), Image.LANCZOS)
        folha.paste(foto, (x + 4, y + 4))
        desenho.text((x + 14, y + cel + 8), r["numero"], font=fonte, fill="#ffcf5c")

    folha.save(destino / "folha-de-contato.jpg", "JPEG", quality=82, optimize=True)


def gerar_csv(registros: list[dict], destino: Path) -> None:
    with open(destino / "catalogo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["numero", "arquivo_original", "area_ou_ambiente", "usar_no_site", "legenda"])
        for r in registros:
            w.writerow([r["numero"], r["arquivo_original"], "", "", ""])


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(f"Uso: python3 {sys.argv[0]} <fotos.zip|pasta> <pasta-destino>")

    origem = Path(sys.argv[1])
    destino = Path(sys.argv[2])
    titulo = destino.name.replace("-", " ").title()

    print(f"Lendo {origem} ...")
    fotos = coletar(origem, destino / ".tmp-extraido")
    print(f"{len(fotos)} fotos encontradas. Convertendo para WebP:\n")

    registros = converter(fotos, destino)
    gerar_html(registros, destino, titulo)
    gerar_jpg(registros, destino)
    gerar_csv(registros, destino)
    shutil.rmtree(destino / ".tmp-extraido", ignore_errors=True)

    print(f"""
Pronto.
  {destino}/folha-de-contato.html   abra no navegador
  {destino}/folha-de-contato.jpg    mande no WhatsApp
  {destino}/catalogo.csv            preencha a coluna 'area_ou_ambiente'
  {destino}/fotos/                  {len(registros)} fotos em WebP (full + thumb)
""")


if __name__ == "__main__":
    main()
