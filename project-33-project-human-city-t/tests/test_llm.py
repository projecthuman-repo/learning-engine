import pytest
from api.index import app

VALID_TOKEN = open('tests/valid_token.txt', 'r').read()
HEADERS = {'token': VALID_TOKEN}

def test_llm_word_definition_pairs():
    with app.test_client() as client:
        response = client.post('/api/llm/generate-word-definition-pairs', headers=HEADERS, json={
            'material_id': '6552b7cacdbae5d00cfcc7c4'
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "word_definitions" in response.json
        assert "game_id" in response.json

def test_mcqs_llm():
    with app.test_client() as client:
        response = client.post('/api/llm/generate-mcqs', headers=HEADERS, json={
            'material_id': '6552b7cacdbae5d00cfcc7c4'
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "mcqs" in response.json
        assert "game_id" in response.json

def test_short_answer_llm():
    with app.test_client() as client:
        response = client.post('/api/llm/generate-short-answers', headers=HEADERS, json={
            'material_id': '6552b7cacdbae5d00cfcc7c4'
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "short_answers" in response.json
        assert "game_id" in response.json

def test_fill_in_the_blanks_llm():
    with app.test_client() as client:
        response = client.post('/api/llm/generate-fill-in-the-blanks', headers=HEADERS, json={
            'material_id': '6552b7cacdbae5d00cfcc7c4'
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "fill_in_the_blanks" in response.json
        assert "game_id" in response.json

if __name__ == '__main__':
    pytest.main()