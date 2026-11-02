@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m codeatlas.desktop
) else (
  python -m codeatlas.desktop
)
if errorlevel 1 (
  echo.
  echo Avvio non riuscito. Verifica che Python 3.10+ sia installato.
  pause
)
