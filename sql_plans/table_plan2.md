# Table Plan 2: Library Management System

## Overview
Complete library module with catalog, circulation, reservations, and patron management.

## Tables (10)

### Book Catalog
- `college_books` - Master book catalog (title, author, ISBN, metadata)
- `college_book_copies` - Physical copy inventory with barcodes
- `college_book_categories` - Subject/genre classification

### Circulation
- `college_book_loans` - Active and historical borrow records
- `college_book_reservations` - Hold requests and queue management
- `college_library_cards` - Student/faculty library accounts with limits

### Administration
- `college_fines` - Overdue fines and payment tracking
- `college_library_settings` - Loan periods, fine rates, limits
- `college_library_logs` - Circulations audit trail

## Dependencies
- Requires `college_students` and `college_teachers` from core (Plan 1)
- Optional: `college_notices` for library announcements

## Estimated Complexity
High - Complex business logic for reservations, fines, and availability.