# Paraíso da Enseada — áreas identificadas nas fotos

Levantado a partir das fotos enviadas no chat. **Isto é uma proposta de
agrupamento, não uma catalogação final.** Serve para decidir a estrutura da
galeria antes de os arquivos chegarem. A associação foto-a-foto continua sendo
manual, via `tools/folha_de_contato.py` + `catalogo.csv`.

## Áreas

| # | Área | O que aparece |
|---|---|---|
| 1 | Portaria | Portão e cerca de madeira roliça, guarita de vidro, placa "Paraíso da Enseada" sobre base terracota |
| 2 | Piscina — nível do solo | Piscina principal em L, prainha com degraus, deck de madeira, espreguiçadeiras, guarda-sóis listrados laranja/vermelho |
| 3 | Piscina — vista aérea | Drone top-down e drone em ângulo, mostrando a implantação do conjunto |
| 4 | Espaço gourmet | Cobertura de madeira roliça com tábua corrida, bancada com azulejaria estampada, mesa longa e banquetas |
| 5 | Fachada dos blocos | Dois pavimentos, estrutura de madeira roliça, varandas com guarda-corpo em treliça, telha cerâmica |
| 6 | Jardins e circulação | Passeios de tijolo, paisagismo, balizadores, palmeiras |

## Observações que afetam o resultado

**As fotos do Drive são screenshots de celular.** Todas as que chegaram pelo
chat têm tarja preta em cima e embaixo, mais a barra do indicador de home do
iOS. Os nomes no Drive (`IMG_0727.PNG`, `IMG_6877.PNG`) são consistentes com
isso. O `folha_de_contato.py` já detecta e corta essas tarjas, mas cortar uma
tarja não devolve resolução: o que sobra é a faixa de foto na resolução da
tela, não a foto original.

**Existem originais em resolução boa.** As duas primeiras imagens enviadas
tinham cerca de 2000 px de largura e nenhuma tarja — são os arquivos do
fotógrafo. Se a pasta completa desses originais existir, ela dá um resultado
muito melhor que os screenshots, principalmente no hero e no lightbox.
Vale procurar antes de processar os screenshots.

**Há fotos repetidas.** Pelo menos a fachada da portaria, a aérea top-down e a
aérea em ângulo apareceram duas vezes. Duplicata na galeria é ruído — a coluna
`usar_no_site` do `catalogo.csv` existe para isso.

## Paleta observada

Terracota das paredes, madeira roliça clara, telha cerâmica, laranja/vermelho
dos guarda-sóis, azul das piscinas, verde do paisagismo. A identidade da página
segue a da PRIMOR (preto/vermelho), mas o vermelho da marca convive bem com o
terracota do empreendimento — não há conflito a resolver aqui.
