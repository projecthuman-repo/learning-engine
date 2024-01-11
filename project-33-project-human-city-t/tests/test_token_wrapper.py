import pytest
from api.index import app

VALID_TOKEN = open('tests/valid_token.txt', 'r').read()
INVALID_TOKEN = "invalid_token"

def test_require_token_valid():
    with app.test_client() as client:
        headers = {'token': VALID_TOKEN}
        response = client.get('/api/', headers=headers)
        assert response.status_code == 200
        assert "error" not in response.json

def test_require_token_missing_token():
    with app.test_client() as client:
        response = client.get('/api/', headers={})
        assert response.status_code == 401
        assert "error" in response.json
        assert "Token is missing" in response.json["error"]

def test_require_token_invalid_token():
    with app.test_client() as client:
        headers = {'token': INVALID_TOKEN}
        response = client.get('/api/', headers=headers)
        assert response.status_code == 403
        assert "error" in response.json
        assert "Invalid Token" in response.json["error"]

if __name__ == '__main__':
    pytest.main()
