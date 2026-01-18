import pytest

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    # The home page might redirect to /login or show index
    assert response.status_code == 200

def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "login" in response.text.lower()

def test_signup_page(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert "signup" in response.text.lower() or "register" in response.text.lower()
