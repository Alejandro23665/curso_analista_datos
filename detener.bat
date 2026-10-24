@echo off
cd /d "%~dp0"
docker compose down
echo DataPath detenido. Tus datos se conservan.
pause
