import pytest
from api.index import app

VALID_TOKEN = open('tests/valid_token.txt', 'r').read()
HEADERS = {'token': VALID_TOKEN}

def test_get_material():
    with app.test_client() as client:
        response = client.post('/api/database/material', headers=HEADERS, json={
            'material_id': '6552b7cacdbae5d00cfcc7c4'
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "content" in response.json

def test_get_game():
    with app.test_client() as client:
        response = client.post('/api/database/game', headers=HEADERS, json={
            'game_id': '6552ba84a316097da00c9aa5'
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "game" in response.json
        assert "content" in response.json["game"]
        assert "type" in response.json["game"]
        assert "material_id" in response.json["game"]




if __name__ == '__main__':
    pytest.main()