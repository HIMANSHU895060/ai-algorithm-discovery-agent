@echo off
REM AI Algorithm Discovery Agent - Automatic Installation Script
REM For Windows Systems
REM Run this file by double-clicking it!

echo.
echo ====================================================
echo   AI Algorithm Discovery Agent - Installation
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from python.org
    echo Then run this script again.
    pause
    exit /b 1
)

echo [1/5] Checking Python installation... OK
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install requirements
echo [4/5] Installing dependencies...
if exist requirements.txt (
    pip install -r requirements.txt --quiet
    echo Dependencies installed!
) else (
    echo Installing core packages...
    pip install flask numpy --quiet
    echo Core packages installed!
)
echo.

REM Create quick start script
echo [5/5] Creating quick start shortcuts...

REM Create RUN.bat
echo Creating RUN.bat...
(
    echo @echo off
    echo call venv\Scripts\activate.bat
    echo python cli.py %%*
    echo pause
) > RUN.bat

REM Create DISCOVER.bat (quick discovery)
echo Creating DISCOVER.bat...
(
    echo @echo off
    echo call venv\Scripts\activate.bat
    echo python cli.py discover sorting
    echo pause
) > DISCOVER.bat

echo.
echo ====================================================
echo   INSTALLATION COMPLETE!
echo ====================================================
echo.
echo You can now use these commands:
echo.
echo 1. Double-click RUN.bat to use the CLI
echo    Or type commands like:
echo    - RUN.bat discover sorting
    echo    - RUN.bat discoveries
echo    - RUN.bat stats
echo.
echo 2. Double-click DISCOVER.bat to quickly discover algorithms
echo.
echo 3. Use these CLI commands:
echo    discover PROBLEM_TYPE   - Discover algorithm
echo    discoveries            - List all discoveries
echo    stats                  - Show statistics
echo    status                 - Show system status
echo.
echo ====================================================
echo.
pause
