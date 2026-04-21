# tests/test_auth.py
import pytest
from flask import g, session
from mutt_journal.db import get_db

def test_register(client, app):
    # Test that the register page loads
    assert client.get('/auth/register').status_code == 200
    
    # Test valid registration redirects to login
    response = client.post(
        '/auth/register', data={'username': 'new_dog', 'password': 'password123'}
    )
    assert response.headers['Location'] == '/auth/login'

    # Verify the user was actually inserted into the database
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'new_dog'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username required'),
    ('a', '', b'Password required'),
    ('test_user', 'test', b'is already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    # Test that the login page loads
    assert client.get('/auth/login').status_code == 200
    
    # Test valid login redirects to index
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Verify that the session contains the user_id after login
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test_user'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('unknown_dog', 'test', b'Incorrect username.'),
    ('test_user', 'wrong_password', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()
    
    with client:
        auth.logout()
        assert 'user_id' not in session