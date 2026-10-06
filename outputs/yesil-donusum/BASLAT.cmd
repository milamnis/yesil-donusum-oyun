@echo off
cd /d "%~dp0"
where node >nul 2>&1
if errorlevel 1 (
  echo Node.js bulunamadi. Node.js 22 veya daha yeni surumunu kurun.
  pause
  exit /b 1
)
node serve.mjs --open
