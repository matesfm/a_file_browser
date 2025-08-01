@echo off
echo ============================================
echo   FlexiFiles - Instalace na plochu
echo ============================================
echo.

REM Kontrola existence executable souboru
if not exist "dist\FlexiFiles_v3.exe" (
    echo CHYBA: FlexiFiles_v3.exe nenalezen v dist\ složce!
    echo Ujistěte se, že jste spustili build procesu.
    pause
    exit /b 1
)

REM Vytvoření zástupce na ploše
echo Vytvářím zástupce na ploše...

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\FlexiFiles.lnk'); $Shortcut.TargetPath = '%CD%\dist\FlexiFiles_v3.exe'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'FlexiFiles - Profesionální správce souborů'; $Shortcut.Save()"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ ÚSPĚCH: Zástupce FlexiFiles byl vytvořen na ploše!
    echo.
    echo Můžete nyní FlexiFiles spustit:
    echo   - Dvojklikem na zástupce na ploše
    echo   - Nebo přímo spuštěním: dist\FlexiFiles_v3.exe
    echo.
) else (
    echo.
    echo ❌ CHYBA: Nepodařilo se vytvořit zástupce!
    echo.
)

echo Stiskněte libovolnou klávesu pro ukončení...
pause > nul
