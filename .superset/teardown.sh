#!/bin/bash
# Workspace silinirken: bu workspace'in dev server'ını durdur, port kirasını bırak.
set -uo pipefail
cd "${SUPERSET_WORKSPACE_PATH:-$(pwd)}"

PORT="$(python3 .superset/port.py get 2>/dev/null || true)"
if [ -n "$PORT" ]; then
  for pid in $(lsof -ti "tcp:$PORT" -sTCP:LISTEN 2>/dev/null); do
    # Sadece bizim başlattığımız sunucuyu öldür
    if ps -o command= -p "$pid" | grep -q "http.server $PORT"; then
      kill "$pid" 2>/dev/null && echo "durduruldu: http.server (pid $pid, port $PORT)"
    fi
  done
fi

python3 .superset/port.py release
exit 0
