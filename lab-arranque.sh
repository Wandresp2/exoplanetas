#!/usr/bin/env bash
# Libera puertos 3306/8501 ocupados por contenedores Docker, pull y up --no-build.
set -euo pipefail

echo "==> Liberando contenedores que publican 3306 o 8501..."
for port in 3306 8501; do
  ids=$(docker ps -aq --filter "publish=${port}" || true)
  if [[ -n "${ids}" ]]; then
    echo "    docker rm -f (puerto ${port}): ${ids}"
    docker rm -f ${ids} >/dev/null || true
  fi
done

echo "==> docker compose down -v"
docker compose down -v

echo "==> docker compose pull"
docker compose pull

echo "==> docker compose up -d --no-build"
docker compose up -d --no-build

echo ""
echo "Listo. UI: http://localhost:8501"
echo "MySQL: localhost:3306 (root/root, DB astronomia)"
