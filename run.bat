@echo off
cd /d "%~dp0"

if not exist .venv (
    echo First run: installing dependencies...
    py -3 -m venv .venv 2>nul || python -m venv .venv || goto :no_python
    .venv\Scripts\python -m pip install -q --disable-pip-version-check -r requirements.txt || goto :install_failed
)

start "" .venv\Scripts\pythonw app.py
exit /b 0

:no_python
echo Python 3.9+ is required: https://www.python.org/downloads/
pause
exit /b 1

:install_failed
rmdir /s /q .venv
echo Dependency installation failed.
pause
exit /b 1
