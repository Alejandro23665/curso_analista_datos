# DataPath · Mi ruta a analista e ingeniero de datos

Plataforma de estudio personal (estilo DataCamp) con **React + FastAPI + PostgreSQL**.
Cada tema tiene **Teoría**, **Práctica** (ejercicios que se corrigen solos) y **Apuntes** (tus notas en Markdown).
El panel de inicio y la página *Fortalezas y debilidades* se calculan con tus intentos reales.

## Qué incluye

- **3 rutas de aprendizaje** con secciones propias (por defecto solo se muestra la de producto; ver `ACTIVE_TRACKS`):
  - 🛠️ **Ingeniero de datos** (28 temas, ~304 h): Python, SQL, bases de datos, pipelines, calidad, cloud e IA.
  - 🚀 **Ingeniero de producto y startups** (29 temas, ~282 h): Python profesional, APIs, seguridad, LLMs por dentro, RAG, agentes y MCP, evaluación y seguridad de IA, desarrollo con agentes de código, arquitectura (incluida la distribuida), diseño de sistemas, producción y validación de startups.
  - 📊 **Analista de datos** (28 temas, ~276 h): SQL, pandas, estadística, Excel, Power BI y comunicación.
- **Progreso compartido:** el progreso se guarda por tema, así que un tema que está en varias rutas (Python, SQL, Docker, IA asistida...) cuenta en todas al completarlo. En el mapa de cada ruta se marcan con 🔗.
- **49 temas y 283 ejercicios**: SQL (contra un PostgreSQL de práctica), Python (en tu navegador con Pyodide), quizzes y listas de verificación de proyectos.
- **Proyectos de portafolio:** análisis exploratorio, pipeline de datos, dashboard publicado y un MVP en producción.
- **Progreso** por ruta, sección y tema, racha de estudio y fecha estimada de finalización.
- **Fortalezas y debilidades** por habilidad (≥ 3 intentos: ≥ 75 % fortaleza, < 50 % a reforzar) y plan de repaso sugerido.
- **Apuntes** por tema con guardado automático y vista previa Markdown.
- **Para profundizar:** videos, documentación y libros recomendados al final de la teoría de cada tema (`backend/app/content/recursos.py`).

## Arrancar con Docker (lo más sencillo)

Requisitos: Docker Desktop. En PowerShell, dentro de esta carpeta:

```powershell
copy .env.example .env      # y edita las claves
docker compose up -d --build
```

Abre **http://localhost:8080**. La primera vez el backend crea las tablas y los datos de práctica solo.

```powershell
docker compose logs -f backend     # ver logs
docker compose down                # detener (tus datos se conservan en el volumen pgdata)
```

## Desarrollo local (sin construir imágenes)

1. Base de datos: `docker compose up -d db`
2. Backend (Python 3.11+):

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

3. Frontend (Node 20+):

```powershell
cd frontend
npm install
npm run dev
```

Abre **http://localhost:5173** (Vite envía `/api` al backend en el puerto 8000).

## Variables de entorno (backend)

| Variable | Por defecto | Para qué |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg://datapath:datapath@localhost:5432/datapath` | Conexión a PostgreSQL |
| `SANDBOX_DB_PASSWORD` | `sandbox_ro_change_me` | Clave del rol de solo lectura que ejecuta tu SQL |
| `STUDY_HOURS_PER_DAY` | `3` | Para estimar la fecha de finalización |
| `APP_TZ` | `America/Caracas` | Zona horaria de la racha de estudio |
| `CORS_ORIGINS` | `http://localhost:5173` | Orígenes permitidos (separados por comas) |
| `APP_PASSWORD` | *(vacía)* | Contraseña de acceso; si está vacía no se pide (solo para uso local) |
| `ACTIVE_TRACKS` | `producto` | Rutas visibles, separadas por comas (`producto,ingeniero-datos,analista`). Las ocultas conservan su contenido y tu progreso |

## Cómo funciona la práctica

- **SQL:** tu consulta corre en el esquema `sandbox` con un rol `sandbox_ro` (solo `SELECT`, transacción de solo lectura, límite de 5 s). La app compara tu resultado con el de la solución de referencia (columnas por posición, números a 2 decimales; el orden solo cuenta si el enunciado lo pide).
- **Python:** se ejecuta en un Web Worker con Pyodide (Python en WebAssembly). El código nunca llega al servidor y un bucle infinito no congela la página (se corta a los 20 s). La primera vez descarga Python/pandas desde un CDN, así que necesita internet.
- **Quizzes:** se corrigen en el servidor. **Listas de verificación:** las marcas tú mismo (proyectos y portafolio).

## Datos de práctica en CSV

