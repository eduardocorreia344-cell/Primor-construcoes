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

O arquivo oficial entrou como `assets/img/originais/logo-primor.png`
(2048x2048, fundo branco, sem alpha). `tools/prepara_logo.py` deriva dele:

| Arquivo | Uso |
|---|---|
| `assets/img/logo-primor.webp` | header, fundo claro |
| `assets/img/logo-primor-branca.webp` | rodape, fundo preto |

O script tira o matte branco (alpha pelo afastamento do branco, desfazendo a
composicao), recorta no conteudo e reduz para 400 px. A versao branca clareia
so os pixels sem cor — o wordmark preto e o "EMPREENDIMENTOS" cinza — e
preserva o hexagono vermelho. O "EMPREENDIMENTOS" sai do fundo branco com
alpha baixo, entao leva uma gama no alpha para nao virar cinza escuro sobre o
rodape.

Para trocar por um vetor, colocar o novo arquivo em `assets/img/originais/` e
rodar o script de novo. Se houver SVG, melhor ainda: apontar as tags `<img>`
para ele e dispensar o script.

**O header tem 104 px de altura por causa da logo.** O lockup e quadrado (o
hexagono fica acima do wordmark), entao num header de 70 px ele caberia com
~55 px de largura e o "PRIMOR" viraria borrao. A 76 px de altura fica legivel.
Se um dia existir uma versao horizontal do lockup (hexagono a esquerda do
wordmark), o header pode voltar a ser baixo.

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

## Fotos — processadas

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

## Estado

`tools/checar_pendencias.sh` passa limpo: nao ha mais nenhum `class="pendente"`
nas paginas. Todo o conteudo esta preenchido com dado confirmado.

### Correcao de localizacao

Os textos institucionais chegaram com "Itacimirim em Salvador" (Enseada) e
"Itacimirim SA" (Lagoa). Itacimirim e distrito de **Camacari**, nao de
Salvador, e e o que o resto do site ja dizia. Publicado como
"Itacimirim, Camacari".

### Acentuacao

O texto do site foi escrito sem acento na primeira versao, por cautela com
encoding que nao se justificava: as paginas sao utf-8 e sempre foram. Um site
em portugues com "Paraiso" e "incorporacao" le como quebrado. Todo o texto
visivel foi acentuado — incluindo `alt`, `title`, meta description, Open Graph
e JSON-LD. Os caminhos de arquivo continuam sem acento, como manda a regra de
case-sensitivity.

O filtro de linguagem de oferta do `checar_pendencias.sh` tambem foi acentuado:
ele excluia "nao ha unidades disponiveis" sem acento e passou a acusar falso
positivo quando o texto ganhou acento.

### O que ainda pode melhorar

- Razao social da imobiliaria responsavel pela comercializacao
- Originais em alta das fotos da galeria: as do Drive sao screenshots de 1170 px
- Capa do card do Ilha Bela: hoje e a logo, a pedido; foto converte mais
- Versao horizontal do lockup da logo, que permitiria um header mais baixo
- CNPJ das SPEs do Paraiso da Enseada e do Paraiso da Lagoa, se existirem

## Razao social e o que foi para cada rodape

`Ilhabela Empreendimentos SPE LTDA`, CNPJ `36.490.400/0002-50` (digito
verificador confere; ordem `0002`, um estabelecimento filial).

SPE e Sociedade de Proposito Especifico: existe para um empreendimento. Esta e
a do **Ilha Bela**. Por isso:

- **Home**: a linha nomeia o empreendimento — "Ilha Bela Itacimirim Villages —
  incorporacao: Ilhabela Empreendimentos SPE LTDA, CNPJ ..." — mais o CRECI da
  comercializacao.
- **Enseada e Lagoa**: so "PRIMOR Empreendimentos". Atribuir a SPE do Ilha Bela
  a empreendimentos de 2018 e 2021 seria errado, e nao ha CRECI a declarar numa
  pagina que nao oferta nada.

Se cada entregue tiver a propria SPE, os CNPJs entram nesses dois rodapes.

## Registro de incorporacao

Publicado **sem** o numero do registro e o cartorio, por decisao do Gabriel.

Fica o registro do motivo de isso ter sido levantado: a Lei 4.591/64, art. 32,
§3º exige que o numero do registro da incorporacao e o cartorio competente
constem de anuncios, impressos e publicacoes referentes a incorporacao, e o
Ilha Bela tem Fase 02 em obra. Enseada e Lagoa, concluidos, nao entram nessa
hipotese. Quando o numero chegar, o lugar e o rodape da home, junto da linha da
SPE.

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
