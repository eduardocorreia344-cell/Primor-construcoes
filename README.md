# Site institucional PRIMOR Empreendimentos

Site estatico, um repositorio, um projeto Vercel. Sem build: e HTML/CSS/JS puro.

## Estrutura

```
/                      index.html         Home institucional PRIMOR          [construida]
/paraiso-da-enseada/   index.html         Vitrine institucional              [texto pronto, faltam fotos]
/paraiso-da-lagoa/     index.html         Vitrine institucional              [texto pronto, faltam fotos]
/ilhabela/             —                  Site de vendas                     [NAO migrado — ver abaixo]
/assets/css/primor.css                    Marca: paleta, tipografia, header, rodape, depoimentos
/assets/css/vitrine.css                   Estilos das paginas de entregues
/assets/js/galeria.js                     Galeria + lightbox
/tools/                                   Scripts de apoio
```

## Identidade visual

Derivada da logo: wordmark preto + hexagono vermelho.

| Token | Valor | Uso |
|---|---|---|
| `--preto` | `#0e0e0e` | Hero, rodape, tipografia |
| `--vermelho` | `#d92b20` | CTA, filete, faixa juridica, tag "em vendas" |
| `--vermelho-vivo` | `#e8443a` | Hover, destaque sobre preto |
| Neutros | `#fafafa` a `#3d3d3d` | Superficies e texto secundario |

Tipografia: **Poppins** (Google Fonts), familia unica. E a correspondencia mais
proxima do wordmark — geometrica, "O" circular, "R" de perna reta.

**A logo e ~90% preta e ~10% vermelha. O site segue a mesma proporcao.**
Vermelho e acento, nunca superficie grande. Pintar o site de vermelho seria
usar a cor de alerta da marca como cor de fundo — e um site de incorporadora
nao pode gritar.

Dois itens ainda a acertar contra o arquivo original:

- `--vermelho` foi estimado a olho a partir da imagem da logo. O hexagono tem
  gradiente (faceta clara e faceta escura); o valor escolhido fica no meio.
  Se houver manual de marca com o HEX exato, trocar o token.
- O wordmark do header e uma **reproducao tipografica em Poppins**, com um
  hexagono SVG simples ao lado. Nao e a logo. Colocar o arquivo oficial em
  `assets/img/logo-primor.svg` e trocar o bloco `.marca` por um `<img>`.

## Logo

**O header e o rodape ainda NAO usam a logo da PRIMOR.** Usam um wordmark
provisorio: "PRIMOR / EMPREENDIMENTOS" em Poppins com um hexagono SVG liso ao
lado. Nao e a marca — o hexagono real tem monograma P+E isometrico, facetas 3D
e gradiente, e refazer isso a mao sai parecido, nao igual.
`tools/checar_pendencias.sh` bloqueia a publicacao enquanto o arquivo faltar.

Para resolver, colocar o arquivo em `assets/img/logo-primor.svg` (SVG de
preferencia; PNG com fundo transparente e no minimo 600 px de largura serve) e,
em `index.html`, `paraiso-da-enseada/index.html` e `paraiso-da-lagoa/index.html`,
trocar os dois blocos `.marca` (um no header, um no rodape) por:

```html
<a class="marca" href="/">
  <img src="/assets/img/logo-primor.svg" alt="PRIMOR Empreendimentos" width="150" height="44">
</a>
```

No rodape, sobre fundo preto, usar a versao invertida da logo se existir
(`logo-primor-branca.svg`). O wordmark da logo e preto; sobre o rodape preto
ele some.

## Regra inegociavel das vitrines

`/paraiso-da-enseada/` e `/paraiso-da-lagoa/` sao empreendimentos **entregues e
100% comercializados**. Essas paginas nao podem, em nenhuma hipotese:

- exibir preco, plano de pagamento ou tabela de disponibilidade;
- ter formulario de lead ou botao de WhatsApp;
- usar linguagem de oferta ("agende sua visita", "unidades disponiveis").

