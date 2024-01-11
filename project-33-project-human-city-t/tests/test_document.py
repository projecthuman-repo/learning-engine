import pytest
from api.index import app

VALID_TOKEN = open('tests/valid_token.txt', 'r').read()
HEADERS = {'token': VALID_TOKEN}

def test_document_word():
    with app.test_client() as client:
        response = client.post('/api/document/extract-text', headers=HEADERS, data={
            'document': open(r'tests/documents/hello world.docx', 'rb')
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "text" in response.json
        assert "material_id" in response.json
        assert response.json["text"].strip() == "Hello World!"

def test_document_pdf():
    with app.test_client() as client:
        response = client.post('/api/document/extract-text', headers=HEADERS, data={
            'document': open(r'tests/documents/hello world.pdf', 'rb')
        })
        assert response.status_code == 200
        assert "error" not in response.json
        assert "text" in response.json
        assert "material_id" in response.json
        assert response.json["text"].strip() == "Hello World!"



if __name__ == '__main__':
    pytest.main()