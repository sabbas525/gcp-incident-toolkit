#!/usr/bin/env bash
# Probe a list of endpoints and report status
set -euo pipefail

ENDPOINTS=${@:-"http://localhost:8080/health"}

for url in $ENDPOINTS; do
  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")
  if [ "$status" = "200" ]; then
    echo "[OK]   $url ($status)"
  else
    echo "[FAIL] $url ($status)"
  fi
done
