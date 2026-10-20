@echo off
setlocal
REM Run from any working directory. Uses this Python interpreter's pip only.
python -c "import sys; raise SystemExit(sys.version_info < (3, 10))" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.10 or newer is required on PATH.
    exit /b 1
)
pushd "%~dp0"
if errorlevel 1 exit /b 1
python -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo ERROR: Dependency installation failed. Use an activated virtual environment.
    popd
    exit /b 1
)
python -m pytest "%~dp0tests" -v --tb=short
if errorlevel 1 (
    echo ERROR: Tests failed; setup is not qualified.
    popd
    exit /b 1
)
popd
echo Setup checks passed. Compiler and research tools remain experimental.
echo Usage: python hc11cc.py examples/blink.c -o blink.asm
echo Usage: python hc11kit.py --help
exit /b 0
