@echo off
setlocal

REM ==========================================================
REM CONFIGURATION
REM ==========================================================
set PYTHON_SCRIPT=main.py
set ICON_FILE=icon.ico
set OUTPUT_DIR=dist
set BUILD_DIR=build
set OBF_DIR=obf

echo =========================================================
echo [1] Obfuscating Python script with PyArmor...
echo =========================================================
pyarmor gen -O %OBF_DIR% %PYTHON_SCRIPT%

if errorlevel 1 (
    echo Obfuscation failed. Exiting.
    exit /b 1
)

echo =========================================================
echo [2] Compiling Obfuscated script to .exe with icon...
echo =========================================================
pyinstaller --onefile --hidden-import asyncio --hidden-import json --hidden-import os --hidden-import time --hidden-import threading --hidden-import winreg --hidden-import atexit --hidden-import mitmproxy --hidden-import mitmproxy.tools.dump --icon=%ICON_FILE% %OBF_DIR%\%PYTHON_SCRIPT%

if errorlevel 1 (
    echo Compilation failed. Exiting.
    exit /b 1
)

echo =========================================================
echo Done! ✅ Check the 'dist' folder for your compiled .exe
echo =========================================================
endlocal
pause
