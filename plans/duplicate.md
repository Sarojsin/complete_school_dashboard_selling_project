API Endpoint Duplicates (7)
These endpoints appear in both the standard API modules and the admin API modules.

Method	Endpoint	Files
GET	/api/courses	courses.py, admin_academic.py
POST	/api/courses	courses.py, admin_academic.py
DELETE	/api/courses/{course_id}	courses.py, admin_academic.py
GET	/api/notices	notices.py, admin_notices.py
POST	/api/notices	notices.py, admin_notices.py
DELETE	/api/notices/{notice_id}	notices.py, admin_notices.py
GET	/api/stats	admin_dashboard.py, admin_academic.py
Web Route Duplicates (23)
These endpoints are defined both in authority.py and authority_crud.py under the /authority prefix.

Method	Endpoint
GET	/authority/students/add
POST	/authority/students/add
GET	/authority/students/{id}
GET	/authority/students/{id}/edit
POST	/authority/students/{id}/edit
POST	/authority/students/{id}/delete
GET	/authority/teachers/add
POST	/authority/teachers/add
GET	/authority/teachers/{id}
GET	/authority/teachers/{id}/edit
POST	/authority/teachers/{id}/edit
POST	/authority/teachers/{id}/delete
GET	/authority/courses/add
POST	/authority/courses/add
GET	/authority/courses/{id}
GET	/authority/courses/{id}/edit
POST	/authority/courses/{id}/edit
GET	/authority/notices/create
POST	/authority/notices/create
GET	/authority/notices/{id}
GET	/authority/notices/{id}/edit
POST	/authority/notices/{id}/edit