Cada pagina carrega um selo "Entregue AAAA · 100% comercializado" no hero e uma
faixa vermelha de aviso logo abaixo. Ausencia de preco nao comunica nada por si
so; o selo e a faixa comunicam. O unico CTA aponta de volta para o Ilha Bela.

`tools/checar_pendencias.sh` verifica isso automaticamente.

## Antes de publicar

```bash
bash tools/checar_pendencias.sh
```

Sai com erro enquanto houver `class="pendente"` em qualquer pagina, WhatsApp
numa vitrine, linguagem de oferta, ou nome de arquivo servido na web com
maiuscula/acento. Hoje **bloqueia de proposito**.

## Dados confirmados

| | Paraiso da Enseada | Paraiso da Lagoa | Ilha Bela |
|---|---|---|---|
| Situacao | Entregue | Entregue | Em vendas |
| Entrega | 2018 | 2021 | Fase 02 em 2027 |
| Unidades | 16 | 32 | — |
| Local | Itacimirim — BA | Itacimirim — BA | Itacimirim — BA |

PRIMOR fundada em 2015. **48 unidades entregues** (16 + 32), ambos os
condominios integralmente comercializados.

A localizacao de Enseada e Lagoa vem dos proprios depoimentos, em que os
compradores nomeiam Itacimirim. Vale uma conferida, mas e fonte primaria.

## Depoimentos

Tres depoimentos de proprietarios, transcritos dos prints de WhatsApp. Aparecem
na home e na pagina do respectivo empreendimento.

| Autor | Empreendimento |
|---|---|
| Ciro | Paraiso da Enseada |
| Jairo e Rosana | Paraiso da Lagoa |
| Philipe Ralejo | Paraiso da Lagoa |

O texto foi mantido como escrito, com apenas tres correcoes ortograficas:
`vilages` → `villages`, `proprietario ... está sempre` → `estar sempre`,
`á parte` → `a parte`. Nenhuma frase foi reescrita, cortada ou reordenada.
Se preferir o texto 100% literal, e so reverter essas tres.

Sobrenomes de Ciro e de Jairo e Rosana nao aparecem nos prints — estao marcados
como pendentes. Um depoimento so com primeiro nome vale menos como prova.

## Fotos — o que falta

As 19 fotos da Enseada e as 14 da Lagoa estao no Drive, nas pastas
`Paraíso da Enseada` e `Paraíso da Lagoa`. **Elas nao podem ser trazidas para ca
por este ambiente**: `drive.google.com` esta bloqueado pela politica de rede da
sessao, e o conector do Drive devolve o arquivo como base64 dentro da conversa —
33 PNGs de 3 a 13 MB nao cabem.

**Anexar no chat tambem nao funciona.** Imagem colada na conversa nao vira
arquivo no disco do ambiente: da para olhar, nao para converter nem commitar.

O unico caminho que funciona e **subir os arquivos para este repositorio**, na
branch `claude/primor-site-institucional-wtw8l9`:

1. Baixar as duas pastas do Drive como `.zip` e descompactar no computador.
2. No GitHub, abrir o repositorio na branch acima.
3. `Add file` > `Upload files`, arrastar as fotos da Enseada para
   `paraiso-da-enseada/originais/`.
4. Commitar, e repetir para `paraiso-da-lagoa/originais/`.
5. Avisar aqui. Eu processo, converto e monto a galeria.

Uma pasta por vez: a interface web do GitHub falha em silencio acima de ~100
arquivos e as vezes achata a estrutura de pastas. Sao 19 + 14, entao dois
envios resolvem. Conferir a lista de arquivos resultante antes de seguir.

Com os arquivos em maos:

```bash
pip install Pillow
python3 tools/folha_de_contato.py Paraiso_da_Enseada.zip paraiso-da-enseada
python3 tools/folha_de_contato.py Paraiso_da_lagoa.zip   paraiso-da-lagoa
```

