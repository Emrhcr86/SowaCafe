#!/bin/bash
# SOWA baskı menüsü → PDF. Önce: python3 print/olustur.py
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
D="$(cd "$(dirname "$0")" && pwd)"
for f in menu-a4-2sutun menu-a5-cift-tarafli menu-a4-tek-sutun; do
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --virtual-time-budget=8000 \
    --print-to-pdf="$D/$f.pdf" "file://$D/$f.html" 2>/dev/null
  echo "PDF: $f.pdf"
done
