# tests/test_journal.py
import pytest
from mutt_journal.db import get_db

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # Both free and paid issues should appear on the index
    assert b'Test Issue' in response.data
    assert b'Paid Issue' in response.data

def test_issue_detail_free(client):
    response = client.get('/issue/1')
    assert response.status_code == 200
    assert b'Test body.' in response.data
    assert b'Test comment' in response.data  # From our conftest fixture

def test_issue_detail_paid(client, auth):
    # Anonymous user gets redirected to login
    response = client.get('/issue/2')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']
    
    # Logged-in user can view the exclusive issue
    auth.login()
    response = client.get('/issue/2')
    assert response.status_code == 200
    assert b'Paid body.' in response.data

def test_add_comment(client, auth, app):
    auth.login()
    response = client.post('/1/comment', data={'body': 'New bark!'})
    assert response.headers['Location'] == '/issue/1'
    
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM comment').fetchone()[0]
        assert count == 2

def test_edit_comment(client, auth, app):
    auth.login()
    response = client.post('/comment/1/edit', data={'body': 'Edited bark!'})
    assert response.headers['Location'] == '/issue/1'
    
    with app.app_context():
        db = get_db()
        comment = db.execute('SELECT body FROM comment WHERE id = 1').fetchone()
        assert comment['body'] == 'Edited bark!'

def test_delete_comment(client, auth, app):
    auth.login()
    response = client.post('/comment/1/delete')
    assert response.headers['Location'] == '/issue/1'
    
    with app.app_context():
        db = get_db()
        comment = db.execute('SELECT * FROM comment WHERE id = 1').fetchone()
        assert comment is None