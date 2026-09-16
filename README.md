# Site institucional PRIMOR Empreendimentos

Site estatico, um repositorio, um projeto Vercel. Sem build: e HTML/CSS/JS puro.

## Estrutura

```
/                      index.html         Home institucional PRIMOR          [construida]
/paraiso-da-enseada/   index.html         Vitrine institucional              [estrutura pronta, sem fotos]
/paraiso-da-lagoa/     index.html         Vitrine institucional              [estrutura pronta, sem fotos]
/ilhabela/             —                  Site de vendas                     [NAO migrado — ver abaixo]
/assets/css/primor.css                    Tokens + header + rodape compartilhados
/assets/css/vitrine.css                   Estilos das paginas de entregues
/assets/js/galeria.js                     Galeria + lightbox
/tools/                                   Scripts de apoio
```

## Regra inegociavel das vitrines

`/paraiso-da-enseada/` e `/paraiso-da-lagoa/` sao empreendimentos **entregues e
100% comercializados**. Essas paginas nao podem, em nenhuma hipotese:

- exibir preco, plano de pagamento ou tabela de disponibilidade;
- ter formulario de lead ou botao de WhatsApp;
- usar linguagem de oferta ("agende sua visita", "unidades disponiveis").

Cada pagina carrega um **selo visivel** de "Entregue · 100% comercializado" no
hero e uma faixa juridica logo abaixo. Ausencia de preco nao comunica nada por
si so; o selo comunica. O unico CTA aponta de volta para o Ilha Bela.

`tools/checar_pendencias.sh` verifica isso automaticamente.

## Antes de publicar

```bash
bash tools/checar_pendencias.sh
```

Sai com erro enquanto houver `class="pendente"` em qualquer pagina, WhatsApp
numa vitrine, linguagem de oferta, ou nome de arquivo com maiuscula/acento.
Hoje **bloqueia de proposito**: falta confirmar os dados listados abaixo.

## Fluxo das fotos (obrigatorio — nao pular)

Nunca presumir a qual area do empreendimento cada foto pertence. Ja deu errado
antes (planta baixa dentro da galeria de piscina).

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

Com o `catalogo.csv` preenchido, preencher a constante `window.FOTOS` no final
do `index.html` de cada vitrine. Enquanto estiver vazia, a galeria mostra um
aviso amarelo em vez de fingir que esta pronta.

## Dados que faltam confirmar

Todos aparecem destacados em amarelo nas paginas (`class="pendente"`).

**Institucional**
- CNPJ da PRIMOR Empreendimentos
- Razao social da imobiliaria responsavel pela comercializacao
- Instagram / redes da PRIMOR
- 2-3 paragrafos institucionais sobre a incorporadora
- Foto para o `og:image` da home (1200x630, foto real, nao a logo)

**Juridico (prioritario — ver nota abaixo)**
- Numero do registro de incorporacao do Ilha Bela e cartorio competente

**Paraiso da Enseada e Paraiso da Lagoa (cada um)**
- Cidade / bairro
- Ano de entrega
- Numero de unidades
- 2-3 paragrafos sobre o projeto
- Catalogacao das fotos

## Nota juridica: registro de incorporacao

A Lei 4.591/64, art. 32, §3º exige que o numero do registro da incorporacao e o
cartorio competente constem **obrigatoriamente de anuncios, impressos e
publicacoes** referentes a incorporacao. Isso alcanca o **Ilha Bela**, que tem
Fase 02 em obra com entrega em 2027 — ou seja, o empreendimento que de fato e
anunciado e vendido. Enseada e Lagoa, ja concluidos e comercializados, nao
estao nessa hipotese.

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
`target="_blank"` e um `rel="noopener"`.
