@echo off
echo Spouštím FlexiFiles...
echo.

REM Zkontroluje, zda existuje virtuální prostředí
if exist ".venv\Scripts\python.exe" (
    echo Používám virtuální prostředí...
    .venv\Scripts\python.exe file_browser.py
) else (
    echo Virtuální prostředí nenalezeno, používám systémový Python...
    python file_browser.py
)

echo.
echo FlexiFiles byl ukončen.
pause
