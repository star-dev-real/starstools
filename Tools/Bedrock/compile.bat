@echo off
setlocal

REM ==========================================================
REM CONFIGURATION
REM ==========================================================
set PYTHON_SCRIPT=main.py
set ICON_FILE=icon.ico
set OUTPUT_DIR=dist
set BUILD_DIR=build


echo =========================================================
echo [1] Compiling script to .exe with icon...
echo =========================================================

pyinstaller ^
  --onefile ^
  --icon=%ICON_FILE% ^
  --distpath %OUTPUT_DIR% ^
  --workpath %BUILD_DIR% ^
  --clean ^
  %PYTHON_SCRIPT%

if errorlevel 1 (
    echo Compilation failed. Exiting.
    exit /b 1
)

echo =========================================================
echo Done! ✅ Check the '%OUTPUT_DIR%' folder for your compiled .exe
echo =========================================================
endlocal
pause
