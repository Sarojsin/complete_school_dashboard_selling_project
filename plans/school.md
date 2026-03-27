# School Management System - Detailed Role Documentation

**Last Updated:** 2026-03-22  
**Author:** Saroj Singh Dhami

---

## Overview

This document describes the complete flow and responsibilities of each role in the school management system. It explains WHAT each role does and HOW they perform their duties.

---

## 1. User Roles in School System

### 1.1 Authority (School Administration)
### 1.2 Exam Section
### 1.3 Account Section
### 1.4 Teachers
### 1.5 Students
### 1.6 Parents
### 1.7 Academic Levels (Class/Grade Structure)

---

## 2. Authority (School Administrator)

### What Authority Does

The Authority is the highest-level management role in the school system. They have complete control over all school operations.

### Core Responsibilities

#### 2.1 User Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Create Users | Add new students, teachers, parents | Authority fills registration form with user details |
| Edit Users | Modify user information | Authority searches user and updates fields |
| Delete Users | Remove users from system | Authority selects user and confirms deletion |
| Assign Roles | Define user roles (teacher, student, parent) | Authority selects role during user creation |
| Manage Permissions | Control access levels | Authority grants/revokes specific permissions |

#### 2.2 Teacher Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Assign Classes | Give teachers their teaching responsibilities | Authority selects teacher and assigns class(es) |
| Set Subjects | Define which subject each teacher teaches | Authority maps teacher to subject for each class |
| View Performance | Monitor teacher activities | Authority views attendance records, grades entered |
| Approve Leaves | Handle teacher leave requests | Authority receives request and approves/rejects |

#### 2.3 Student Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Admit Students | Add new students to school | Authority fills admission form with student details |
| Assign Classes | Place students in appropriate grade/section | Authority selects grade and section |
| Assign Class Teacher | Assign a teacher as class in-charge | Authority selects teacher for each class |
| View All Data | Access complete student records | Authority searches by name, ID, or class |
| Transfer Students | Move students between classes/sections | Authority initiates transfer and confirms |
| Promote Students | Move students to next grade | Authority runs promotion process at year-end |

#### 2.4 Academic Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Create Classes | Set up new grade levels and sections | Authority defines grade (1-12) and sections (A, B, C) |
| Create Subjects | Add subjects to curriculum | Authority creates subject with name, code, type |
| Define Timetable | Set school schedule | Authority or delegated teacher creates timetable |
| Set Academic Calendar | Define terms, exams, holidays | Authority creates academic year with dates |

#### 2.5 Fee Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Create Fee Structure | Define fee for each grade | Authority sets tuition, lab, transport fees per class |
| Generate Fee Bills | Create fee invoices for students | System generates based on fee structure |
| Approve Waivers | Grant fee concessions | Authority reviews request and approves |
| View Payment Reports | See fee collection status | Authority views reports by class, date range |

#### 2.6 Notice Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Post Notices | Send announcements | Authority creates notice with title, content, priority |
| Target Audience | Select who sees notice | Authority chooses: all, teachers, students, parents |
| Schedule Notices | Set future publish date | Authority sets publish date/time |
| Archive Notices | Keep record of past notices | System automatically archives after expiry |

---

## 3. Exam Section

### What Exam Section Does

The Exam Section manages all examination-related activities including scheduling, conducting exams, and publishing results.

### Core Responsibilities

#### 3.1 Exam Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Create Exam | Set up new exam (Unit Test, Final, etc.) | Exam Section defines exam name, type, date range |
| Schedule Exams | Allocate dates/times for each subject | Exam Section assigns date, time, room for each subject |
| Allocate Seating | Assign exam seats to students | System generates seating arrangement |
| Monitor Exam | Track exam progress | Exam Section views attendance per exam |

#### 3.2 Question Paper Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Create Question Banks | Store questions by subject/chapter | Teachers submit, Exam Section approves |
| Generate Papers | Create exam papers from bank | Exam Section selects questions, sets marks |
| Set Exam Guidelines | Define rules (duration, passing marks) | Exam Section configures exam settings |

#### 3.3 Answer Sheet Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Distribute Papers | Send to teachers for evaluation | Exam Section assigns to subject teachers |
| Track Status | Monitor evaluation progress | System shows pending/evaluated count |
| Resolve Conflicts | Handle marking disputes | Exam Section reviews and decides |

#### 3.4 Result Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Enter Marks | Record student scores | Subject teachers enter, Exam Section verifies |
| Calculate Grades | Compute final grades | System calculates based on grading policy |
| Publish Results | Make results visible | Exam Section reviews and releases |
| Generate Reports | Create report cards | System compiles and generates PDF |

#### 3.5 Re-exam Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Schedule Re-exams | Plan supplementary exams | Exam Section sets dates for failed students |
| Process Improvements | Allow students to improve scores | Exam Section configures rules |

---

## 4. Account Section

### What Account Section Does

The Account Section manages all financial operations including fee collection, expense tracking, and salary payments.

### Core Responsibilities

