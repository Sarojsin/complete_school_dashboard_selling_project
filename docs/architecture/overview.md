# System Architecture

## Overview

The College Management System is a modular, multi-tenant application built with FastAPI that manages both school and college operations. The system uses a dual-database architecture to maintain separation between school and college data while sharing common authentication and user management.

## High-Level Architecture

```mermaid
graph TB
    %% Frontend Layer
    subgraph "Frontend Layer"
        React[React Application<br/>Portals: School/College]
        Mobile[Mobile App<br/>(Future)]
    end

    %% API Gateway / Load Balancer
    subgraph "API Gateway"
        Nginx[Nginx Reverse Proxy<br/>SSL Termination<br/>Rate Limiting]
    end

    %% Application Layer
    subgraph "Application Layer"
        FastAPI[FastAPI Application<br/>REST API<br/>Authentication]

        subgraph "Core Modules"
            Auth[Authentication &<br/>Authorization]
            Shared[Shared Utilities<br/>Logger, Health, Audit]
        end

        subgraph "School Modules"
            SchoolCore[Core School<br/>Students, Teachers, Classes]
            SchoolLib[Library Management]
            SchoolExam[Exam Management]
            SchoolAttendance[Attendance Tracking]
            SchoolTransport[Transport Management]
            SchoolCanteen[Canteen Services]
            SchoolAlumni[Alumni Relations]
        end

        subgraph "College Modules"
            CollegeCore[Core College<br/>Faculty, Students, Programs]
            CollegeExam[Exam Section<br/>Results & Notices]
            CollegeAccount[Account Section<br/>Fee Management]
            CollegeEnroll[Enrollment Management]
            CollegeHostel[Hostel Management]
            CollegeLab[Lab Equipment]
            CollegeResearch[Research & Patents]
            CollegePlacement[Placement Services]
        end
    end

    %% Data Layer
    subgraph "Data Layer"
        subgraph "Primary Databases"
            SchoolDB[(SQLite<br/>school.db<br/>School Data)]
            CollegeDB[(PostgreSQL<br/>college.db<br/>College Data)]
        end

        subgraph "Supporting Services"
            Redis[(Redis<br/>Caching & Sessions<br/>Optional)]
            S3[(AWS S3<br/>File Storage &<br/>Backups)]
        end
    end

    %% External Services
    subgraph "External Services"
        Sentry[Sentry<br/>Error Tracking]
        Prometheus[Prometheus<br/>Metrics Monitoring]
        SMTP[SMTP Server<br/>Email Notifications]
    end

    %% Connections
    React --> Nginx
    Mobile --> Nginx
    Nginx --> FastAPI

    FastAPI --> Auth
    FastAPI --> Shared
    FastAPI --> SchoolCore
    FastAPI --> SchoolLib
    FastAPI --> SchoolExam
    FastAPI --> SchoolAttendance
    FastAPI --> SchoolTransport
    FastAPI --> SchoolCanteen
    FastAPI --> SchoolAlumni

    FastAPI --> CollegeCore
    FastAPI --> CollegeExam
    FastAPI --> CollegeAccount
    FastAPI --> CollegeEnroll
    FastAPI --> CollegeHostel
    FastAPI --> CollegeLab
    FastAPI --> CollegeResearch
    FastAPI --> CollegePlacement

    Auth --> SchoolDB
    Auth --> CollegeDB
    SchoolCore --> SchoolDB
    SchoolLib --> SchoolDB
    SchoolExam --> SchoolDB
    SchoolAttendance --> SchoolDB
    SchoolTransport --> SchoolDB
    SchoolCanteen --> SchoolDB
    SchoolAlumni --> SchoolDB

    CollegeCore --> CollegeDB
    CollegeExam --> CollegeDB
    CollegeAccount --> CollegeDB
    CollegeEnroll --> CollegeDB
    CollegeHostel --> CollegeDB
    CollegeLab --> CollegeDB
    CollegeResearch --> CollegeDB
    CollegePlacement --> CollegeDB

    FastAPI --> Redis
    FastAPI --> S3
    FastAPI --> Sentry
    FastAPI --> Prometheus
    FastAPI --> SMTP

    style FastAPI fill:#e1f5fe
    style Auth fill:#f3e5f5
    style Shared fill:#fff3e0
    style SchoolCore fill:#e8f5e8
    style CollegeCore fill:#fff8e1
    style SchoolDB fill:#e8f5e8
    style CollegeDB fill:#fff8e1
    style Redis fill:#fce4ec
    style S3 fill:#f3e5f5
```

## Module Architecture

### Shared Components
```
modules/shared/
├── config.py          # Application configuration
├── database.py        # Database connections
├── models.py          # Shared models (User, mixins)
├── logger.py          # Structured logging
├── middleware/        # Custom middleware
│   ├── correlation_id.py
│   ├── audit_middleware.py
├── rate_limit.py      # Rate limiting
├── health.py          # Health checks
├── sentry.py          # Error tracking
├── audit.py           # Audit logging models
└── audit_logger.py    # Audit logging service
```

