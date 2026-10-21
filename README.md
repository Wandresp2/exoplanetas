# Exoplanetas NASA

Sistema portable: **MySQL 8.4** + **Streamlit** orquestados con Docker Compose.  
Los datos del NASA Exoplanet Archive se cargan automáticamente desde `init.sql` (sin reejecutar el pipeline ETL): ~4847 estrellas, ~6451 planetas, 133 telescopios y ~6451 descubrimientos.

## Requisitos

- Docker Engine + Docker Compose (Docker Desktop en Windows/Mac)
- Puertos libres: **3306** (MySQL) y **8501** (Streamlit)

## Arranque rápido (tercero)

> **Importante:** sustituye la URL del repositorio por la tuya.  
> Placeholder: `https://github.com/TU_USUARIO/TU_REPO.git`

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### Con script de lab

```bash
# Linux / WSL / macOS
chmod +x lab-arranque.sh && ./lab-arranque.sh

# Windows PowerShell
.\lab-arranque.ps1
```

### Manual (imagen ya publicada en Docker Hub)

```bash
docker compose down -v
docker compose pull
docker compose up -d --no-build
```

Abrir la UI: [http://localhost:8501](http://localhost:8501)

### Primera vez / desarrollo local (construir imagen)

```bash
docker compose up -d --build
```

## Credenciales (lab)

| Variable   | Valor        |
|------------|--------------|
| MySQL user | `root`       |
| Password   | `root`       |
| Database   | `astronomia` |
| Host (app) | `mysql` (nombre del servicio Compose) |

## Arquitectura

```text
Navegador → localhost:8501 → contenedor streamlit → red astronomia_net → mysql:3306
```

| Servicio    | Imagen                              | Rol                                      |
|-------------|-------------------------------------|------------------------------------------|
| `mysql`     | `mysql:8.4`                         | Schema + datos vía `init.sql`            |
| `streamlit` | `andresperez3/exoplanetas:latest`   | UI (también se puede `build: .`)         |

`init.sql` se ejecuta **solo** en el primer arranque con volumen vacío.  
Si cambias el dump: `docker compose down -v` y vuelve a subir.

## UI Streamlit

- **Inicio** — KPIs y resumen  
- **Explorar** — búsqueda de planetas y estrellas  
- **Descubrimientos** — métodos, años, telescopios  
- **Gráficos** — visualizaciones Plotly  

## Publicar imagen (autor)

```bash
docker login -u andresperez3
docker compose build streamlit
docker push andresperez3/exoplanetas:latest
```

Luego sube el repo a GitHub (`compose` + `init.sql` + `app/`) para que terceros puedan clonar y usar `--no-build`.

## Estructura

```text
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── init.sql
├── app/
├── lab-arranque.sh
├── lab-arranque.ps1
└── README.md
```

La carpeta `docs/` (notebook, guía, script generador) es **local** y está en `.gitignore` / `.dockerignore`.

## Regenerar `init.sql` (autor)

Con Python y dependencias (`pandas`, `requests`):

```bash
py docs/generate_init_sql.py
```
