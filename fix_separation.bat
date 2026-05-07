@echo off
echo ========================================
echo FIX DATABASE SEPARATION
echo ========================================
echo.
echo This will:
echo  1. Add missing school_* tables to school_sell_db
echo  2. Remove school_* tables from college_sell_db
echo.

REM School database
set SCHOOL_DB=school_sell_db
set SCHOOL_CONN=postgresql://user:tara@localhost:5432/%SCHOOL_DB%

REM College database
set COLLEGE_DB=college_sell_db
set COLLEGE_CONN=postgresql://user:tara@localhost:5432/%COLLEGE_DB%

echo School DB: %SCHOOL_DB%
echo College DB: %COLLEGE_DB%
echo.

REM Enable extensions in school DB
echo [1/3] Enabling extensions in school DB...
psql %SCHOOL_CONN% -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
psql %SCHOOL_CONN% -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

echo.
echo [2/3] Adding school_* tables to school DB...
echo Execute these files in order against school_sell_db:
echo.
echo   plan1_academic_core_postgres.sql (contains some school_* tables)
echo   plan2_library_postgres.sql (contains some school_* tables)
echo   plan4_transport_postgres.sql (contains school_* tables)
echo   plan5_canteen_postgres.sql (contains school_* tables)
echo   plan6_alumni_placement_postgres.sql (contains college_* only)
echo   plan7_welfare_discipline_postgres.sql (contains college_* mostly)
echo   plan8_assets_postgres.sql (contains school_* tables)
echo   plan9_events_communication_postgres.sql (contains school_* tables)
echo.
echo Use pgAdmin or run:
echo   psql %SCHOOL_CONN% -f plan4_transport_postgres.sql
echo   psql %SCHOOL_CONN% -f plan5_canteen_postgres.sql
echo   psql %SCHOOL_CONN% -f plan8_assets_postgres.sql
echo   psql %SCHOOL_CONN% -f plan9_events_communication_postgres.sql
echo.
echo (Files with only college_* tables can be skipped)

echo [3/3] Removing school_* tables from college DB...
echo WARNING: This will delete school_* tables from college_sell_db
echo.
choice /C YN /M "Proceed with removal"
if errorlevel 2 goto CANCEL

echo Removing school_* tables from college...
psql %COLLEGE_CONN% -c "DO $$ DECLARE r RECORD; BEGIN FOR r IN SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school\_%' LOOP EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.table_name) || ' CASCADE;'; END LOOP; END $$;"

echo.
echo ========================================
echo DONE
echo ========================================
echo.
echo Verify:
echo   School tables in school DB:
echo     psql %SCHOOL_CONN% -c "\dt school_*"
echo   College tables in college DB:
echo     psql %COLLEGE_CONN% -c "\dt college_*"
echo   Check no school_* remain in college:
echo     psql %COLLEGE_CONN% -c "\dt"
echo.

:CANCEL
echo Operation cancelled or completed.