### School Modules
```
modules/school/
├── school_teacher/    # Teacher management
├── school_student/    # Student management
├── school_parent/     # Parent management
├── school_authority/  # School authorities
├── school_account_section/  # Fee management
├── school_library/    # Library management
├── school_exam_section/  # Exam management
├── school_attendance/ # Attendance tracking
├── school_courses/    # Course management
├── school_assignments/ # Assignment management
├── school_tests/      # Test management
├── school_notices/    # Notice management
├── school_grades/     # Grade management
├── school_notes/      # Study notes
├── school_videos/     # Video content
├── school_hod/        # Head of Department
├── school_groups/     # Study groups
├── school_chat/       # Communication
├── school_timetable/  # Timetable management
├── school_dashboard/  # Dashboard views
└── school_transport/  # Transport management
```

### College Modules
```
modules/college/
├── college_faculty/   # Faculty management
├── college_students/  # Student management
├── college_departments/  # Department management
├── college_programs/  # Program management
├── college_semesters/ # Semester management
├── college_courses/   # Course management
├── college_enrollments/  # Enrollment management
├── college_exam_section/ # Exam results & notices
├── college_account_section/  # Fee management
├── college_registrar/ # Registrar functions
├── college_hod/       # College HOD
├── college_dean/      # Dean management
├── college_hostel/    # Hostel management
├── college_lab/       # Lab equipment
├── college_research/  # Research management
├── college_placement/ # Placement services
└── college_semesters/ # Semester management
```

## Data Flow Architecture

### Authentication Flow
```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Auth
    participant Database
    participant Redis

    Client->>FastAPI: POST /auth/login
    FastAPI->>Auth: validate_credentials()
    Auth->>Database: SELECT user
    Database-->>Auth: user_data
    Auth->>Auth: generate_jwt_token()
    Auth-->>FastAPI: jwt_token
    FastAPI->>Redis: cache_session (optional)
    FastAPI-->>Client: token + user_info
```

### API Request Flow
```mermaid
sequenceDiagram
    participant Client
    participant Nginx
    participant FastAPI
    participant Middleware
    participant Module
    participant Database
    participant Audit

    Client->>Nginx: HTTPS Request
    Nginx->>FastAPI: Forward Request

    FastAPI->>Middleware: Correlation ID
    FastAPI->>Middleware: Rate Limiting
    FastAPI->>Middleware: Audit Logging

    FastAPI->>Module: Business Logic
    Module->>Database: Query/Execute
    Database-->>Module: Results

    Module-->>FastAPI: Response
    FastAPI->>Audit: Log Action (async)
    FastAPI-->>Client: JSON Response
```

## Database Architecture

### Dual Database Design
- **School Database (SQLite)**: Lightweight, file-based, suitable for school operations
- **College Database (PostgreSQL)**: Robust, concurrent, suitable for complex college operations
- **Shared User Table**: Authentication data shared between both systems

### Schema Relationships
```mermaid
erDiagram
    users ||--o{ school_students : "belongs_to"
    users ||--o{ teachers : "belongs_to"
    users ||--o{ school_parents : "belongs_to"
    users ||--o{ school_authorities : "belongs_to"

    users ||--o{ college_students : "belongs_to"
    users ||--o{ college_faculty : "belongs_to"

    school_students ||--o{ school_course_enrollments : "enrolls_in"
    school_courses ||--o{ school_course_enrollments : "has_students"

    college_students ||--o{ college_enrollments : "enrolls_in"
    college_courses ||--o{ college_enrollments : "has_students"

    college_departments ||--o{ college_programs : "contains"
    college_programs ||--o{ college_semesters : "has"
    college_semesters ||--o{ college_courses : "offers"

    college_faculty ||--o{ college_courses : "teaches"
    college_faculty ||--o{ college_departments : "belongs_to"
```

## Security Architecture

### Authentication & Authorization
- **JWT Tokens**: Stateless authentication with expiration
- **Role-Based Access**: Hierarchical permissions (admin > dean > faculty > student)
- **Portal Separation**: School vs College access control
- **Session Management**: Optional Redis-based sessions

### Security Layers
```mermaid
graph TD
    A[Client Request] --> B{Nginx}
    B --> C{CORS Check}
    C --> D{Rate Limiting}
    D --> E{JWT Validation}
    E --> F{Role Authorization}
    F --> G{Resource Access}
    G --> H[Business Logic]
    H --> I{Audit Logging}
    I --> J[Response]

    style B fill:#e1f5fe
    style D fill:#fff3e0
    style E fill:#e8f5e8
    style F fill:#fff8e1
    style I fill:#fce4ec
```

## Deployment Architecture

