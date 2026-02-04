import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_and_unregister():
    activity = "Art Club"
    email = "testuser@example.com"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Check participant added
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    # Check participant removed
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]


def test_signup_duplicate():
    activity = "Math Club"
    email = "duplicate@example.com"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Duplicate signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_found():
    activity = "Math Club"
    response = client.post(f"/activities/{activity}/unregister?email=notfound@example.com")
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]
