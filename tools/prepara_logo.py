#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepara a logo da PRIMOR para uso no site, a partir do PNG em fundo branco.

Gera:
    assets/img/logo-primor.png        fundo transparente — header (fundo claro)
    assets/img/logo-primor-branca.png wordmark em branco   — rodape (fundo preto)

O wordmark da logo e preto e o rodape do site e preto: sem a versao invertida
a marca sumiria la. A versao branca clareia so os pixels sem cor (preto e
cinza do texto) e preserva o hexagono vermelho.

Uso: python3 tools/prepara_logo.py "Logo Primor.png"
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

LARGURA_SAIDA = 400  # ~4x o tamanho de exibicao; sobra para telas retina


def remover_fundo_branco(img: Image.Image) -> Image.Image:
    """Tira o matte branco: alpha = quanto o pixel se afasta do branco."""
    rgb = np.asarray(img.convert("RGB"), dtype=np.float32)
    alpha = 255.0 - rgb.min(axis=2)

    # Desfaz a composicao sobre branco: cor = (pixel - branco*(1-a)) / a
    a = np.clip(alpha, 1.0, 255.0)[..., None] / 255.0
    cor = np.clip((rgb - 255.0 * (1.0 - a)) / a, 0, 255)

    saida = np.dstack([cor, alpha]).astype(np.uint8)
    return Image.fromarray(saida, "RGBA")


def versao_branca(img: Image.Image, limiar_saturacao: int = 45) -> Image.Image:
    """Clareia o que e neutro (texto preto/cinza) e mantem o que tem cor.

    O "EMPREENDIMENTOS" e cinza medio, entao sai do fundo branco com alpha
    baixo (~40%). Pintado de branco e composto sobre o rodape preto, ele
    voltaria a ser cinza escuro. A gama no alpha dos pixels neutros compensa
    isso sem estourar o tracado.
    """
    arr = np.asarray(img, dtype=np.float32).copy()
    rgb = arr[..., :3]
    saturacao = rgb.max(axis=2) - rgb.min(axis=2)
    neutro = saturacao < limiar_saturacao

    arr[..., :3][neutro] = 255.0
    a = arr[..., 3] / 255.0
    arr[..., 3] = np.where(neutro, np.power(a, 0.62) * 255.0, arr[..., 3])

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


def main() -> None:
    origem = Path(sys.argv[1] if len(sys.argv) > 1 else "Logo Primor.png")
    if not origem.exists():
        sys.exit(f"ERRO: '{origem}' nao encontrado.")

    img = remover_fundo_branco(Image.open(origem))

    caixa = img.getchannel("A").getbbox()
    if caixa:
        img = img.crop(caixa)
    print(f"recortado para o conteudo: {img.size}")

    escala = LARGURA_SAIDA / img.width
    img = img.resize((LARGURA_SAIDA, round(img.height * escala)), Image.LANCZOS)

    destino = Path("assets/img")
    destino.mkdir(parents=True, exist_ok=True)
    # WebP com alpha: um PNG desta logo passa de 400 KB, no header inteiro.
    img.save(destino / "logo-primor.webp", "WEBP", quality=80, method=6)
    versao_branca(img).save(destino / "logo-primor-branca.webp", "WEBP",
                            quality=80, method=6)

    for nome in ("logo-primor.webp", "logo-primor-branca.webp"):
        caminho = destino / nome
        print(f"  {caminho}  {Image.open(caminho).size}  {caminho.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
