@echo off
rem Double-click to start ZEHEN. Finds Python even when it isn't on PATH; installs libraries on first run.
cd /d "%~dp0"
set "PY="
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*" "%ProgramFiles%\Python3*") do (
  if exist "%%~D\pythonw.exe" set "PY=%%~D\python.exe"
)
rem python.exe on PATH, unless it's the WindowsApps stub that only opens the Microsoft Store
if not defined PY for %%P in (python.exe) do (
  echo %%~$PATH:P | find /i "WindowsApps" >nul || if not "%%~$PATH:P"=="" set "PY=%%~$PATH:P"
)
if not defined PY (
  echo Python 3 was not found. Install it from https://www.python.org/downloads/ and run ZEHEN.bat again.
  pause
  exit /b 1
)
"%PY%" -c "import importlib.util as u, sys; sys.exit(any(u.find_spec(m) is None for m in ('mediapipe', 'cv2', 'pyautogui', 'winrt.windows.ui.input.inking')))" 2>nul
if errorlevel 1 (
  echo First run: installing ZEHEN's libraries, this takes a minute...
  "%PY%" -m pip install -r requirements.txt || (pause & exit /b 1)
)
start "" "%PY:python.exe=pythonw.exe%" zehen.py %*