#### 4.1 Fee Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Create Fee Structure | Define fees per grade | Authority sets fees, Account Section implements |
| Generate Invoices | Create fee bills for students | System generates monthly/term bills |
| Record Payments | Track fee payments | Account Section enters payment details |
| Send Reminders | Notify about due fees | System auto-sends SMS/email reminders |
| Process Refunds | Handle fee refunds | Account Section processes valid requests |

#### 4.2 Payment Tracking
| Task | Description | How It's Done |
|------|-------------|---------------|
| Track Pending | Monitor unpaid fees | System shows outstanding balances |
| Record Transactions | Log all financial entries | Account Section creates transaction records |
| Generate Receipts | Provide payment proof | System generates receipt on payment |
| Reconcile Accounts | Match records with bank | Account Section verifies transactions |

#### 4.3 Expense Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Record Expenses | Log school expenditures | Account Section enters expense details |
| Categorize | Classify expenses (salary, supplies, etc.) | Account Section selects category |
| Approve Payments | Authorize large expenses | Authority approves above threshold |
| Generate Reports | Financial statements | System compiles expense reports |

#### 4.4 Teacher Salary
| Task | Description | How It's Done |
|------|-------------|---------------|
| Set Salary Structure | Define pay scales | Authority sets rules, Account Section implements |
| Process Monthly Salary | Calculate and pay teachers | System calculates based on attendance, deductions |
| Handle Deductions | Tax, PF, other deductions | System automatically deducts configured amounts |
| Generate Payslips | Provide salary details | System generates payslip for each teacher |

#### 4.5 Financial Reports
| Task | Description | How It's Done |
|------|-------------|---------------|
| Income Statement | Revenue vs expenses | System calculates for date range |
| Fee Collection Report | Fee payments received | Report by class, date, mode |
| Expense Report | Spending by category | Detailed expense breakdown |
| Balance Sheet | Financial position | Assets and liabilities summary |

---

## 5. Teachers

### What Teachers Do

Teachers are responsible for classroom teaching, student assessment, and maintaining academic records for their assigned classes.

### Core Responsibilities

#### 5.1 Classroom Teaching
| Task | Description | How It's Done |
|------|-------------|---------------|
| Take Classes | Conduct lessons for assigned subjects | Teacher records class conducted |
| Upload Content | Share study materials | Teacher uploads notes, videos |
| Create Assignments | Give homework to students | Teacher creates with deadline |
| Conduct Tests | Administer class tests | Teacher creates and schedules |

#### 5.2 Attendance Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Mark Daily Attendance | Record student presence | Teacher marks present/absent for each class |
| Update Records | Correct attendance errors | Teacher edits with justification |
| View Reports | See attendance patterns | System generates class-wise reports |

#### 5.3 Student Assessment
| Task | Description | How It's Done |
|------|-------------|---------------|
| Enter Marks | Record test/exam scores | Teacher inputs marks for students |
| Grade Assignments | Evaluate homework | Teacher marks and provides feedback |
| Write Remarks | Add comments on student progress | Teacher writes qualitative feedback |

#### 5.4 Student Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| View Class Students | See enrolled students | Teacher views assigned class list |
| Track Progress | Monitor student performance | Teacher views grades, attendance |
| Communicate | Send messages to students/parents | Teacher sends via system |

#### 5.5 Resource Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| Upload Notes | Share study materials | Teacher uploads to course |
| Add Videos | Share video lessons | Teacher uploads video content |
| Manage Library | Book library resources | Teacher reserves/returns books |

---

## 6. Students

### What Students Do

Students are the primary users who access the system to view their academic information, submit assignments, and communicate with teachers.

### Core Responsibilities

#### 6.1 Academic Access
| Task | Description | How It's Done |
|------|-------------|---------------|
| View Timetable | See class schedule | Student logs in and views timetable |
| Access Study Materials | Download notes/videos | Student browses and downloads |
| View Assignments | See homework given | Student views assigned work |
| Submit Assignments | Upload completed work | Student uploads before deadline |
| Check Grades | View marks and grades | Student views results when published |

#### 6.2 Attendance
| Task | Description | How It's Done |
|------|-------------|---------------|
| View Attendance | See attendance record | Student views own attendance |
| Request Leave | Apply for leave | Student submits leave request |

#### 6.3 Fee Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| View Fee Details | See fee structure | Student views fee breakdown |
| Make Payment | Pay fees online | Student initiates payment |
| Download Receipt | Get payment proof | Student downloads receipt |

#### 6.4 Communication
| Task | Description | How It's Done |
|------|-------------|---------------|
| View Notices | Read announcements | Student views targeted notices |
| Chat with Teachers | Message teachers | Student initiates chat |
| Ask Questions | Clarify doubts | Student posts question |

---

## 7. Parents

### What Parents Do

Parents monitor their children's academic progress and communicate with teachers.

### Core Responsibilities

#### 7.1 Child Monitoring
| Task | Description | How It's Done |
|------|-------------|---------------|
| View Progress | See child's academic status | Parent logs in with child link |
| Check Attendance | Monitor class presence | Parent views attendance record |
| View Grades | See child's marks | Parent views published results |
| Track Assignments | Monitor homework | Parent sees assigned/completed work |

