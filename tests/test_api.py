from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def _token():
    email = 'apiuser@example.com'
    password = 'Password123'
    client.post('/register', json={'full_name': 'API User', 'email': email, 'password': password})
    r = client.post('/login', json={'email': email, 'password': password})
    return r.json()['access_token']


def test_predict_and_ats():
    token = _token()
    headers = {'Authorization': f'JWT {token}'}

    pred = client.post('/predict', json={'text': 'python fastapi sql docker machine learning'}, headers=headers)
    assert pred.status_code == 200
    assert 'category' in pred.json()

    ats = client.post('/ats-score', json={'text': 'python sql project experience education achievements certification'}, headers=headers)
    assert ats.status_code == 200
    assert 'score' in ats.json()
