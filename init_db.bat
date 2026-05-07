@echo off
echo ========================================
echo DATABASE INITIALIZATION
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if psycopg2 is installed
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required packages...
    pip install psycopg2-binary python-dotenv
)

REM Run the initialization script
echo [INFO] Starting database initialization...
python init_database.py

if errorlevel 1 (
    echo.
    echo [ERROR] Database initialization failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Database tables created successfully!
echo.
pause
