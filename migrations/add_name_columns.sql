-- Migration: Add full_name columns to profile tables
-- Date: 2025-12-04

-- Add columns
ALTER TABLE students ADD COLUMN IF NOT EXISTS full_name VARCHAR(255);
ALTER TABLE teachers ADD COLUMN IF NOT EXISTS full_name VARCHAR(255);
ALTER TABLE parents ADD COLUMN IF NOT EXISTS full_name VARCHAR(255);
ALTER TABLE authorities ADD COLUMN IF NOT EXISTS full_name VARCHAR(255);

-- Populate from users table
UPDATE students SET full_name = (SELECT full_name FROM users WHERE users.id = students.user_id);
UPDATE teachers SET full_name = (SELECT full_name FROM users WHERE users.id = teachers.user_id);
UPDATE parents SET full_name = (SELECT full_name FROM users WHERE users.id = parents.user_id);
UPDATE authorities SET full_name = (SELECT full_name FROM users WHERE users.id = authorities.user_id);

-- Optional: Make columns NOT NULL after population (uncomment if desired)
-- ALTER TABLE students ALTER COLUMN full_name SET NOT NULL;
-- ALTER TABLE teachers ALTER COLUMN full_name SET NOT NULL;
-- ALTER TABLE parents ALTER COLUMN full_name SET NOT NULL;
-- ALTER TABLE authorities ALTER COLUMN full_name SET NOT NULL;
