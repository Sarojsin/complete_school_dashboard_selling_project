-- Add PARENT value to userrole enum
ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'PARENT';