Para Excel y Power BI puedes descargar los datos de la tienda en `/api/sandbox/csv/{nombre}` (`ventas`, `orders`, `order_items`, `customers`, `products`, `employees`); por ejemplo http://localhost:8080/api/sandbox/csv/ventas. Los enlaces también están en la teoría de los temas de Excel y Power BI.

## Mantener y ampliar el contenido

Todo el currículo vive en `backend/app/content/fase_*.py` (teoría en Markdown + ejercicios) y las rutas en `backend/app/content/tracks.py`. Para añadir un tema, copia uno existente dentro de `TOPICS`, dale un `slug` único, añádelo a las secciones de las rutas que quieras en `tracks.py` y ejecuta:

```powershell
cd backend
python -m app.content_check                 # valida estructura, soluciones de Python y SQL
python -m unittest discover -s tests -v     # pruebas de la lógica
```

`content_check` comprueba que cada solución pase sus pruebas, que el código inicial **no** las pase y que cada SQL devuelva filas.
Los ejercicios marcados `pg_only=True` usan funciones de PostgreSQL y se validan ejecutándolos en la app.

## Desplegar en Vercel

El repositorio ya trae lo necesario: `vercel.json` (compila el frontend y enruta `/api/*`), `api/index.py` (la API de FastAPI como función de Python),
`requirements.txt` y `.python-version` en la raíz. Vercel **no aloja PostgreSQL**, así que la base va en un servicio aparte (Neon es lo más cómodo y tiene plan gratuito).

1. **Sube el código a GitHub** (ver más abajo).
2. En [vercel.com](https://vercel.com) → **Add New → Project** → importa el repositorio. Deja *Root Directory* en la raíz y *Framework Preset* en **Other**: la configuración se lee de `vercel.json`.
3. **Base de datos:** en el proyecto de Vercel → **Storage → Create Database → Neon** y conéctala al proyecto. Vercel crea las variables `DATABASE_URL` y `DATABASE_URL_UNPOOLED`, y la app usa esta última si existe.
   También puedes crear la base en Neon o Supabase por tu cuenta y definir `DATABASE_URL` a mano.
4. **Variables de entorno** (Settings → Environment Variables):

| Variable | Valor |
|---|---|
| `APP_PASSWORD` | **Obligatoria.** La contraseña para entrar a la app. Sin ella, cualquiera con el enlace vería y cambiaría tu progreso. |
| `SANDBOX_DB_PASSWORD` | Una clave larga para el rol de solo lectura del SQL de práctica. |
| `STUDY_HOURS_PER_DAY` | `3` |
| `APP_TZ` | `America/Caracas` |

5. **Deploy.** La primera petición crea las tablas y los datos de práctica (puede tardar unos segundos). Después entra con tu contraseña.

Notas:

- Si cambias variables de entorno, haz **Redeploy** para que se apliquen.
- Si ves "La base de datos no está disponible", revisa `DATABASE_URL` y los logs de la función en Vercel (*Deployments → Functions*).
- Los ejercicios de Python se ejecutan en tu navegador (Pyodide desde jsDelivr), así que no consumen recursos de Vercel.
- Copia de seguridad: en Neon puedes crear *branches* o usar `pg_dump` con la cadena de conexión.

## Seguridad al publicarla

- Es una app **de un solo usuario**. Con `APP_PASSWORD` definida pide la contraseña y guarda una cookie de sesión segura (HttpOnly) durante 60 días; el botón **Salir** la borra.
- En local (Docker o `iniciar-local.bat`) puedes dejar `APP_PASSWORD` vacía.
- Tu SQL de práctica se ejecuta en transacciones de solo lectura, limitadas al esquema `sandbox` y a 5 segundos.
- Copia de seguridad en Docker:

```powershell
docker compose exec db pg_dump -U datapath datapath > backup.sql
```

## Subir el proyecto a GitHub

```powershell
git init
git add .
git commit -m "DataPath: plataforma de estudio"
git branch -M main
git remote add origin https://github.com/Alejandro23665/curso_analista_datos.git
git push -u origin main
```

`.gitignore` ya excluye `.env`, dependencias y cachés: **nunca subas tu `.env`**.

## Estructura

```
api/index.py      entrada de la API para Vercel
backend/          FastAPI + SQLAlchemy (progreso, intentos, apuntes) + sandbox SQL
  app/content/    currículo (teoría + ejercicios)
frontend/         React + Vite (CodeMirror, Pyodide, Recharts)
docker-compose.yml, iniciar.bat     uso local con Docker
iniciar-local.bat, setup_db.sql     uso local sin Docker
vercel.json, requirements.txt       despliegue en Vercel
```
