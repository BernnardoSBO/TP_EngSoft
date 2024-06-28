import json
import pytest

def test_register_user(test_client, init_database):
    response = test_client.post('/auth/register', json={
        "email": "newuser@example.com",
        "password": "newpassword",
        "name": "New",
        "surname": "User",
        "cpf": "987654321",
        "role": 0
    })
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert "Added User" in data["msg"]
    
def test_invalid_credentials_login_user(test_client, init_database):
    response = test_client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "wrongPassword"
    })
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert "Invalid credentials" in data["msg"]

def test_successfull_login_user(test_client, init_database):
    response = test_client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert "sucessful login" in data["msg"]
    assert "access_token" in data

    test_client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {data['access_token']}"
    
def test_get_users(test_client, init_database):
    response = test_client.get('/users/')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert "users" in data
    assert len(data["users"]) > 0

def test_get_user(test_client, init_database):
    response = test_client.get('/users/1')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert "users" in data
    assert data["users"]["email"] == "test@example.com"

