# Exoplanetas NASA

MySQL 8.4 + Streamlit con Docker Compose.  
Repo: [https://github.com/Wandresp2/exoplanetas.git](https://github.com/Wandresp2/exoplanetas.git)  
UI: [http://localhost:8501](http://localhost:8501) · Puertos: **3306** (MySQL), **8501** (Streamlit)

---

## 1. Clonar e entrar al repositorio

```bash
git clone https://github.com/Wandresp2/exoplanetas.git
cd exoplanetas
```

---

## 2. Liberar puertos (si 3306 o 8501 están ocupados)

**Menos agresivo** — detiene el contenedor:

```bash
# Linux / macOS / WSL
docker stop $(docker ps -q --filter "publish=3306")
docker stop $(docker ps -q --filter "publish=8501")
```

```powershell
# Windows PowerShell
docker ps -q --filter "publish=3306" | ForEach-Object { docker stop $_ }
docker ps -q --filter "publish=8501" | ForEach-Object { docker stop $_ }
```

**Más agresivo** — elimina el contenedor:

```bash
# Linux / macOS / WSL
docker rm -f $(docker ps -aq --filter "publish=3306")
docker rm -f $(docker ps -aq --filter "publish=8501")
```

```powershell
# Windows PowerShell
docker ps -aq --filter "publish=3306" | ForEach-Object { docker rm -f $_ }
docker ps -aq --filter "publish=8501" | ForEach-Object { docker rm -f $_ }
```

---

## 3. Levantar el proyecto

Baja volúmenes previos, descarga imágenes y arranca sin construir en local:

```bash
docker compose down -v
docker compose pull
docker compose up -d --no-build
```

Abrir: [http://localhost:8501](http://localhost:8501)

---

## 4. Detener el proyecto

```bash
docker compose stop
```

Para borrar también contenedores y datos del volumen:

```bash
docker compose down -v
```

---

## 5. Volver a correr

Si solo lo detuviste con `stop`:

```bash
docker compose start
```

Si usaste `down -v` (o es un arranque limpio), repite la sección **3**.
