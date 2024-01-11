import pytest
from api.index import app

def test_404():
    with app.test_client() as client:
        response = client.get('/not_found')
        assert response.status_code == 404
        assert "error" in response.json


if __name__ == '__main__':
    pytest.main()