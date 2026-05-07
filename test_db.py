#!/usr/bin/env python3

"""
Basic database connectivity test for college module
"""

import sqlite3

def test_college_tables():
    """Test that college tables exist in database"""
    conn = sqlite3.connect('school_sell.db')
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    college_tables = [t for t in tables if t.startswith('college_')]
    print(f"Found {len(college_tables)} college tables:")
    for table in sorted(college_tables):
        print(f"  - {table}")

    # Check expected tables
    expected = [
        "college_departments", "college_faculty", "college_programs",
        "college_semesters", "college_courses", "college_students",
        "college_enrollments", "college_exam_results", "college_exam_notices",
        "college_faculty_payments", "college_fee_structures", "college_fee_records"
    ]

    missing = [t for t in expected if t not in tables]
    if missing:
        print(f"\nMissing tables: {missing}")
    else:
        print("\nAll expected college tables exist!")

    conn.close()

if __name__ == "__main__":
    test_college_tables()