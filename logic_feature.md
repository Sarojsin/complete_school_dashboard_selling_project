# School Management System: Deep Dive Logic & Features

This document provides an exhaustive technical and functional breakdown of the School Management System, covering security protocols, specific business service implementations, and technical architecture.

---

## 1. Security & Authentication Framework

### 1.1 Dual-Token Authentication (JWT)
The system implements a robust stateless authentication mechanism using **JSON Web Tokens (JWT)**.
- **Access Tokens**: Short-lived (configured in `ACCESS_TOKEN_EXPIRE_MINUTES`) used for authorizing every request. Includes claims such as `sub` (user_id), `role`, and `type`.
- **Refresh Tokens**: Long-lived (configured in `REFRESH_TOKEN_EXPIRE_DAYS`) used to obtain new access tokens without requiring the user to re-enter credentials.
- **Verification Flow**: The `AuthService` decodes tokens using a `SECRET_KEY` and `HS256` algorithm. Role-based access is enforced by checking the `role` claim against the required permissions for each endpoint.

### 1.2 CSRF Protection Mechanism
A custom `CSRFMiddleware` secures the application against cross-site request forgery, particularly for the web interface:
- **Token Lifecycle**: A unique 32-byte `csrf_token` is generated and stored in the user's encrypted session upon the first visit.
- **Validation Logic**:
  - Automatically validates `POST`, `PUT`, `DELETE`, and `PATCH` methods.
  - **AJAX/Fetch**: Looks for the `X-CSRF-Token` header for modern API-driven requests.
  - **Form Submissions**: Supports standard HTML form posts through a JavaScript injector that dynamically adds the token as a hidden field.
- **Template Integration**: The token is injected into all Jinja2 templates via a context processor, making `csrf_token` available for any custom frontend logic.

---

## 2. Advanced Business Services

### 2.1 Attendance Intelligence (`AttendanceService`)
Attendance tracking goes beyond simple binary logging:
- **Monthly Reporting**: The system generates drill-down reports for parents and students. It calculates `total_days`, `present`, `absent`, and `late` counts for any given month/year.
- **Attendance Rate**: Dynamically calculates `(present_days / total_days) * 100` to help monitor student engagement trends.
- **Bulk Marking**: Teachers can use a single submission to mark attendance for an entire class roster, reducing administrative overhead and database load.

### 2.2 Grading & Academic Analytics (`GradeService`)
- **Automated Calculations**: Aggregates scores from both assignments and scheduled tests.
- **GPA & Letter Grades**: Uses the `GradeRepository` to map percentages to a 4.0 GPA scale and standard letter grades (A-F).
- **In-depth Analytics**: Provides teachers with cohort-level statistics, including class average, highest/lowest scores, and grade distribution (how many students got an 'A', 'B', etc.).

### 2.3 Online Testing Engine (`TestService`)
A high-integrity assessment module:
- **Auto-Grading Logic**: For Multiple Choice (MCQ) and True/False questions, the service matches student answers against stored `correct_answer` values in real-time.
- **Timer Management**: Tracks `started_at` for each student. The `calculate_time_remaining` logic ensures students cannot submit once their individual duration or the global `end_time` has elapsed.

---

## 3. Collaboration & Communication

### 3.1 Social Groups & Resource Sharing
The `Groups` module facilitates class-specific collaboration:
- **Access Control**: Groups are secured by unique alphanumeric codes. Only users with the code can join.
- **Resource Categorization**: Posts are classified as `NOTICE` (urgent announcements), `NOTE` (study materials), or `LINK` (external resources), allowing students to filter their feed.

### 3.2 Real-time Chat & Data Retention
- **WebSocket Protocol**: Built for low-latency, real-time messaging between students, teachers, and parents.
- **Storage Optimization**: The `ChatCleanupService` manages a retention policy (e.g., 30 or 90 days), automatically purging old messages to keep the database efficient while maintaining sufficient history for active conversations.

---

## 4. Technical Architecture

### 4.1 Model Relationships (SQLAlchemy)
The database follows a **User-Persona Pattern**:
- **Authentication Core**: The `User` table handles login, password hashing (Bcrypt), and global roles.
- **Persona Extension**: role-specific data is stored in `Student`, `Teacher`, `Parent`, and `Authority` tables, each linked back to the `User` table via a **1:1 relationship**.
- **Cascading Integrity**: Relationships are configured with `ondelete="CASCADE"` where appropriate, ensuring that deleting a student also cleans up their enrollments, grades, and attendance records.

### 4.2 Web vs. API Layering
- **Web Layer (`app/web/routers`)**: Focuses on the user interface, serving Jinja2 templates and handling browser-specific sessions and CSRF.
- **API Layer (`app/api/v1/endpoints`)**: A pure RESTful API returning JSON. This layer is designed for modularity, allowing for future mobile app or desktop client integration.

---

## 6. Functional Workflows (Step-by-Step)

### 6.1 The Lifecycle of an Assignment
1.  **Creation**: A Teacher creates an `Assignment` by specifying a `course_id`, `due_date`, and `target_classes` (e.g., "9A", "9B"). They can upload a reference PDF.
2.  **Notification**: Students in the target classes receive a notification through their dashboard.
3.  **Submission**: A Student uploads their work (file or text). The system records the `submitted_at` timestamp.
4.  **Grading**: The Teacher reviews the submission, assigns a `score`, and provides `feedback`.
5.  **Completion**: The Student’s `GradeRecord` is updated, and the assignment is marked as "Graded" in their portal.

### 6.2 The Journey of an Online Test
1.  **Preparation**: The Teacher defines a `Test` with a specific `duration` (in minutes) and a pool of `TestQuestions`.
2.  **Activation**: The test becomes available only between its `start_time` and `end_time`.
3.  **Execution**:
    - Once a student clicks "Start", a `TestSubmission` record is created with a `started_at` timestamp.
    - The frontend (via `calculate_time_remaining`) displays a countdown.
4.  **Submission & Auto-Grading**:
    - Upon submission, the `TestService` immediately grades objective questions.
    - If the user tries to submit after the time is up, the backend rejects it.
5.  **Analytics**: The `GradeService` aggregates the test score into the student's overall course performance.

### 6.3 Real-time Communication (Chat)
1.  **Connection**: Users establish a persistent WebSocket connection upon logging in.
2.  **Payload**: Messages are sent as JSON objects containing `receiver_id`, `content`, and optional `file_id`.
3.  **Persistence**: Every message is committed to the `ChatMessage` table for history, but tagged with an `expires_at` date for future cleanup.
4.  **Feedback**: The system sends a `delivery_receipt` back to the sender once the message is stored and emitted to the receiver.

---

## 7. Configuration & Environment Settings

The system is highly configurable via the `config/config.py` file, which utilizes Pydantic for validation:
- **`SECRET_KEY`**: Critical for JWT and CSRF signing.
- **`DATABASE_URL`**: Supports Async PostgreSQL drivers (`postgresql+asyncpg://`).
- **`MESSAGE_RETENTION_DAYS`**: Controls how long chat history is kept before being purged by the cleanup worker.
- **`FILE_UPLOAD_MAX_SIZE`**: Sets limits on assignment and profile picture uploads.

---

*Document finalized by GitHub Copilot on January 22, 2026*


