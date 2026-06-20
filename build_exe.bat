@echo off
echo Creando ejecutable de PowerOff-Timer...
echo.

REM Instalar PyInstaller si no está instalado
pip install pyinstaller

REM Crear el ejecutable usando python -m
python -m PyInstaller --onefile --windowed --name PowerOff-Timer --icon=icon.ico main.py

echo.
echo Ejecutable creado en: dist\PowerOff-Timer.exe
pause

@REM Made by Abraham
