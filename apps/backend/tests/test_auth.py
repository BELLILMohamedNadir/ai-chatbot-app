import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def test_user():
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }


def test_register_user(test_user):
    """Test user registration with valid data"""
    response = client.post("/api/v1/auth/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]
    assert "id" in data


def test_register_duplicate_email(test_user):
    """Test registration fails with duplicate email"""
    client.post("/api/v1/auth/register", json=test_user)
    response = client.post("/api/v1/auth/register", json=test_user)
    assert response.status_code == 400


def test_login_user(test_user):
    """Test user login with valid credentials"""
    client.post("/api/v1/auth/register", json=test_user)
    response = client.post("/api/v1/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"


def test_login_invalid_password(test_user):
    """Test login fails with wrong password"""
    client.post("/api/v1/auth/register", json=test_user)
    response = client.post("/api/v1/auth/login", json={
        "email": test_user["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_nonexistent_user():
    """Test login fails for non-existent user"""
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "anypassword"
    })
    assert response.status_code == 401
