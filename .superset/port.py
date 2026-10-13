#!/usr/bin/env python3
"""Workspace başına dev-server portu ayırır.

Paralel Superset workspace'leri aynı portta çakışmasın diye her workspace'e
~/.superset/port-allocations.json içinde kalıcı bir port kiralanır.

  port.py allocate   → portu ayır (varsa mevcut olanı ver), stdout'a yaz
  port.py get        → ayrılmış portu yaz; yoksa allocate gibi davranır
  port.py release    → kirayı bırak
"""
import fcntl, json, os, pathlib, socket, sys

BASE, LIMIT = 8100, 8199
DOSYA = pathlib.Path.home() / ".superset" / "port-allocations.json"
ANAHTAR = os.environ.get("SUPERSET_WORKSPACE_PATH") or os.getcwd()


def bos_mu(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def main(komut):
    DOSYA.parent.mkdir(parents=True, exist_ok=True)
    with open(DOSYA, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        try:
            kiralar = json.loads(f.read() or "{}")
        except json.JSONDecodeError:
            kiralar = {}
        # Silinmiş worktree'lerin kiralarını temizle
        kiralar = {k: v for k, v in kiralar.items() if os.path.isdir(k)}

        if komut == "release":
            kiralar.pop(ANAHTAR, None)
            port = None
        else:
            port = kiralar.get(ANAHTAR)
            if port is None or (komut == "allocate" and not bos_mu(port)):
                dolu = set(kiralar.values())
                port = next((p for p in range(BASE, LIMIT + 1)
                             if p not in dolu and bos_mu(p)), None)
                if port is None:
                    sys.exit(f"{BASE}-{LIMIT} aralığında boş port yok")
                kiralar[ANAHTAR] = port

        f.seek(0)
        f.truncate()
        json.dump(kiralar, f, indent=2, sort_keys=True)
    if port is not None:
        print(port)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("allocate", "get", "release"):
        sys.exit(__doc__)
    main(sys.argv[1])
