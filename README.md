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
| `assets/img/favicon-32.png` e `-180.png` | icone da aba, recortado do hexagono |

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

## Dominio

O site e servido em **www.primorconstrucoes.com.br**, que e o host
canonico. O apex `primorconstrucoes.com.br` redireciona para ele.

Essa direcao e o padrao do Vercel ("Redirect apex domains to www") e tem
motivo tecnico: o apex nao pode ser um CNAME por limitacao de DNS, entao
depende de um registro A com IP fixo. Servindo pelo `www`, que e CNAME, uma
eventual mudanca de IP do Vercel nao derruba o site — no maximo o
redirecionamento do apex. Quem decide a direcao e a configuracao de dominios
do Vercel, nao o `vercel.json`.

Todo `canonical`, `og:url`, `og:image` e o JSON-LD apontam para o dominio.
`tools/checar_pendencias.sh` falha se uma URL de `vercel.app` voltar ao HTML:
canonical apontando para o endereco temporario faz o Google consolidar nele
em vez de no dominio, que e o oposto do motivo de ter comprado o dominio.

`sitemap.xml` lista as tres paginas proprias. `/ilhabela/` fica fora de
proposito — e um rewrite da landing do empreendimento, que declara canonical
para o dominio dela.

## Formulario de cadastro

Secao `#cadastro` na home: "Cadastre-se e receba novidades dos proximos
empreendimentos". Nome, e-mail, WhatsApp opcional e consentimento.

Os cadastros vao para o **Formspree**, configurado em
`window.CADASTRO_ENDPOINT` no `index.html`. O identificador do formulario e
publico por natureza — ele vive no HTML e e o que o navegador chama. Quem
protege contra spam e a armadilha em `formulario.js` mais o filtro do
proprio Formspree.

Para trocar de servico (Basin, Web3Forms) basta trocar esse endereco: o
formulario envia `FormData` com `Accept: application/json`, que e o formato
que todos eles aceitam.

`tools/checar_pendencias.sh` bloqueia a publicacao se o endereco voltar a
ficar vazio. Nesse estado o formulario recusa o envio com mensagem clara,
em vez de fingir sucesso e perder o cadastro.

**Os testes nunca tocam o servico real.** `tools/testa_formulario.py` aborta
qualquer requisicao para `formspree.io` e simula o cenario de destino vazio
em vez de herda-lo da pagina — sem isso, cada rodada de teste geraria
cadastro de mentira na caixa de entrada.

### O que o formulario ja faz

- **Validacao antes de enviar**: nome com 2 ou mais caracteres, e-mail com
  formato plausivel, consentimento marcado. Campo invalido ganha borda
  vermelha, mensagem propria e recebe o foco.
- **Armadilha de robo** (*honeypot*): um campo escondido fora da tela, com
  `tabindex="-1"`. Pessoa nenhuma preenche; robo de spam preenche quase
  sempre. Preenchido, a tela responde como sucesso e nada e enviado.
  Fica fora da tela em vez de `display: none`, que parte dos robos detecta.
- **Estados visiveis**: enviando, sucesso e erro, num `aria-live` para
  leitor de tela anunciar. Em erro o formulario **nao** e limpo, para nao
  obrigar a redigitar.
- **Consentimento explicito** com texto de finalidade e direito de remocao,
  como manda a LGPD. Quem recebe os dados precisa honrar o pedido de
  remocao — isso e processo, nao codigo.

`tools/testa_formulario.py` cobre os oito cenarios: envio vazio, e-mail
malformado, falta de consentimento, destino vazio, envio bem-sucedido, erro
do servidor, armadilha de robo e o campo escondido fora do alcance do
teclado.

## Movimento

Tudo depende da classe `.motion` no `<html>`, posta por um script inline no
`<head>`. **Sem JavaScript a classe nunca entra e a pagina aparece inteira,
estatica** — nunca em branco esperando um script que falhou.

| O que | Onde | Termo |
|---|---|---|
| Entrada no scroll | `motion.js` + `primor.css` | IntersectionObserver |
| Header que encolhe (104 -> 72 px) | `motion.js` + `primor.css` | shrink-on-scroll |
| Zoom lento na capa das vitrines | `vitrine.css` | Ken Burns |
| Transicao entre paginas | `@view-transition` em `primor.css` | View Transitions API |
| Miniatura que vira foto no lightbox | `galeria.js` | shared element transition |
| Legenda da galeria no hover | `vitrine.css` | so em `@media (hover: hover)` |

Peso somado: **36 KB**, sem nenhuma biblioteca.

### Regras que o codigo segue

- **`prefers-reduced-motion`**: desliga tudo. A variavel `--rv-opacidade` e
  herdada da raiz, entao o grupo inteiro nasce visivel sem repetir a lista de
  seletores nem usar `!important` — que quebraria transforms legitimos.
- **So `transform` e `opacity`** nas animacoes de lista. A unica excecao e a
  altura do header, documentada no CSS: e um elemento so, uma vez por mudanca
  de direcao do scroll, e nao ha como falsear com transform sem deixar uma
  faixa vazia.
- **Nada animado acima da dobra.** O que ja esta na tela ao abrir aparece sem
  animar. Medido: LCP 420 ms na home e 456 ms na vitrine, CLS 0.
