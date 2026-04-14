@echo off
echo Starting install....
pip install pyinstaller
echo Installed pyinstaller ✅
echo Starting Build
python -m PyInstaller --onefile --windowed --uac-admin --icon="zapret.ico" --name "Zapret control" --add-data "Bin;Bin" --add-data "Resources;Resources" main.py
echo Succsesfuly compiled
echo Priyatnogo ispolzovainya (:
pause