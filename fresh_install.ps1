# Fresh PostgreSQL Database Installation Script
# Run this in PowerShell: .\fresh_install.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FRESH DATABASE INSTALLATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Load environment variables
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -notmatch '^#' -and $_ -match '=') {
            $key, $value = $_ -split '=', 2
            $env:$key.Trim() = $value.Trim('"').Trim("'")
        }
    }
}

# Database configuration
$dbHost = "localhost"
$dbPort = "5432"
$dbUser = "user"
$dbPass = "tara"
$dbName = "college_sell_db"

$adminConn = "postgresql://$dbUser:$dbPass@$dbHost:$dbPort/postgres"
$appConn = "postgresql://$dbUser:$dbPass@$dbHost:$dbPort/$dbName"

Write-Host "Target Database: $dbName" -ForegroundColor Yellow
Write-Host "Host: $dbHost`:$dbPort" -ForegroundColor Yellow
Write-Host ""

# Ask for confirmation
$confirm = Read-Host "This will DROP and RECREATE the database. Continue? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Cancelled." -ForegroundColor Red
    exit 0
}

# Step 1: Drop existing database
Write-Host "`n[1/5] Dropping existing database..." -ForegroundColor Gray
psql $adminConn -c "DROP DATABASE IF EXISTS `"$dbName`";" 2>$null
Write-Host "  [OK]" -ForegroundColor Green

# Step 2: Create fresh database
Write-Host "[2/5] Creating fresh database..." -ForegroundColor Gray
$result = psql $adminConn -c "CREATE DATABASE `"$dbName`";" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Failed to create database" -ForegroundColor Red
    Write-Host $result -ForegroundColor Red
    exit 1
}
Write-Host "  [OK]" -ForegroundColor Green

# Step 3: Enable extensions
Write-Host "[3/5] Enabling PostgreSQL extensions..." -ForegroundColor Gray
psql $appConn -c "CREATE EXTENSION IF NOT EXISTS pg_trgm; CREATE EXTENSION IF NOT EXISTS `"uuid-ossp`";" 2>$null
Write-Host "  [OK]" -ForegroundColor Green

# Step 4: Create core foundation
Write-Host "[4/5] Creating core foundation tables..." -ForegroundColor Gray
if (Test-Path "core_foundation_tables.sql") {
    psql $appConn -f "core_foundation_tables.sql" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Core tables created" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] Failed to create core tables" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  [ERROR] core_foundation_tables.sql not found!" -ForegroundColor Red
    exit 1
}

# Step 5: Execute all plan files in order
Write-Host "[5/5] Executing schema plans..." -ForegroundColor Gray

$planFiles = @(
    "plan1_academic_core_postgres.sql",
    "plan2_library_postgres.sql",
    "plan3_system_admin_postgres.sql",
    "plan4_transport_postgres.sql",
    "plan5_canteen_postgres.sql",
    "plan6_alumni_placement_postgres.sql",
    "plan7_welfare_discipline_postgres.sql",
    "plan8_assets_postgres.sql",
    "plan9_events_communication_postgres.sql",
    "plan10_reporting_postgres.sql"
)

$success = 0
$errors = 0

for ($i = 0; $i -lt $planFiles.Count; $i++) {
    $file = $planFiles[$i]
    if (Test-Path $file) {
        Write-Host "  [$($i+1)/$($planFiles.Count)] $file..." -ForegroundColor Gray -NoNewline
        $output = psql $appConn -f $file 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host " [OK]" -ForegroundColor Green
            $success++
        } else {
            Write-Host " [ERROR]" -ForegroundColor Red
            # Check if error is just "already exists" (may be OK)
            if ($output -match 'already exists') {
                Write-Host "    (Table already exists - usually OK)" -ForegroundColor Yellow
            } else {
                # Show first error line
                $firstError = $output -split "`n" | Select-Object -First 1
                if ($firstError) {
                    Write-Host "    $firstError" -ForegroundColor Red
                }
                $errors++
            }
        }
    } else {
        Write-Host "  [$($i+1)/$($planFiles.Count)] $file - NOT FOUND, skipping" -ForegroundColor Yellow
        $errors++
    }
}

# Verification
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "VERIFICATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$tableCount = (psql $appConn -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';" 2>$null).Trim()
Write-Host "`nTotal tables created: $tableCount" -ForegroundColor Green

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Database: $dbName"
Write-Host "  Core foundation: CREATED"
Write-Host "  Schema plans: $success/10 successful"
Write-Host "  Total tables: $tableCount"
Write-Host ""

if ($errors -eq 0) {
    Write-Host "[SUCCESS] Database fully installed!" -ForegroundColor Green
} else {
    Write-Host "[WARNING] $errors schema(s) had issues" -ForegroundColor Yellow
    Write-Host "Check above errors. Database may be partially functional." -ForegroundColor Yellow
}

Write-Host "`nConnect with pgAdmin or your application:"
Write-Host "  postgresql://$dbUser:*@$dbHost`:$dbPort/$dbName" -ForegroundColor Cyan
Write-Host ""

Pause
