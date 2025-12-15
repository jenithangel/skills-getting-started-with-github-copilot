import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for test
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    # Unregister
    response = client.post(f"/api/activities/{activity}/unregister", json={"email": test_email})
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_signup_duplicate():
    test_email = "pytestdupe@mergington.edu"
    activity = "Programming Class"
    # Signup first time
    client.post(f"/activities/{activity}/signup?email={test_email}")
    # Signup again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_nonexistent():
    activity = "Chess Club"
    response = client.post(f"/api/activities/{activity}/unregister", json={"email": "notfound@mergington.edu"})
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]
