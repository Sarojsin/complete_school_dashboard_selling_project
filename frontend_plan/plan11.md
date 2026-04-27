# Plan 11: Library Page Enhancement

## Objective
Enhance library pages to match backup/templates quality with overdue alerts and stats.

## Current State (React)
- LibraryDashboard exists with basic summary
- Books page exists
- No overdue alerts
- No fines display
- No comprehensive stats

## Required Changes

### 11.1 Student Library View (in dashboard or separate page)

#### Current Borrowings Section
- List of borrowed books
- Due date for each
- Status badge (Active / Overdue)
- Return button

#### Overdue Alert
- Red alert box if any overdue
- Number of overdue books
- Total fines amount

#### Stats Summary
- Total books borrowed (all time)
- Books returned
- Currently active
- Total fines

### 11.2 Library Dashboard (for library staff)

#### Stats Row
1. **Total Books** - Count
2. **Available** - Count
3. **Borrowed** - Count
4. **Overdue** - Count

#### Quick Actions
- Add Book
- Issue Book
- Return Book
- View Overdue

#### Recent Activity
- Recent issues
- Recent returns

### 11.3 Books Catalog Page
- Search functionality
- Filter by category, availability
- Grid/list view toggle
- Book details modal

### 11.4 Issue/Return Pages Enhancement
- Student search
- Book selection
- Due date calculation
- Confirmation dialog

## Priority
MEDIUM - Important service

## Estimated Time
5-6 hours

## Files to Modify
- Enhance: `frontend/src/modules/school/school_library/pages/LibraryDashboard.jsx`
- Modify: `frontend/src/modules/school/school_library/pages/Books.jsx`
- Modify: `frontend/src/modules/school/school_library/pages/IssueBook.jsx`
- Modify: `frontend/src/modules/school/school_library/pages/ReturnBook.jsx`
- Modify: `frontend/src/modules/school/school_library/pages/Overdue.jsx`