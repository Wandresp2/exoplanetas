# Libera puertos 3306/8501 ocupados por contenedores Docker, pull y up --no-build.
$ErrorActionPreference = "Stop"

Write-Host "==> Liberando contenedores que publican 3306 o 8501..."
foreach ($port in 3306, 8501) {
    $ids = docker ps -aq --filter "publish=$port" 2>$null
    if ($ids) {
        Write-Host "    docker rm -f (puerto $port): $ids"
        docker rm -f $ids | Out-Null
    }
}

Write-Host "==> docker compose down -v"
docker compose down -v

Write-Host "==> docker compose pull"
docker compose pull

Write-Host "==> docker compose up -d --no-build"
docker compose up -d --no-build

Write-Host ""
Write-Host "Listo. UI: http://localhost:8501"
Write-Host "MySQL: localhost:3306 (root/root, DB astronomia)"
