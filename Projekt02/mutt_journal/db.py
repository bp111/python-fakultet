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

    issues = []
    
    # one chosen month has to have 10+ entries, checking how list behaves vertically
    for i in range(1, 11):
        created = datetime(2024, 5, i, 10, 0)
        issues.append((
            f'Dog special #{i}', 
            f'Summary for special {i}.', 
            '**Ababababa dog food** Testing *markdown* here. Love doggy foood am i right', 
            None, 
            i % 2 == 0,
            created
        ))

    # 20 more entries, 20 different months
    month_offset = 0
    for i in range(1, 21):        
        y = 2023 + (month_offset // 12)
        m = (month_offset % 12) + 1

        # may skipped        
        if y == 2024 and m == 5:
            month_offset += 1
            y = 2023 + (month_offset // 12)
            m = (month_offset % 12) + 1
            
        created = datetime(y, m, 15, 12, 0)
        issues.append((
            f'Regular dog {y}-{m:02d}', 
            f'Just a regular dog for {y}-{m:02d}.', 
            'Havent got any fun news today sorry :(', 
            None, 
            0,
            created
        ))
        month_offset += 1

    try:        
        db.executemany(
            'INSERT INTO issue (title, summary, body, thumbnail, paid, created) VALUES (?, ?, ?, ?, ?, ?)',
            issues
        )
        db.commit()
        click.echo(f'Added {len(issues)} dummy issue entries.')
    except Exception as e:
        click.echo(f'An error occurred: {e}')
    

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

# for sqlite: how to handle datetime objects when inserting into db
sqlite3.register_adapter(datetime, lambda v: v.isoformat()) 


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)