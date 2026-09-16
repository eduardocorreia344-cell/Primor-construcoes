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

Caminho que funciona: baixar as duas pastas como `.zip` e anexar no chat, ou
subir os arquivos direto no repositorio.

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

Nunca presumir a qual area cada foto pertence. Ja deu errado antes (planta baixa
dentro da galeria de piscina). Com o `catalogo.csv` preenchido, preencher a
constante `window.FOTOS` no fim do `index.html` de cada vitrine. Enquanto
estiver vazia, a galeria mostra um aviso amarelo em vez de fingir que esta pronta.

## Outros dados que faltam confirmar

Todos destacados em amarelo nas paginas (`class="pendente"`).

- CNPJ da PRIMOR Empreendimentos
- Razao social da imobiliaria responsavel pela comercializacao
- Instagram / redes da PRIMOR
- Sobrenomes de Ciro e de Jairo e Rosana
- 1 paragrafo sobre padrao construtivo (home) e 2-3 por empreendimento entregue
- Foto para o `og:image` de cada pagina (1200x630, foto real, nao a logo)
- **Numero do registro de incorporacao do Ilha Bela e cartorio competente**

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
