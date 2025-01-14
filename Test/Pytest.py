import pytest
import json
from app import app, db, User, Flashcard, History

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

def test_view_history_not_authenticated(client):
    response = client.get('/view_history')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'error' in data
    assert data['error'] == 'User not authenticated'

def test_save_history_no_email(client):
    response = client.post('/save_history', json={'score_percentage': 90})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == 'Email or score_percentage missing.'