### Production Stack
```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Nginx Load Balancer<br/>SSL Termination<br/>Rate Limiting]
    end

    subgraph "Application Servers"
        App1[FastAPI App<br/>Server 1]
        App2[FastAPI App<br/>Server 2]
        AppN[FastAPI App<br/>Server N]
    end

    subgraph "Databases"
        SchoolDB[(SQLite<br/>School DB)]
        CollegeDB[(PostgreSQL<br/>College DB<br/>Primary)]
        CollegeReplica[(PostgreSQL<br/>Read Replica)]
    end

    subgraph "Supporting Services"
        Redis[(Redis<br/>Cache & Sessions)]
        S3[(AWS S3<br/>File Storage)]
        Backup[(Backup Storage)]
    end

    subgraph "Monitoring"
        Prometheus[Prometheus<br/>Metrics]
        Grafana[Grafana<br/>Dashboards]
        Sentry[Sentry<br/>Error Tracking]
    end

    LB --> App1
    LB --> App2
    LB --> AppN

    App1 --> CollegeDB
    App2 --> CollegeDB
    AppN --> CollegeDB

    App1 --> SchoolDB
    App2 --> SchoolDB
    AppN --> SchoolDB

    CollegeDB --> CollegeReplica

    App1 --> Redis
    App2 --> Redis
    AppN --> Redis

    App1 --> S3
    App2 --> S3
    AppN --> S3

    App1 --> Backup
    App2 --> Backup
    AppN --> Backup

    Prometheus --> App1
    Prometheus --> App2
    Prometheus --> AppN

    Grafana --> Prometheus
    Sentry --> App1
    Sentry --> App2
    Sentry --> AppN
```

## Technology Stack

### Backend
- **Framework**: FastAPI (async Python web framework)
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy (async support)
- **Databases**: SQLite (school), PostgreSQL (college)
- **Authentication**: JWT tokens with role-based access
- **Caching**: Redis (optional)
- **File Storage**: Local filesystem with S3 backup

### Frontend
- **Framework**: React with TypeScript
- **State Management**: Redux/Context API
- **Styling**: Tailwind CSS
- **Routing**: React Router
- **API Client**: Axios with interceptors

### DevOps & Monitoring
- **Containerization**: Docker
- **Orchestration**: Docker Compose (development)
- **Load Balancing**: Nginx
- **Monitoring**: Prometheus + Grafana
- **Error Tracking**: Sentry
- **Logging**: Structured JSON logs
- **CI/CD**: GitHub Actions (future)

### Security
- **HTTPS**: SSL/TLS encryption
- **Rate Limiting**: SlowAPI with Redis storage
- **Input Validation**: Pydantic schemas
- **CORS**: Configurable cross-origin policies
- **Audit Logging**: Complete transaction tracking
- **Soft Deletes**: Data recovery capabilities

## Development Workflow

### Local Development
```mermaid
graph LR
    A[Developer] --> B[Git Clone]
    B --> C[Install Dependencies]
    C --> D[Setup Environment]
    D --> E[Run Migrations]
    E --> F[Start Application]
    F --> G[Run Tests]
    G --> H[Code Review]
    H --> I[Merge to Main]
```

### CI/CD Pipeline (Future)
```mermaid
graph LR
    A[Push to Git] --> B[Run Tests]
    B --> C[Security Scan]
    C --> D[Build Docker Image]
    D --> E[Deploy to Staging]
    E --> F[Integration Tests]
    F --> G[Deploy to Production]
    G --> H[Health Checks]
    H --> I[Monitoring Alerts]
```

## Performance Considerations

### Database Optimization
- **Connection Pooling**: SQLAlchemy async engine
- **Query Optimization**: Selective field loading
- **Indexing**: Strategic indexes on frequently queried fields
- **Read Replicas**: PostgreSQL read replicas for reporting

### Caching Strategy
- **Redis Caching**: Frequently accessed data
- **Application Cache**: In-memory LRU cache for static data
- **CDN**: Static assets served via CDN

### Scalability Features
- **Horizontal Scaling**: Stateless application design
- **Database Sharding**: Future partitioning strategy
- **Microservices Ready**: Modular architecture supports decomposition

## Backup & Recovery

### Automated Backup Strategy
- **School DB**: SQLite backup with compression (daily)
- **College DB**: PostgreSQL pg_dump (daily)
- **Retention**: 30 days with weekly archives
- **Storage**: Local with S3 offsite backup

### Disaster Recovery
- **Recovery Time Objective**: < 15 minutes for critical data
- **Recovery Point Objective**: < 1 hour data loss
- **Failover**: Database replication and automatic failover

## Compliance & Security

### Data Protection
- **GDPR Compliance**: Data minimization and user rights
- **Encryption**: Data at rest and in transit
- **Audit Trails**: Complete user action logging
- **Access Controls**: Principle of least privilege

### Security Standards
- **OWASP Top 10**: Protection against common vulnerabilities
- **Input Validation**: Comprehensive request sanitization
- **Rate Limiting**: DoS and brute force protection
- **Secure Headers**: HTTP security headers implementation

This architecture provides a scalable, secure, and maintainable foundation for the College Management System, supporting both school and college operations with enterprise-grade features and monitoring capabilities.