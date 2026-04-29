school_management_system/
├── modules/
│   ├── teacher/
│   │   ├── __init__.py
│   │   ├── models.py            # All teacher DB models
│   │   ├── schemas.py           # All teacher schemas
│   │   ├── repository.py        # Teacher data access
│   │   ├── service.py           # Teacher business logic
│   │   ├── api.py               # FastAPI routes
│   │   ├── web.py               # Web routes
│   │   ├── constants.py         # Teacher-specific constants
│   │   ├── exceptions.py        # Teacher-specific errors
│   │   ├── utils.py             # Teacher helper functions
│   │   ├── templates/           # Teacher HTML templates
│   │   │   ├── dashboard.html
│   │   │   ├── profile.html
│   │   │   └── attendance.html
│   │   └── tests/
│   │       ├── test_service.py
│   │       └── test_api.py
│   │
│   ├── student/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── api.py
│   │   ├── web.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── templates/
│   │   └── tests/
│   │
│   ├── exam/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── api.py
│   │   ├── web.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── templates/
│   │   └── tests/
│   │
│   ├── library/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── api.py
│   │   ├── web.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── templates/
│   │   └── tests/
│   │
│   ├── account/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── api.py
│   │   ├── web.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── templates/
│   │   └── tests/
│   │
│   ├── department/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── api.py
│   │   ├── web.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── tests/
│   │
│   └── shared/                   # Shared across modules
│       ├── __init__.py
│       ├── base/
│       │   ├── base_model.py
│       │   ├── base_repository.py
│       │   └── base_service.py
│       ├── auth/
│       │   ├── dependencies.py
│       │   ├── jwt.py
│       │   └── permissions.py
│       ├── database/
│       │   ├── connection.py
│       │   └── session.py
│       ├── config.py
│       ├── exceptions.py
│       └── utils.py
│
├── core/                        # Application core
│   ├── main.py
│   ├── dependencies.py
│   └── events.py
│
├── migrations/                  # Alembic migrations
├── static/                      # Global static files
├── tests/                       # Global tests
└── requirements.txt