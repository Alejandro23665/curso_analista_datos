@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal

echo === DataPath (modo local, sin Docker) ===
echo.

rem --- Comprobar herramientas ---
where python >nul 2>nul || (echo No se encontro Python en el PATH. & pause & exit /b 1)
where node >nul 2>nul || (echo No se encontro Node.js en el PATH. & pause & exit /b 1)
where psql >nul 2>nul
if errorlevel 1 (
  for /d %%D in ("C:\Program Files\PostgreSQL\*") do set "PGBIN=%%D\bin"
  if defined PGBIN set "PATH=%PGBIN%;%PATH%"
)
where psql >nul 2>nul || (echo No se encontro psql. Anade la carpeta bin de PostgreSQL al PATH. & pause & exit /b 1)

rem --- Base de datos (solo la primera vez) ---
echo [1/4] Preparando la base de datos. Si te pide una clave, es la del usuario "postgres" de tu PostgreSQL.
psql -h localhost -p 5432 -U postgres -v ON_ERROR_STOP=1 -q -f setup_db.sql
if errorlevel 1 (
  echo.
  echo No se pudo preparar la base de datos. Comprueba que PostgreSQL este en marcha en el puerto 5432
  echo y que la clave del usuario postgres sea correcta.
  pause
  exit /b 1
)

rem --- Backend ---
echo [2/4] Instalando dependencias del backend...
if not exist backend\.venv (
  python -m venv backend\.venv || (echo No se pudo crear el entorno virtual. & pause & exit /b 1)
)
call backend\.venv\Scripts\python.exe -m pip install -q -r backend\requirements.txt
if errorlevel 1 (echo Fallo pip install. Revisa tu conexion a internet. & pause & exit /b 1)

rem --- Frontend ---
echo [3/4] Instalando dependencias del frontend (la primera vez tarda)...
pushd frontend
call npm install
if errorlevel 1 (popd & echo Fallo npm install. & pause & exit /b 1)
popd

echo [4/4] Arrancando backend y frontend en ventanas aparte...
start "DataPath - Backend" cmd /k "cd /d %~dp0backend && set DATABASE_URL=postgresql+psycopg://datapath:datapath@localhost:5432/datapath && .venv\Scripts\python.exe -m uvicorn app.main:app --port 8000"
start "DataPath - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Esperando a que arranque...
timeout /t 12 /nobreak >nul
start "" http://localhost:5173
echo.
echo Si la pagina muestra un error de conexion, espera unos segundos y recarga.
echo Para detener todo, cierra las dos ventanas "DataPath".
pause