#### 7.2 Communication
| Task | Description | How It's Done |
|------|-------------|---------------|
| Contact Teachers | Message class teacher | Parent initiates conversation |
| Receive Notices | Get school updates | Parent views relevant notices |
| Meet Teachers | Request appointments | Parent schedules meeting |

#### 7.3 Fee Management
| Task | Description | How It's Done |
|------|-------------|---------------|
| View Fee | See child's fee details | Parent views fee breakdown |
| Make Payment | Pay child's fees | Parent initiates payment |
| Download Receipt | Get payment proof | Parent downloads receipt |

---

## 8. Academic Levels (Grade Structure)

### What It Defines

The level structure organizes students into grades (Class 1-12) with sections for manageable instruction.

### Level Hierarchy

```
School
├── Primary (Classes 1-5)
│   ├── Class 1 (Section A, B, C...)
│   ├── Class 2 (Section A, B, C...)
│   └── Class 5 (Section A, B, C...)
├── Lower Secondary (Classes 6-8)
│   ├── Class 6 (Section A, B...)
│   └── Class 8 (Section A, B...)
├── Secondary (Classes 9-10)
│   ├── Class 9 (Section A, B...)
│   └── Class 10 (Section A, B...)
└── Higher Secondary (Classes 11-12)
    ├── Class 11 (Science, Commerce, Arts)
    └── Class 12 (Science, Commerce, Arts)
```

### How Levels Work

| Level | Classes | Typical Age | Focus |
|-------|---------|-------------|-------|
| Primary | 1-5 | 5-10 years | Foundation, Basic literacy |
| Lower Secondary | 6-8 | 11-13 years | Core subjects, Skills |
| Secondary | 9-10 | 14-15 years | Board preparation |
| Higher Secondary | 11-12 | 16-17 years | Stream specialization |

### Class Management Flow

```
Authority Creates Class
        ↓
Assigns Class Teacher
        ↓
Defines Sections (A, B, C)
        ↓
Assigns Subjects to Class
        ↓
Admits Students to Class
        ↓
Teacher Takes Attendance
        ↓
Teacher Marks Grades
        ↓
Authority Promotes to Next Class
```

---

## 9. Data Flow Between Roles

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            AUTHORITY                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Create      │  │ Assign      │  │ Set Fee     │  │ Manage      │   │
│  │ Classes     │  │ Teachers    │  │ Structure   │  │ Academic    │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
└─────────┼────────────────┼────────────────┼────────────────┼──────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         EXAM SECTION                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Schedule    │  │ Distribute  │  │ Enter       │  │ Publish     │   │
│  │ Exams       │  │ Question    │  │ Marks       │  │ Results     │   │
│  │             │  │ Papers      │  │             │  │             │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
└─────────┼────────────────┼────────────────┼────────────────┼──────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          ACCOUNT SECTION                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Generate    │  │ Record      │  │ Process     │  │ Generate    │   │
│  │ Fee Bills   │  │ Payments    │  │ Salaries    │  │ Reports     │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
└─────────┼────────────────┼────────────────┼────────────────┼──────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            TEACHERS                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Take        │  │ Upload      │  │ Mark        │  │ Enter       │   │
│  │ Attendance  │  │ Content     │  │ Assignments │  │ Grades      │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
└─────────┼────────────────┼────────────────┼────────────────┼──────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           STUDENTS                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ View        │  │ Submit      │  │ View        │  │ Pay         │   │
│  │ Timetable   │  │ Assignments │  │ Grades      │  │ Fees        │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
└─────────┼────────────────┼────────────────┼────────────────┼──────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            PARENTS                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Monitor     │  │ View        │  │ Communicate │  │ Pay         │   │
│  │ Progress    │  │ Attendance  │  │ with Teacher│  │ Fees        │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Key Processes Summary

### 10.1 Student Admission Flow
1. Parent/Student submits admission form
2. Authority verifies documents
3. Authority creates student account
4. Authority assigns class and section
5. Account Section generates fee structure
6. Student receives login credentials

### 10.2 Exam Result Flow
1. Exam Section creates exam
2. Teachers enter marks
3. Exam Section verifies marks
4. Exam Section calculates grades
5. Authority approves publication
6. Students view results

### 10.3 Fee Payment Flow
1. Account Section generates fee bills
2. System sends payment reminders
3. Student/Parent makes payment
4. Account Section records payment
5. System generates receipt
6. Account Section reconciles accounts

---

## 11. Summary Matrix

| Role | Manages | Creates | Views | Approves |
|------|---------|---------|-------|----------|
| Authority | All | All | All | All |
| Exam Section | Exams | Exams, Results | All Exam Data | Results |
| Account Section | Fees, Salaries | Bills, Payslips | All Financial Data | Large Expenses |
| Teachers | Classes | Assignments, Grades | Assigned Classes | Own Content |
| Students | Own Work | Assignments | Own Data | - |
| Parents | Child Info | Requests | Child Data | - |

---

*End of School System Documentation*
