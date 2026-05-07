@echo off
echo ========================================
echo FRESH DATABASE INSTALLATION
echo ========================================
echo.

REM Load environment
call .env

REM Set connection variables
set DB_HOST=localhost
set DB_PORT=5432
set DB_USER=user
set DB_PASS=tara
set DB_NAME=college_sell_db

REM Drop database if exists
echo [1/5] Dropping existing database...
psql postgresql://%DB_USER%:%DB_PASS%@%DB_HOST%:%DB_PORT%/postgres -c "DROP DATABASE IF EXISTS %DB_NAME%;" 2>nul

REM Create fresh database
echo [2/5] Creating fresh database...
psql postgresql://%DB_USER%:%DB_PASS%@%DB_HOST%:%DB_PORT%/postgres -c "CREATE DATABASE %DB_NAME%;"

if errorlevel 1 (
    echo [ERROR] Failed to create database
    pause
    exit /b 1
)

REM Enable extensions
echo [3/5] Enabling extensions...
psql postgresql://%DB_USER%:%DB_PASS%@%DB_HOST%:%DB_PORT%/%DB_NAME% -c "CREATE EXTENSION IF NOT EXISTS pg_trgm; CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

REM Drop core foundation if partial
echo [4/5] Creating core foundation...
if exist core_foundation_tables.sql (
    psql postgresql://%DB_USER%:%DB_PASS%@%DB_HOST%:%DB_PORT%/%DB_NAME% -f core_foundation_tables.sql
) else (
    echo [ERROR] core_foundation_tables.sql not found!
    exit /b 1
)

REM Execute all plan files in order
echo [5/5] Executing schema plans...
for %%f in (
    plan1_academic_core_postgres.sql
    plan2_library_postgres.sql
    plan3_system_admin_postgres.sql
    plan4_transport_postgres.sql
    plan5_canteen_postgres.sql
    plan6_alumni_placement_postgres.sql
    plan7_welfare_discipline_postgres.sql
    plan8_assets_postgres.sql
    plan9_events_communication_postgres.sql
    plan10_reporting_postgres.sql
) do (
    if exist "%%f" (
        echo   Executing %%f...
        psql postgresql://%DB_USER%:%DB_PASS%@%DB_HOST%:%DB_PORT%/%DB_NAME% -f "%%f"
    ) else (
        echo   [WARNING] %%f not found, skipping
    )
)

echo.
echo ========================================
echo VERIFICATION
echo ========================================
psql postgresql://%DB_USER%:%DB_PASS%@%DB_HOST%:%DB_PORT%/%DB_NAME% -c "SELECT COUNT(*) as total_tables FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';"

echo.
echo [SUCCESS] Installation complete!
echo Connection: postgresql://%DB_USER%:%DB_PASS%@%DB_HOST%:%DB_PORT%/%DB_NAME%
echo.
pause
