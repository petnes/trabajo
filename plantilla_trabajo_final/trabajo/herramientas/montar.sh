#!/bin/bash
# Regenera trabajo/final/Ibanez_Esteban_Aritz_TFM.docx a partir del borrador y de trabajo/apartados.
# Uso (desde la carpeta plantilla_trabajo_final):  bash trabajo/herramientas/montar.sh
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
H="$ROOT/trabajo/herramientas"
TMP="$(mktemp -d)"
OUT="$ROOT/trabajo/final/Ibanez_Esteban_Aritz_TFM.docx"
mkdir -p "$ROOT/trabajo/final"
python3 -I "$H/assemble.py" "$ROOT/material/Ibanez_Esteban_Aritz_Borrador_3.docx" "$TMP/build.docx" "$ROOT/trabajo/apartados"
soffice --headless --convert-to pdf --outdir "$TMP" "$TMP/build.docx" >/dev/null 2>&1
python3 -I "$H/toc_update.py" "$TMP/build.docx" "$TMP/build.pdf"
rm -f "$TMP/build.pdf"
soffice --headless --convert-to pdf --outdir "$TMP" "$TMP/build.docx" >/dev/null 2>&1
pdfinfo "$TMP/build.pdf" | grep Pages
python3 -I "$H/validate_order.py" "$TMP/build.docx"
python3 -I "$H/check_style.py" "$TMP/build.docx"
cp "$TMP/build.docx" "$OUT"
echo "Word final: $OUT"
