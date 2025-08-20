@echo off
REM MKV Video Compressor Build Script for Windows
REM This script builds the project for distribution

setlocal enabledelayedexpansion

echo [INFO] Starting build process...

REM Check if Python is available
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set python_version=%%i
echo [INFO] Using Python %python_version%

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
pip install --upgrade pip

REM Install build dependencies
echo [INFO] Installing build dependencies...
pip install build twine wheel setuptools

REM Install project dependencies
echo [INFO] Installing project dependencies...
pip install -r requirements.txt

REM Install development dependencies
echo [INFO] Installing development dependencies...
pip install pytest pytest-cov black flake8 mypy

REM Run tests
echo [INFO] Running tests...
python -m pytest tests\ -v

if !errorlevel! neq 0 (
    echo [ERROR] Tests failed! Please fix issues before building.
    exit /b 1
)

REM Check code style
echo [INFO] Checking code style...
black --check src\
if !errorlevel! neq 0 (
    echo [WARNING] Code style issues found. Run 'black src\' to fix.
)

flake8 src\
if !errorlevel! neq 0 (
    echo [WARNING] Linting issues found.
)

REM Clean previous builds
echo [INFO] Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.egg-info" rmdir /s /q *.egg-info

REM Build the package
echo [INFO] Building package...
python -m build

REM Check the built package
echo [INFO] Checking built package...
twine check dist\*

echo [INFO] Build completed successfully!
echo [INFO] Built packages:
dir dist\

echo.
echo [INFO] To install the package locally:
echo   pip install dist\mkv_video_compressor-*.whl
echo.
echo [INFO] To upload to PyPI (test):
echo   twine upload --repository testpypi dist\*
echo.
echo [INFO] To upload to PyPI (production):
echo   twine upload dist\*

pause