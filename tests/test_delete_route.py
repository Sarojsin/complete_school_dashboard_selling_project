
from fastapi import FastAPI
from app.web.routers.authority import router as authority_router
from starlette.testclient import TestClient

app = FastAPI()
app.include_router(authority_router)

def test_url_for():
    with TestClient(app) as client:
        # Check if the route exists
        url = app.url_path_for('authority_delete_teacher', id=2)
        print(f"Generated URL for ID 2: {url}")
        
        # Try to simulate a POST request to a non-existent teacher to see the response
        response = client.post("/authority/teachers/2/delete")
        print(f"POST /authority/teachers/2/delete response: {response.status_code}")
        print(f"Response content: {response.content}")

if __name__ == "__main__":
    test_url_for()