- **`:where()` na lista de seletores.** Sem isso `.motion .secao .filete`
  (0,3,0) venceria `.motion .visivel` (0,2,0) e o elemento receberia a classe
  mas continuaria invisivel.
- **Varredura de seguranca.** O IntersectionObserver so avisa quando o estado
  de intersecao MUDA. Num salto — link de ancora, recarregar no meio da
  pagina — o elemento vai de "abaixo da tela" direto para "acima" sem nunca
  intersectar, e o conteudo ficaria preso invisivel. Uma varredura limitada ao
  que falta, no maximo a cada 250 ms, cobre o caso.
- **Sem `backdrop-filter` no header.** Com a altura animando, o blur recompoe
  a cada quadro e deixa um fantasma da logo no tamanho antigo.

### Testes

`tools/testa_movimento.py` cobre, nas tres paginas: salto instantaneo ao fim,
scroll gradual, header encolhendo e voltando, ausencia de erro de JavaScript,
pagina sem JavaScript e `prefers-reduced-motion`. Criterio: **nenhum elemento
pode ficar com `opacity: 0`** ao fim de cada cenario.

```bash
python3 -m http.server 8099 &
python3 tools/testa_movimento.py
```

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

### Unidades entregues

| Empreendimento | Unidades | Situacao |
|---|---|---|
| Paraiso da Enseada | 16 | Entregue em 2018, 100% vendido desde 2020 |
| Paraiso da Lagoa | 32 | Entregue em 2021, 100% vendido |
| Ilha Bela — Fase 01 | 60 | Entregue em 2026, quase 100% vendida (4 disponiveis) |
| **Total entregue** | **108** | |
| Ilha Bela — Fase 02 | — | Em obras, entrega abril/2027, disponivel |

As 4 unidades ainda disponiveis da Fase 01 **nao** aparecem no site. Numero
de escassez so funciona se for mantido atualizado; desatualizado, vira o
oposto. A linha do tempo diz "quase 100% vendida", que continua verdadeiro
sem depender de manutencao.

### O que ainda pode melhorar

- Razao social da imobiliaria responsavel pela comercializacao
- Originais em alta das fotos da galeria: as do Drive sao screenshots de 1170 px
- Capa do card do Ilha Bela: e a logo oficial do empreendimento, a pedido.
  A fonte tem 696 px, entao ela sobe cerca de 1,3x na tela; um arquivo
  maior deixaria mais nitido. Foto do empreendimento converteria mais
  que logo, mas a escolha e do Gabriel.
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

## /ilhabela/ — como esta ligado

`vercel.json` faz um **rewrite** de `/ilhabela/` para
`https://ilhabela-one.vercel.app`. Rewrite nao e redirecionamento: a URL na
barra continua sendo a da PRIMOR e o Vercel busca o conteudo do outro projeto
por tras. O visitante nao sai do dominio.

```json
{ "source": "/ilhabela/:caminho*",
  "destination": "https://ilhabela-one.vercel.app/:caminho*" }
```

Funciona porque a landing do Ilha Bela usa **so caminhos relativos**
(`hero.jpg`, `frame-000.jpg`) — verificado no repositorio
`eduardocorreia344-cell/ilhabela`: zero `src="/..."`, zero `href="/..."`,
zero fetch com caminho absoluto. Fosse com caminho absoluto, o navegador
pediria `primor.../hero.jpg`, que a regra nao pega, e a pagina viria sem
imagem nem estilo. `trailingSlash: true` garante que `/ilhabela` vire
`/ilhabela/` antes do rewrite, o que e o que faz o caminho relativo resolver
para dentro da pasta.

**Nao deu para testar daqui**: a politica de rede desta sessao recusa
`vercel.app`, e rewrite so existe no Vercel de verdade. A configuracao esta
correta na sintaxe e coerente com a estrutura da landing, mas quem confirma
e o deploy.

### O dominio proprio do Ilha Bela

A landing declara `<link rel="canonical" href="https://www.ilhabelaitacimirim.com.br/">`.
Existe dominio proprio para o empreendimento. Isso contradiz a premissa das
recomendacoes anteriores deste arquivo, que assumiam so `.vercel.app`.

Com o rewrite, a mesma pagina passa a existir em tres enderecos. Nao gera
penalidade, porque o canonical dentro dela aponta para o `.com.br` e o Google
consolida tudo la — mas tambem significa que o caminho na PRIMOR nao acumula
nada de SEO, so serve a experiencia de nao tirar o visitante do dominio.

Se a preferencia for mandar o visitante para o endereco proprio do
empreendimento, e trocar o rewrite por link externo: apagar o bloco
`rewrites` do `vercel.json` e trocar `href="/ilhabela/"` por
`href="https://www.ilhabelaitacimirim.com.br/"` com `target="_blank"` e
`rel="noopener"` nos tres arquivos HTML.

### Cache

Os nomes de arquivo do site nao carregam hash de conteudo: `capa-ilhabela.webp`
continua `capa-ilhabela.webp` depois de trocada. O `Cache-Control` era
`immutable` por um ano, o que faria quem ja tivesse visitado continuar vendo a
versao antiga por um ano. Trocado por `max-age=86400, must-revalidate`: um dia
de cache e depois revalidacao por ETag, que devolve 304 quando nada mudou.

## Historico: a decisao de nao copiar o Ilha Bela para dentro do repo

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
