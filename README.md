# XLSB → XLSX

Local converter for Excel binary workbooks. Your files never leave your computer.

## Run (Windows)

Requires [Python 3.9+](https://www.python.org/downloads/).

Double-click `run.bat`. The first run installs the dependencies.

## Standalone .exe

Run `build.bat` after the first run. The output is `dist\xlsb2xlsx.exe`, which runs without Python installed.

## Notes

Copies cell values, including dates, into every sheet. It does not copy formatting, formulas, or charts.