Gera em cada pasta:

| Arquivo | Para que serve |
|---|---|
| `folha-de-contato.jpg` | grade numerada, para mandar no WhatsApp |
| `folha-de-contato.html` | mesma grade, para abrir no navegador |
| `catalogo.csv` | preencher a coluna `area_ou_ambiente` de cada numero |
| `fotos/NNN.webp` | foto do lightbox (max 1600px, q80) |
| `fotos/NNN-thumb.webp` | miniatura do card (max 520px, q78) |

### As fotos sao screenshots

Os arquivos do Drive sao screenshots de celular: a foto ocupa uma faixa no meio
e o resto e tarja preta, com a barra do indicador de home do iOS no rodape. O
`folha_de_contato.py` detecta e corta essas tarjas automaticamente e avisa no
relatorio quais fotos cortou.

Cortar tarja nao devolve resolucao. O que sobra e a faixa de foto no tamanho da
tela, nao o arquivo do fotografo. **Se a pasta dos originais existir, ela vale
muito mais** — sobretudo para o hero e o lightbox. Vale procurar antes de
processar os screenshots.

Nunca presumir a qual area cada foto pertence. Ja deu errado antes (planta baixa
dentro da galeria de piscina). Com o `catalogo.csv` preenchido, preencher a
constante `window.FOTOS` no fim do `index.html` de cada vitrine. Enquanto
estiver vazia, a galeria mostra um aviso amarelo em vez de fingir que esta pronta.

## Outros dados que faltam confirmar

Todos destacados em amarelo nas paginas (`class="pendente"`).

- Razao social da imobiliaria responsavel pela comercializacao
- Instagram / redes da PRIMOR
- Sobrenomes de Ciro e de Jairo e Rosana
- 1 paragrafo sobre padrao construtivo (home) e 2-3 por empreendimento entregue
- Foto para o `og:image` de cada pagina (1200x630, foto real, nao a logo)
- Arquivo da logo oficial (ver secao "Logo")
- **Numero do registro de incorporacao do Ilha Bela e cartorio competente**

CNPJ aplicado no rodape: **36.490.400/0002-50** (digito verificador confere).
E um estabelecimento **filial** (ordem `0002`), nao a matriz `0001`. Se a
incorporadora destes empreendimentos for a matriz, trocar.

## Nota juridica: registro de incorporacao

A Lei 4.591/64, art. 32, §3º exige que o numero do registro da incorporacao e o
cartorio competente constem **obrigatoriamente de anuncios, impressos e
publicacoes** referentes a incorporacao. Isso alcanca o **Ilha Bela**, que tem
Fase 02 em obra com entrega em 2027 — o empreendimento que de fato e anunciado
e vendido. Enseada e Lagoa, ja concluidos e comercializados, nao estao nessa
hipotese.

O rodape ja tem o campo reservado. Confirmar o numero com a PRIMOR antes de
tirar o marcador amarelo.

## Sobre a migracao do Ilha Bela

O site do Ilha Bela (`eduardocorreia344-cell/ilhabela`) **ainda nao foi movido**
para `/ilhabela/`. Os links da home ja apontam para esse caminho, entao hoje
eles quebram — e intencional: e o unico item pendente que aparece na navegacao.

A recomendacao e migrar apenas junto com a compra do dominio proprio, em um
movimento so com os redirects. Enquanto o endereco for `.vercel.app`, nao ha
ganho de SEO em consolidar (cada `*.vercel.app` e tratado como site
independente — o dominio esta na Public Suffix List), e mover o unico ativo que
gera receita, com campanhas apontando para ele, e risco sem retorno.

Se a decisao for migrar agora, os links da home ja estao prontos. Se for
esperar, trocar os `href="/ilhabela/"` por `https://ilhabela.vercel.app/` com
`target="_blank"` e `rel="noopener"`.
