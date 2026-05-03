"""
Load testing script using Locust
Run: locust -f scripts/locustfile.py --host=http://localhost:8000
Then open: http://localhost:8089 in browser
Set: users=50, spawn rate=5, run for 2 minutes

Pass criteria:
- p95 response time < 500ms with 50 concurrent users
- Error rate < 1%
- RPS (requests/sec) >= pre-migration baseline
"""

from locust import HttpUser, task, between, events
import random


class SchoolUser(HttpUser):
    """Simulates a school teacher or staff member."""
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login at start of each simulated user session."""
        # Try to login with test credentials
        response = self.client.post("/api/v1/auth/login", json={
            "username": "testteacher",
            "password": "test123"
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token", "")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            # Fallback - try with admin
            response = self.client.post("/api/v1/auth/login", json={
                "username": "admin",
                "password": "adminpass"
            })
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token", "")
                self.headers = {"Authorization": f"Bearer {self.token}"}
            else:
                self.token = ""
                self.headers = {}

    @task(3)
    def list_students(self):
        """List students - high priority"""
        if self.token:
            self.client.get("/api/v1/school/students/", headers=self.headers)

    @task(2)
    def list_attendance(self):
        """List attendance records"""
        if self.token:
            self.client.get("/api/v1/school/attendance/", headers=self.headers)

    @task(2)
    def list_teachers(self):
        """List teachers"""
        if self.token:
            self.client.get("/api/v1/school/teachers/", headers=self.headers)

    @task(1)
    def list_exams(self):
        """List exams"""
        if self.token:
            self.client.get("/api/v1/school/exams/", headers=self.headers)

    @task(1)
    def list_library(self):
        """List library books"""
        if self.token:
            self.client.get("/api/v1/school/library/", headers=self.headers)

    @task(1)
    def get_auth_me(self):
        """Get current user info"""
        if self.token:
            self.client.get("/api/v1/auth/me", headers=self.headers)


class AdminUser(HttpUser):
    """Simulates an administrator."""
    wait_time = between(2, 5)
    
    def on_start(self):
        """Login as admin"""
        response = self.client.post("/api/v1/auth/login", json={
            "username": "superadmin",
            "password": "adminpass"
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token", "")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = ""
            self.headers = {}

    @task(2)
    def dashboard(self):
        """Admin dashboard"""
        if self.token:
            self.client.get("/api/v1/admin/dashboard", headers=self.headers)

    @task(2)
    def list_users(self):
        """List all users"""
        if self.token:
            self.client.get("/api/v1/admin/users", headers=self.headers)

    @task(1)
    def get_audit_logs(self):
        """Get audit logs"""
        if self.token:
            self.client.get("/api/v1/admin/audit-logs", headers=self.headers)

    @task(1)
    def get_system_settings(self):
        """Get system settings"""
        if self.token:
            self.client.get("/api/v1/admin/settings", headers=self.headers)


class CollegeUser(HttpUser):
    """Simulates a college faculty member."""
    wait_time = between(2, 4)
    
    def on_start(self):
        """Login as college faculty"""
        response = self.client.post("/api/v1/auth/login", json={
            "username": "college_faculty",
            "password": "test123"
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token", "")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = ""
            self.headers = {}

    @task(3)
    def list_college_students(self):
        """List college students"""
        if self.token:
            self.client.get("/api/v1/college/students/", headers=self.headers)

    @task(2)
    def list_faculty(self):
        """List college faculty"""
        if self.token:
            self.client.get("/api/v1/college/faculty/", headers=self.headers)

    @task(1)
    def list_departments(self):
        """List departments"""
        if self.token:
            self.client.get("/api/v1/college/departments/", headers=self.headers)


class AnonymousUser(HttpUser):
    """Simulates anonymous public access."""
    wait_time = between(3, 6)
    
    @task(5)
    def health_check(self):
        """Public health endpoint"""
        self.client.get("/health")

    @task(1)
    def login_page(self):
        """Try accessing login (should redirect)"""
        self.client.get("/api/v1/auth/login")


# Print test summary when test is done
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Print summary when test stops."""
    print("\n" + "=" * 60)
    print("📊 Load Test Complete")
    print("=" * 60)
    
    stats = environment.stats
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    
    if total_requests > 0:
        error_rate = (total_failures / total_requests) * 100
        print(f"Total Requests: {total_requests}")
        print(f"Failures: {total_failures}")
        print(f"Error Rate: {error_rate:.2f}%")
        
        if error_rate < 1:
            print("✅ Error rate < 1% - PASS")
        else:
            print("❌ Error rate >= 1% - CHECK FAILURES")
        
        # Print p95 response times
        if stats.total.p95_response_time:
            print(f"p95 Response Time: {stats.total.p95_response_time}ms")
            if stats.total.p95_response_time < 500:
                print("✅ p95 < 500ms - PASS")
            else:
                print("❌ p95 >= 500ms - CHECK SLOW ENDPOINTS")
    
    print("=" * 60)
