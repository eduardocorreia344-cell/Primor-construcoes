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
    | grep -viE "n[ao]o h[ao] unidades|n[ao]o constitui|integralmente comercializado"; then
  echo "  ERRO: linguagem de oferta em pagina de empreendimento entregue."
  falhou=1
else
  echo "  nenhum. ok"
fi

echo
echo "== Nomes de arquivo com maiuscula, espaco ou acento =="
if find . -path ./.git -prune -o -print | grep -P '[A-Z ]|[^\x00-\x7F]' | grep -v '^./tools/'; then
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
