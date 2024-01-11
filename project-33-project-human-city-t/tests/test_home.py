import pytest
from api.index import app

VALID_TOKEN = open('tests/valid_token.txt', 'r').read()
HEADERS = {'token': VALID_TOKEN}

def test_home():
    with app.test_client() as client:
        response = client.get('/', headers=HEADERS)
        assert response.status_code == 200
        assert response.data == b'Hello world!'
    
def test_api_home():
    with app.test_client() as client:
        response = client.get('/api/', headers=HEADERS)
        assert response.status_code == 200
        assert "error" not in response.json
        assert "message" in response.json
        assert response.json["message"] == "Hello world!"



if __name__ == '__main__':
    pytest.main()