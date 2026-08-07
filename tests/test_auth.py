from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_register_and_login():
    payload = {'full_name': 'Test User', 'email': 'test@example.com', 'password': 'Password123'}
    r = client.post('/register', json=payload)
    assert r.status_code in (200, 400)

    login = client.post('/login', json={'email': payload['email'], 'password': payload['password']})
    assert login.status_code == 200
    assert 'access_token' in login.json()
