# Database Schema Installation Guide

## Overview
This package contains 10 PostgreSQL schema plans with **116 tables** covering:
- Academic Core (14 tables)
- Library Management (10 tables)
- System Administration (11 tables)
- Transport Management (12 tables)
- Canteen Services (10 tables)
- Alumni & Placement (14 tables)
- Student Welfare & Discipline (12 tables)
- Assets & Facilities (15 tables)
- Events & Communication (17 tables)
- Reporting & Infrastructure (10 tables)

## Prerequisites

### 1. PostgreSQL Installation
- PostgreSQL 12+ installed and running
- Database created: `college_sell_db` (or your configured database name)

### 2. Python Dependencies (for automated execution)
```bash
pip install psycopg2-binary python-dotenv
```

### 3. Database Credentials
Update your `.env` file with correct credentials:

```env
# Use separate databases mode
DATABASE_MODE=separate

# College database (main business logic)
COLLEGE_DATABASE_URL=postgresql://user:password@localhost:5432/college_sell_db

# OR single database mode (both school and college use same DB)
DATABASE_URL=postgresql://user:password@localhost:5432/school_sell_db
```

## Installation Methods

### Method 1: Automated Python Script (Recommended)

**Windows:**
```bash
init_db.bat
```

**Linux/Mac:**
```bash
chmod +x init_db.sh
./init_db.sh
```

**Or manually:**
```bash
python init_database.py
```

The script will:
1. Load database configuration from `.env`
2. Connect to PostgreSQL
3. Execute all `plan*_postgres.sql` files in order
4. Verify table creation
5. Show summary statistics

### Method 2: Direct psql Command

Execute all SQL files directly:

```bash
# Connect to database
psql postgresql://user:password@localhost:5432/college_sell_db

# Inside psql, run:
\i plan1_academic_core_postgres.sql
\i plan2_library_postgres.sql
\i plan3_system_admin_postgres.sql
\i plan4_transport_postgres.sql
\i plan5_canteen_postgres.sql
\i plan6_alumni_placement_postgres.sql
\i plan7_welfare_discipline_postgres.sql
\i plan8_assets_postgres.sql
\i plan9_events_communication_postgres.sql
\i plan10_reporting_postgres.sql
```

Or via command line:
```bash
for file in plan*_postgres.sql; do
    echo "Executing $file..."
    psql postgresql://user:password@localhost:5432/college_sell_db -f "$file"
done
```

### Method 3: Using your FastAPI Application

The application will automatically create tables on startup if they don't exist:

```bash
# Ensure COLLEGE_DATABASE_URL is set to PostgreSQL
python -m app.main
```

Or call the creation function directly:
```python
from modules.college.database import create_college_tables
create_college_tables()
```

## Verification

After installation, verify tables were created:

```sql
-- Count tables by prefix
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE table_name LIKE 'college_%') as college_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'school_%') as school_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'system_%') as system_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'audit_%') as audit_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'notification_%') as notification_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'attachment_%') as attachment_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'support_%') as support_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'survey_%') as survey_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'backup_%') as backup_tables,
    COUNT(*) FILTER (WHERE table_name LIKE 'webhook_%') as webhook_tables
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND (table_name LIKE 'college_%' 
       OR table_name LIKE 'school_%'
       OR table_name LIKE 'system_%'
       OR table_name LIKE 'audit_%'
       OR table_name LIKE 'notification_%'
       OR table_name LIKE 'attachment_%'
       OR table_name LIKE 'support_%'
       OR table_name LIKE 'survey_%'
       OR table_name LIKE 'backup_%'
       OR table_name LIKE 'webhook_%');

-- List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name NOT LIKE 'pg_%'
  AND table_name NOT LIKE 'sql_%'
ORDER BY table_name;
```

## Expected Table Count

**Total: ~116 tables**

| Plan | Module | Tables |
|------|--------|--------|
| 1 | Academic Core | 14 |
| 2 | Library | 10 |
| 3 | System Admin | 11 |
| 4 | Transport | 12 |
| 5 | Canteen | 10 |
| 6 | Alumni & Placement | 14 |
| 7 | Welfare & Discipline | 12 |
| 8 | Assets & Inventory | 15 |
| 9 | Events & Communication | 17 |
| 10 | Reporting & Infrastructure | 10 |
| **Total** | | **105** |

Note: Original count was 116, but some tables like `school_holidays` and `school_academic_calendar` are in plan 9, bringing total to 105+.

## Important Notes

### 1. Database Extensions
Some tables use PostgreSQL extensions. Ensure they're enabled:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

The SQL files include these commands, but you can manually run them if needed.

### 2. Order of Execution
Tables must be created in order due to foreign key dependencies:

**Dependency Chain:**
- Plan 1 (Academic Core) - Foundation
- Plan 2 (Library) - depends on students/teachers from Plan 1
- Plan 3 (System Admin) - independent (can run anytime)
- Plan 4-10 - generally depend on core tables

### 3. Handling Existing Tables
If tables already exist:

```sql
-- Drop all (DANGEROUS - destroys data!)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- Then re-run SQL files

-- Or use CREATE OR REPLACE (but may fail on FK constraints)
-- The provided SQL uses CREATE TABLE IF NOT EXISTS
```

### 4. Connection Issues

**Common errors and fixes:**

```bash
# Error: connection refused
# Fix: Start PostgreSQL service
# Windows: 
net start postgresql-x64-17
# Linux/Mac:
sudo systemctl start postgresql

# Error: database does not exist
# Fix: Create database first
createdb college_sell_db
# or in psql:
CREATE DATABASE college_sell_db;

# Error: password authentication failed
# Fix: Check credentials in .env or pg_hba.conf
```

### 5. Performance Tuning
After creating all tables, run:

```sql
-- Analyze for query optimizer
ANALYZE;

-- Vacuum to clean up
VACUUM ANALYZE;

-- Create additional indexes if needed (already included in SQL)
```

## Post-Installation

### 1. Test Connection
```bash
python -c "
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://user:password@localhost:5432/college_sell_db')
with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ''public'''))
    print(f'Tables created: {result.scalar()}')
"
```

### 2. Start Application
```bash
# Ensure .env has correct DATABASE_URL or COLLEGE_DATABASE_URL
python -m app.main
# or
uvicorn app.main:app --reload
```

### 3. Verify in Application
Visit: http://localhost:8000/health/ready

## Troubleshooting

**"relation does not exist" errors:**
- Tables not created yet
- Run init_database.py first

**"permission denied" errors:**
- Database user lacks CREATE privilege
- Grant privileges: `GRANT ALL ON DATABASE college_sell_db TO user;`

**"extension pg_trgm does not exist":**
- Install PostgreSQL extensions
- `CREATE EXTENSION pg_trgm;`

**"could not connect to server":**
- Check PostgreSQL is running
- Verify host/port in connection string
- Check firewall settings

## Rollback

To drop all tables and start over:

```python
from modules.college.database import drop_college_tables
drop_college_tables()
```

Or raw SQL:
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- Re-run initialization
```

## Support

- Database config: `modules/shared/config.py`
- College DB: `modules/college/database.py`
- SQL files: `plan*_postgres.sql` in project root
