#!/bin/bash
# Yeni Superset workspace'ini hazırlar. İdempotent — tekrar çalıştırmak güvenli.
set -euo pipefail

ROOT="${SUPERSET_ROOT_PATH:?SUPERSET_ROOT_PATH tanımlı değil}"
WS="${SUPERSET_WORKSPACE_PATH:-$(pwd)}"
cd "$WS"

# Bağımlılık yok: site statik HTML, sunucu ve baskı scriptleri sadece python3 stdlib.
command -v python3 >/dev/null || { echo "python3 bulunamadı" >&2; exit 1; }

# Git'te olmayan yerel dosyaları ana checkout'tan kopyala (varsa, üzerine yazmadan).
if [ "$ROOT" != "$WS" ]; then
  for f in .env .env.local .claude/settings.local.json; do
    if [ -f "$ROOT/$f" ] && [ ! -e "$WS/$f" ]; then
      mkdir -p "$(dirname "$WS/$f")"
      cp "$ROOT/$f" "$WS/$f"
      echo "kopyalandı: $f"
    fi
  done
fi

PORT="$(python3 .superset/port.py allocate)"
echo "Dev server portu: $PORT  (Run → http://localhost:$PORT)"
