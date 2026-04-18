import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initiliazed the database.')

@click.command('populate-db')
def populate_db_command():
    """Populate the database with some dummy entries."""
    db = get_db()

    issues = [
        ('Dog Food Taxes Raise!!!', 'Now we eat less for more :( bark bark', 0, 'Finances'),
        ('Dog Salaries Lowered', 'Now we work harder for less :( woof woof', 0, 'Finances'),
        ('Extra Daily Dog', 'Blah blah blah heres what ur money is worth to us', 1, 'Extra'),
    ]

    try:
        db.executemany(
            'INSERT INTO issue (title, body, paid, tag) VALUES (?, ?, ?, ?)',
            issues
        )
        db.commit()
        click.echo('Added three dummy issue entries.')
    except Exception as e:
        click.echo(f'An error occurred: {e}')
    

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)