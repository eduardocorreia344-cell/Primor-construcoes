#!/usr/bin/env bash
# Trava de publicacao: nenhuma pagina com marcador "pendente" pode ir ao ar.
# Uso: bash tools/checar_pendencias.sh
set -uo pipefail
cd "$(dirname "$0")/.."

falhou=0

echo "== Marcadores de dado nao confirmado =="
if grep -rn --include="*.html" 'class="pendente"' . | grep -v '^./tools/'; then
  falhou=1
else
  echo "  nenhum. ok"
fi

echo
echo "== WhatsApp indevido nas vitrines (Enseada / Lagoa) =="
if grep -rn "wa.me" paraiso-da-enseada paraiso-da-lagoa 2>/dev/null; then
  echo "  ERRO: vitrine de empreendimento entregue nao pode ter WhatsApp."
  falhou=1
else
  echo "  nenhum. ok"
fi

echo
echo "== Termos de oferta nas vitrines =="
if grep -rniE "a partir de R\\\$|entrada de|parcelas de|unidades dispon|agende (sua )?visita|simule" \
    paraiso-da-enseada paraiso-da-lagoa 2>/dev/null \
    | grep -viE "n(ã|a)o h(á|a) unidades|n(ã|a)o constitui|integralmente comercializado"; then
  echo "  ERRO: linguagem de oferta em pagina de empreendimento entregue."
  falhou=1
else
  echo "  nenhum. ok"
fi

echo
echo "== Endereco canonico aponta para o dominio proprio =="
# O canonico e www.primorconstrucoes.com.br, que e o padrao do Vercel
# (apex redireciona para www). Uma pagina apontando para o host sem www
# teria canonical para uma URL que redireciona, e o Google pode ignora-lo.
if grep -rn 'https://primorconstrucoes\.com\.br' --include="*.html" --include="*.xml" --include="*.txt" .; then
  echo "  ERRO: canonical sem www. O host canonico e www.primorconstrucoes.com.br."
  falhou=1
fi
if grep -rn 'vercel\.app' --include="*.html" . | grep -v 'ilhabela-one'; then
  echo "  ERRO: ha URL de vercel.app no HTML. Canonical e Open Graph precisam"
  echo "  apontar para primorconstrucoes.com.br, senao o Google consolida o"
  echo "  endereco temporario em vez do dominio."
  falhou=1
else
  echo "  nenhuma. ok"
fi

echo
echo "== Destino do formulario de cadastro =="
if grep -q 'window.CADASTRO_ENDPOINT = ""' index.html; then
  echo "  ERRO: window.CADASTRO_ENDPOINT esta vazio em index.html."
  echo "  O formulario recusa o envio nesse estado. Ver 'Formulario de"
  echo "  cadastro' no README para configurar em poucos minutos."
  falhou=1
else
  echo "  configurado. ok"
fi

echo
echo "== Logo oficial da PRIMOR =="
if ls assets/img/logo-primor.* >/dev/null 2>&1; then
  echo "  presente. ok"
else
  echo "  ERRO: assets/img/logo-primor.(svg|png) nao existe."
  echo "  O header e o rodape ainda usam o wordmark provisorio em Poppins,"
  echo "  que NAO e a logo da marca. Ver 'Logo' no README."
  falhou=1
fi

echo
echo "== Nomes de arquivo com maiuscula, espaco ou acento =="
# So arquivos servidos na web. README.md, LICENSE etc. sao meta do repo.
if find . \( -path ./.git -o -name originais \) -prune -o -type f \
     \( -name '*.html' -o -name '*.css' -o -name '*.js' -o -name '*.webp' \
        -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' -o -name '*.svg' \
        -o -name '*.mp4' -o -name '*.woff2' \) -print \
   | grep -P '[A-Z ]|[^\x00-\x7F]'; then
  echo "  ERRO: renomear para minusculo-sem-acento (case-sensitivity no Vercel)."
  falhou=1
else
  echo "  nenhum. ok"
fi

echo
if [ "$falhou" -eq 0 ]; then
  echo "TUDO LIMPO — pode publicar."
else
  echo "BLOQUEADO — resolva os itens acima antes de publicar."
fi
exit "$falhou"
