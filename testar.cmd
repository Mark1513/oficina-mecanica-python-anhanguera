@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
py -3 -X utf8 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if not errorlevel 1 (
    py -3 -X utf8 -m unittest discover -s tests -v
    goto fim
)
python -X utf8 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if not errorlevel 1 (
    python -X utf8 -m unittest discover -s tests -v
    goto fim
)
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -X utf8 -m unittest discover -s tests -v
    goto fim
)
echo Python 3.10 ou superior nao encontrado. Instale-o e execute novamente.
:fim
pause
