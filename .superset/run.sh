#!/bin/bash
# Statik menüyü workspace'e ayrılmış portta sunar.
set -euo pipefail
cd "${SUPERSET_WORKSPACE_PATH:-$(pwd)}"

PORT="$(python3 .superset/port.py get)"
echo "SOWA menü → http://localhost:$PORT/sowa-qr-menu/"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
