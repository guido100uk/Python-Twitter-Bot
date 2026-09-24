@echo off
setlocal EnableExtensions
REM One-click Windows File Organizer
REM Double-click this file, or drag a folder onto it.

cd /d "%~dp0"

set "TARGET=%~1"
if "%TARGET%"=="" set "TARGET=%CD%"

where python >nul 2>&1
if errorlevel 1 (
  where py >nul 2>&1
  if errorlevel 1 (
    echo Python was not found. Install Python 3 from https://www.python.org/downloads/
    echo Make sure "Add python.exe to PATH" is checked.
    pause
    exit /b 1
  )
  set "PY=py -3"
) else (
  set "PY=python"
)

set "PYTHONPATH=%~dp0src;%PYTHONPATH%"

echo.
echo === Preview ===
%PY% -m file_organizer "%TARGET%"
if errorlevel 1 (
  pause
  exit /b 1
)

echo.
set /p CONFIRM="Organize this folder now? [Y/N] "
if /I not "%CONFIRM%"=="Y" (
  echo Cancelled.
  pause
  exit /b 0
)

echo.
echo === Organizing ===
%PY% -m file_organizer "%TARGET%" --organize
echo.
echo Done. To undo:  %PY% -m file_organizer "%TARGET%" --undo
pause
endlocal
