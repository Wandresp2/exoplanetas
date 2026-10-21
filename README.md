# Exoplanetas NASA

Sistema portable: **MySQL 8.4** + **Streamlit** orquestados con Docker Compose.  
Los datos del NASA Exoplanet Archive se cargan automáticamente desde `init.sql` (sin reejecutar el pipeline ETL): ~4847 estrellas, ~6451 planetas, 133 telescopios y ~6451 descubrimientos.

## Requisitos

- Docker Engine + Docker Compose (en Windows/Mac: Docker Desktop)
- Git
- Puertos libres: **3306** (MySQL) y **8501** (Streamlit)
- Internet la primera vez (pull de `mysql:8.4` y de la imagen de la app)

## Estructura del repositorio

```text
├── docker-compose.yml      # orquesta mysql + streamlit
├── Dockerfile              # imagen de la app Streamlit
├── .dockerignore
├── requirements.txt        # dependencias Python (pinnadas)
├── init.sql                # CREATE + INSERT (schema y datos)
├── app/                    # código Streamlit (UI multipágina)
└── README.md               # este archivo
```

| Servicio    | Imagen                            | Rol                                   |
|-------------|-----------------------------------|---------------------------------------|
| `mysql`     | `mysql:8.4`                       | Base de datos + carga de `init.sql`   |
| `streamlit` | `andresperez3/exoplanetas:latest` | UI en el navegador                    |

Red Docker: `astronomia_net`  
Credenciales lab: usuario `root`, contraseña `root`, base `astronomia`.

---

## 1. Clonar el repositorio

Repositorio: [https://github.com/Wandresp2/exoplanetas.git](https://github.com/Wandresp2/exoplanetas.git)

Ejecuta **en este orden**:

```bash
git clone https://github.com/Wandresp2/exoplanetas.git
cd exoplanetas
```

---

## 2. Levantar el sistema (imagen ya publicada en Docker Hub)

Secuencia recomendada para un tercero (pull desde Hub, **sin** construir en local).  
Ejecuta **en este orden**:

```bash
docker compose down -v
docker compose pull
docker compose up -d --no-build
```

Abrir en el navegador:

- UI Streamlit: [http://localhost:8501](http://localhost:8501)
- MySQL (opcional, desde el host): `localhost:3306`

Comprobar estado:

```bash
docker compose ps
```

---

## 3. Primera vez / desarrollo (construir la imagen localmente)

Si aún no está la imagen en Hub, o estás desarrollando la app, ejecuta **en este orden**:

```bash
docker compose down -v
docker compose up -d --build
```

---

## 4. Si un puerto está ocupado (3306 o 8501)

Si Docker indica que el puerto **3306** o **8501** ya está en uso, hay que **detener** o **eliminar** el contenedor que lo publica, y luego volver a la secuencia de arranque (sección 2 o 3).

### Opción A — Detener (menos agresivo)

Solo para el contenedor; no lo elimina.

**Linux / macOS / WSL** (prioridad):

```bash
docker ps --filter "publish=3306"
docker ps --filter "publish=8501"
docker stop $(docker ps -q --filter "publish=3306")
docker stop $(docker ps -q --filter "publish=8501")
```

Si algún `docker stop` falla porque no hay contenedor en ese puerto, continúa con el siguiente comando.

**Windows (PowerShell):**

```powershell
docker ps --filter "publish=3306"
docker ps --filter "publish=8501"
docker ps -q --filter "publish=3306" | ForEach-Object { docker stop $_ }
docker ps -q --filter "publish=8501" | ForEach-Object { docker stop $_ }
```

### Opción B — Eliminar el contenedor que usa el puerto

Más directo si el contenedor no te importa conservar.

**Linux / macOS / WSL** (prioridad):

```bash
docker rm -f $(docker ps -aq --filter "publish=3306")
docker rm -f $(docker ps -aq --filter "publish=8501")
```

**Windows (PowerShell):**

```powershell
docker ps -aq --filter "publish=3306" | ForEach-Object { docker rm -f $_ }
docker ps -aq --filter "publish=8501" | ForEach-Object { docker rm -f $_ }
```

### Después de liberar el puerto

Vuelve a arrancar **en este orden**:

```bash
docker compose down -v
docker compose pull
docker compose up -d --no-build
```

(O usa `docker compose up -d --build` si estás en modo desarrollo.)

---

## 5. Detener el proyecto (sin borrar datos)

Ejecuta:

```bash
docker compose stop
```

Para volver a iniciarlo más tarde (mismo volumen / datos):

```bash
docker compose start
```

---

## 6. Apagar y eliminar contenedores (conservando el volumen)

```bash
docker compose down
```

---

## 7. Eliminar el proyecto por completo (contenedores + volumen + datos)

Esto borra también los datos de MySQL del volumen. Ejecuta **en este orden**:

```bash
docker compose down -v
```

Opcional: eliminar también la imagen local de la app:

```bash
docker rmi andresperez3/exoplanetas:latest
```

---

## 8. Volver a correr desde cero

Tras haber hecho `down -v` (o en una máquina limpia), ejecuta **en este orden**:

```bash
docker compose pull
docker compose up -d --no-build
```

Abrir de nuevo: [http://localhost:8501](http://localhost:8501)

---

## 9. Arquitectura (recordatorio)

```text
Navegador → localhost:8501 → contenedor streamlit → red astronomia_net → mysql:3306
```

Dentro del contenedor de la app, el host de MySQL es el nombre del servicio (`mysql`), **no** `localhost`.

`init.sql` se ejecuta **solo** en el primer arranque con volumen vacío.  
Si cambias el dump o quieres recargar datos: `docker compose down -v` y luego `up` de nuevo.

---

## 10. UI Streamlit

- **Inicio** — KPIs y resumen  
- **Explorar** — búsqueda de planetas y estrellas  
- **Descubrimientos** — métodos, años, telescopios  
- **Gráficos** — visualizaciones Plotly  

---

## 11. Publicar imagen en Docker Hub (autor)

Ejecuta **en este orden**:

```bash
docker login -u andresperez3
docker compose build streamlit
docker push andresperez3/exoplanetas:latest
```

Luego sube el repositorio a GitHub (`compose` + `init.sql` + `app/` + `README.md`) para que terceros puedan clonar y usar `--no-build`.
