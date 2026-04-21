# tests/test_db.py
import sqlite3
import pytest
from mutt_journal.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('mutt_journal.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    
    assert 'Initiliazed' in result.output
    assert Recorder.called

def test_populate_db_command(runner, app):
    with app.app_context():
        result = runner.invoke(args=['populate-db'])
        assert 'Added 30 dummy issue entries.' in result.output
        
        db = get_db()
        # Conftest added 2 issues, populate-db adds 30 more, so there should be 32 total
        count = db.execute('SELECT COUNT(*) FROM issue').fetchone()[0]
        assert count == 32