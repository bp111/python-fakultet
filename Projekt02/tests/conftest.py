# tests/conftest.py
import os
import tempfile
import pytest
from werkzeug.security import generate_password_hash

from mutt_journal import create_app
from mutt_journal.db import get_db, init_db

@pytest.fixture
def app():
    # Create a temporary file to isolate the database for tests
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'UPLOAD_FOLDER': tempfile.mkdtemp(), # Mock upload folder
    })

    with app.app_context():
        init_db()
        db = get_db()
        
        # Populate with dummy data for testing
        db.execute(
            "INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?)",
            ('test_user', generate_password_hash('test'), 0)
        )
        db.execute(
            "INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?)",
            ('admin_user', generate_password_hash('admin'), 1)
        )
        db.execute(
            "INSERT INTO issue (title, summary, body, paid) VALUES (?, ?, ?, ?)",
            ('Test Issue', 'A test summary.', 'Test body.', 0)
        )
        db.execute(
            "INSERT INTO issue (title, summary, body, paid) VALUES (?, ?, ?, ?)",
            ('Paid Issue', 'A paid summary.', 'Paid body.', 1)
        )
        db.execute(
            "INSERT INTO comment (body, author_id, issue_id) VALUES (?, ?, ?)",
            ('Test comment', 1, 1)
        )
        db.commit()

    yield app

    # Clean up the temporary database after the test is done
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test_user', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)