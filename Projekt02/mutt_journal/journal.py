from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from mutt_journal.auth import login_required
from mutt_journal.db import get_db

bp = Blueprint('journal', __name__)

@bp.route('/')
def index():
    db = get_db()
    issues = db.execute(
        'SELECT id, created, title, body, paid, tag'
        ' FROM issue'
        ' ORDER BY created DESC'
    ).fetchall()

    comments_data = db.execute(
        'SELECT c.id, c.created, c.body, c.author_id, c.issue_id, u.username'
        ' FROM comment c JOIN user u ON c.author_id = u.id'
        ' ORDER BY c.created ASC'
    ).fetchall()

    comments = {}
    for c in comments_data:
        if c['issue_id'] not in comments:
            comments[c['issue_id']] = []
        comments[c['issue_id']].append(c)

    return render_template('journal/index.html', issues=issues, comments=comments)


@bp.route('/<int:id>/comment', methods=('POST',))
@login_required
def add_comment(id):
    body = request.form['body']
    if not body:
        flash('Please sumbit a non-empty comment.')
    else:
        db = get_db()
        db.execute(
            'INSERT INTO comment (body, author_id, issue_id) VALUES (?, ?, ?)',
            (body, g.user['id'], id)    
        )
        db.commit()

    return redirect(url_for('journal.index'))


@bp.route('/comment/<int:id>/edit', methods=('POST',))
@login_required
def edit_comment(id):
    body = request.form['body']
    db = get_db()
    comment = db.execute('SELECT * FROM comment WHERE id = ?', (id,)).fetchone()
        
    if comment is None or comment['author_id'] != g.user['id']:
        abort(403)
        
    if body:
        db.execute('UPDATE comment SET body = ? WHERE id = ?', (body, id))
        db.commit()

    return redirect(url_for('journal.index'))


@bp.route('/comment/<int:id>/delete', methods=('POST',))
@login_required
def delete_comment(id):
    db = get_db()
    comment = db.execute('SELECT * FROM comment WHERE id = ?', (id,)).fetchone()
        
    if comment is None or comment['author_id'] != g.user['id']:
        abort(403)
    
    db.execute('DELETE FROM comment WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('journal.index'))