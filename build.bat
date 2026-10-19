@echo off
rem Builds dist\ZEHEN.exe. Needs about 1 GB free disk space while building.
cd /d "%~dp0"
set WORK=%TEMP%\zehen_build
python -m pip install -r requirements.txt pyinstaller || goto fail
python -m PyInstaller --noconfirm --onefile --windowed --name ZEHEN --icon "%~dp0zehen.ico" ^
  --collect-all mediapipe --collect-all winrt --exclude-module matplotlib --exclude-module sounddevice ^
  --add-data "%~dp0hand_landmarker.task;." --add-data "%~dp0zehen.ico;." ^
  --distpath "%~dp0dist" --workpath "%WORK%" --specpath "%WORK%" "%~dp0zehen.py" || goto fail
rmdir /s /q "%WORK%"
start /wait "" "%~dp0dist\ZEHEN.exe" --test || goto fail
echo.
echo Done: dist\ZEHEN.exe
pause
exit /b 0
:fail
rmdir /s /q "%WORK%" 2>nul
echo.
echo Build failed. Check you have about 1 GB free disk space.
pause
exit /b 1
