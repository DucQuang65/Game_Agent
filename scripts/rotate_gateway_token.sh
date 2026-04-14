#!/bin/bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OPENCLAW_LOG_FILE="$PROJECT_ROOT/Openclaw.txt"

if ! command -v openclaw >/dev/null 2>&1; then
    echo "[ERROR] openclaw command not found in PATH"
    exit 1
fi

echo "[INFO] Rotating OpenClaw gateway token..."
openclaw doctor --generate-gateway-token

echo "[INFO] Current gateway token:"
openclaw config get gateway.auth.token

if [ -f "$OPENCLAW_LOG_FILE" ]; then
    echo "[INFO] Redacting tokenized dashboard URLs in Openclaw.txt"
    sed -E 's/(#token=)[A-Za-z0-9]+/\1<REDACTED>/g' "$OPENCLAW_LOG_FILE" > "$OPENCLAW_LOG_FILE.tmp"
    mv "$OPENCLAW_LOG_FILE.tmp" "$OPENCLAW_LOG_FILE"
fi

echo "[OK] Token rotation flow completed. Update any dependent clients if needed."
