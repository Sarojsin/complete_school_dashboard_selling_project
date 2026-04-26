# Frontend Mapping 6: School Library Module

## Overview
Migration of Library Portal from Jinja templates to React.

## Backend API Source
**Prefix:** `/api/library`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/library/books | Create new book |
| GET | /api/library/books/{book_id} | Get book by ID |
| GET | /api/library/books | List books |
| PUT | /api/library/books/{book_id} | Update book |
| DELETE | /api/library/books/{book_id} | Delete book |
| POST | /api/library/loans | Issue book |
| GET | /api/library/loans/{loan_id}/return | Return book |
| GET | /api/library/loans/student/{student_id} | Get student loans |
| GET | /api/library/loans/overdue | Get overdue loans |
| GET | /api/library/summary | Get library summary |

## Additional Endpoints
**Books:** `/api/books`
- Search books
- Filter by category

## Old Jinja Templates (Source)
Location: `backup/templates/library/`
- dashboard.html
- books.html
- add_book.html
- issue_book.html
- return_book.html
- overdue.html
- profile.html

## Frontend Module Structure
```
frontend/src/modules/school/school_library/
├── api/
│   └── library.js       # ❌ MISSING - NEED TO CREATE
├── pages/
│   ├── Dashboard.jsx    # ❌ MISSING
│   ├── Books.jsx        # ❌ MISSING
│   ├── AddBook.jsx      # ❌ MISSING
│   ├── IssueBook.jsx    # ❌ MISSING
│   ├── ReturnBook.jsx   # ❌ MISSING
│   ├── Overdue.jsx      # ❌ MISSING
│   └── Profile.jsx      # ❌ MISSING
└── styles/
    └── library.css
```

## Frontend Pages - ALL MISSING ❌

### 1. Dashboard.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Library statistics
- Recent activities
- Quick links

**API Calls needed:**
```javascript
// Create api/library.js
- getLibraryDashboard() → GET /api/library/summary
- getRecentLoans() → GET /api/library/loans/recent
```

### 2. Books.jsx
**Status:** ❌ MISSING
**Features to implement:**
- List all books
- Search books
- Filter by category/author
- Book details
- Available copies count

**API Calls needed:**
```javascript
- getAllBooks() → GET /api/library/books
- searchBooks(query) → GET /api/library/books?search={query}
- getBookDetails(bookId) → GET /api/library/books/{book_id}
```

### 3. AddBook.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Add new book form
- Bulk import books
- Book categories

**API Calls needed:**
```javascript
- addBook(data) → POST /api/library/books
- updateBook(bookId, data) → PUT /api/library/books/{book_id}
- deleteBook(bookId) → DELETE /api/library/books/{book_id}
```

### 4. IssueBook.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Issue book to student
- Select student
- Select book
- Due date selection

**API Calls needed:**
```javascript
- issueBook(data) → POST /api/library/loans
  // data: { student_id, book_id, due_date }
- getAvailableBooks() → GET /api/library/books?available=true
- getStudents() → GET /api/students/
```

### 5. ReturnBook.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Return book form
- Scan/enter book ID
- Scan/enter student ID
- Late fee calculation

**API Calls needed:**
```javascript
- returnBook(loanId) → GET /api/library/loans/{loan_id}/return
- getActiveLoans() → GET /api/library/loans/active
- calculateFine(loanId) → GET /api/library/loans/{loan_id}/fine
```

### 6. Overdue.jsx
**Status:** ❌ MISSING
**Features to implement:**
- List overdue books
- Send reminder
- Calculate fines

**API Calls needed:**
```javascript
- getOverdueLoans() → GET /api/library/loans/overdue
- sendReminder(loanId) → POST /api/library/loans/{loan_id}/reminder
```

### 7. Profile.jsx
**Status:** ❌ MISSING
**Features to implement:**
- Librarian profile
- Edit profile

**API Calls needed:**
```javascript
- getProfile() → GET /api/library/profile
- updateProfile(data) → PUT /api/library/profile
```

## Data Schemas

### Book
```javascript
{
  id: number,
  title: string,
  author: string,
  isbn: string,
  publisher: string,
  category: string,
  total_copies: number,
  available_copies: number,
  shelf_location: string,
  price: number
}
```

### Loan
```javascript
{
  id: number,
  book_id: number,
  book_title: string,
  student_id: number,
  student_name: string,
  issue_date: string,
  due_date: string,
  return_date?: string,
  status: "active" | "returned" | "overdue",
  fine?: number
}
```

### Library Summary
```javascript
{
  total_books: number,
  total_students: number,
  books_issued: number,
  overdue_count: number,
  available_books: number
}
```

## Implementation Order
1. ❌ Dashboard - First
2. ❌ Books - Second
3. ❌ AddBook - Third
4. ❌ IssueBook - Fourth
5. ❌ ReturnBook - Fifth
6. ❌ Overdue - Sixth
7. ❌ Profile - Seventh

## Notes
- Library module is 0% complete - needs full implementation
- Need to create api/library.js first
- Key features: Book management, loan tracking, overdue management
