import pytest
from api.index import app

VALID_TOKEN = open('tests/valid_token.txt', 'r').read()
HEADERS = {'token': VALID_TOKEN}

def test_crossword():
    with app.test_client() as client:
        response = client.post('/api/game/crossword', headers=HEADERS, json={
            'game_id': '6552ba84a316097da00c9aa5',
            'grid_size': 10
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "crossword" in response.json
        assert "hints" in response.json["crossword"]
        assert "grid" in response.json["crossword"]
        assert len(response.json["crossword"]["grid"]) == 10
        assert "game_id" in response.json

def test_wordsearch():
    with app.test_client() as client:
        response = client.post('/api/game/wordsearch', headers=HEADERS, json={
            'game_id': '6552ba84a316097da00c9aa5',
            'grid_size': 10
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "wordsearch" in response.json
        assert "grid" in response.json["wordsearch"]
        assert "hints" in response.json["wordsearch"]
        assert len(response.json["wordsearch"]["grid"]) == 10
        assert "game_id" in response.json




if __name__ == '__main__':
    pytest.main()