# tests/test_admin.py
import pytest
from mutt_journal.db import get_db

def test_admin_access_anonymous(client):
    response = client.get('/admin/')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']

def test_admin_access_regular_user(client, auth):
    auth.login(username='test_user', password='test') # Standard user from fixture
    response = client.get('/admin/')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']

def test_admin_access_admin_user(client, auth):
    auth.login(username='admin_user', password='admin') # Admin user from fixture
    response = client.get('/admin/')
    assert response.status_code == 200

def test_admin_create_issue(client, auth, app):
    auth.login(username='admin_user', password='admin')
    
    # Post data to the flask-admin BaseView we set up
    response = client.post('/admin/issue_admin/', data={
        'title': 'Admin Dog',
        'created': '2024-05-15',
        'summary': 'Admin summary',
        'body': 'Admin body content',
        # Omitting thumbnail file to test basic text insertion
    })
    
    assert response.status_code == 302 # Redirects back to index on success
    
    with app.app_context():
        db = get_db()
        issue = db.execute("SELECT * FROM issue WHERE title = 'Admin Dog'").fetchone()
        assert issue is not None
        assert issue['summary'] == 'Admin summary'
        assert issue['paid'] == 0 # Should default to false since we didn't pass the checkbox