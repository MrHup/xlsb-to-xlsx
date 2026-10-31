@echo off
rem Builds a standalone dist\xlsb2xlsx.exe. Run run.bat once first.
cd /d "%~dp0"
.venv\Scripts\python -m pip install -q --disable-pip-version-check pyinstaller
.venv\Scripts\pyinstaller --onefile --windowed --name xlsb2xlsx app.py
