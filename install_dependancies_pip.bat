@echo off
REM ============================================================================
REM KingAI 68HC11 C Compiler — Setup Script
REM ============================================================================
REM
REM Prerequisites:
REM   - Python 3.10+ (3.12 or 3.13 recommended)
REM     Download: https://www.python.org/downloads/
REM     IMPORTANT: Check "Add Python to PATH" during install
REM
REM   - VS Code (optional but recommended)
REM     Download: https://code.visualstudio.com/
REM     Recommended extensions:
REM       ms-python.python          (Python language support)
REM       ms-python.debugpy         (Python debugger)
REM       dan-c-underwood.arm       (ARM/68HC11 assembly syntax)
REM       eamodio.gitlens            (Git integration)
REM      ms-vscode.cpptools       this is large can skip  (C/C++ language support)
REM
REM Usage:
REM   Run this script to install Python dependencies and verify setup.



REM ============================================================================

echo.
echo === KingAI 68HC11 C Compiler Setup ===
echo.

REM Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH.
    echo.
    echo Install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Python found:
python --version
echo.

REM Install dependencies
echo [2/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: pip install failed. Trying with --user flag...
    pip install --user -r requirements.txt
)
echo.

REM Run test suite to verify
echo [3/3] Running test suite to verify installation...
python -m pytest tests/ -v --tb=short
echo.

if errorlevel 1 (
    echo WARNING: Some tests failed. Check output above.
) else (
    echo All tests passed!
)

echo.
echo === Setup Complete ===
echo.
echo Usage:
echo   python hc11cc.py examples/blink.c -o blink.asm       Compile C to assembly
echo   python hc11cc.py examples/blink.c -o blink.s19 -f s19  Compile to S-record
echo   python hc11kit.py examples/blink.c                    Compile + assemble
echo   python -m pytest tests/ -v                            Run tests
echo.
pause
