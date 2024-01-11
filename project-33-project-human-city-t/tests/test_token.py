import pytest
from api.index import app
from api.database.mongo import verifyToken

VALID_TOKEN = open('tests/valid_token.txt', 'r').read()

def test_get_token_for_admin():
    with app.test_client() as client:
        response = client.post('/api/auth/gettoken', json={
            'username': 'test',
            'password': 'test'
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "token" in response.json

def test_get_token_for_user():
    with app.test_client() as client:
        response = client.post('/api/auth/gettoken', json={
            'username': 'catfish123',
            'password': 'catfish123'
        })
        assert response.status_code == 400
        assert "error" in response.json
        assert "token" not in response.json

def test_get_token_missing_credentials():
    with app.test_client() as client:
        response = client.post('/api/auth/gettoken', json={})
        assert response.status_code == 400
        assert "error" in response.json
        assert "token" not in response.json
        assert "Missing username or password" in response.json["error"]

def test_get_token_user_not_found():
    with app.test_client() as client:
        response = client.post('/api/auth/gettoken', json={
            'username': 'nonexistent_user',
            'password': 'password123'
        })
        assert response.status_code == 400
        assert "error" in response.json
        assert "token" not in response.json
        assert "Invalid username or password" in response.json["error"]

def test_get_token_incorrect_password():
    with app.test_client() as client:
        response = client.post('/api/auth/gettoken', json={
            'username': 'test',
            'password': 'wrong_password'
        })
        assert response.status_code == 400
        assert "error" in response.json
        assert "token" not in response.json
        assert "Invalid username or password" in response.json["error"]

def test_get_token_user_not_eligible():
    with app.test_client() as client:
        response = client.post('/api/auth/gettoken', json={
            'username': 'catfish123',
            'password': 'catfish123'
        })
        assert response.status_code == 400
        assert "error" in response.json
        assert "token" not in response.json
        assert "User not eligible to gain a token" in response.json["error"]

def test_verifyToken_valid():
    assert verifyToken(VALID_TOKEN) is True

def test_verifyToken_invalid():
    invalid_token = 'invalid_token'
    assert verifyToken(invalid_token) is False

if __name__ == '__main__':
    pytest.main()