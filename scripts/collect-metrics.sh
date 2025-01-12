#!/usr/bin/env bash
# Collect basic system metrics
set -euo pipefail

echo "=== CPU ==="
top -l 1 -n 0 2>/dev/null | grep "CPU usage" || uptime

echo ""
echo "=== Memory ==="
free -m 2>/dev/null || vm_stat 2>/dev/null | head -10

echo ""
echo "=== Disk ==="
df -h /

echo ""
echo "=== Network Connections ==="
ss -tuln 2>/dev/null || netstat -an | grep LISTEN | head -20
