@echo off
chcp 65001 >nul
cd /d "%~dp0"
where docker >nul 2>nul
if errorlevel 1 (
  echo No se encontro Docker. Instala Docker Desktop, abrelo y vuelve a ejecutar este archivo.
  pause
  exit /b 1
)
if not exist .env copy .env.example .env >nul
echo Construyendo y levantando DataPath. La primera vez tarda varios minutos...
docker compose up -d --build
if errorlevel 1 (
  echo.
  echo Hubo un error. Comprueba que Docker Desktop este abierto y en marcha.
  pause
  exit /b 1
)
echo.
echo Listo. Abriendo http://localhost:8080
start "" http://localhost:8080
pause
