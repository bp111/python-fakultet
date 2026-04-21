import datetime
import markdown
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
    
    # months that have issues published
    distinct_months_rows = db.execute(
        'SELECT DISTINCT strftime("%Y-%m", created) as ym FROM issue ORDER BY ym DESC'
    ).fetchall()    
    distinct_months = [row['ym'] for row in distinct_months_rows]
    total_pages = len(distinct_months)
    
    if total_pages == 0:
        return render_template('journal/index.html', issues=[], total_pages=0)

    # get the requested page    
    try:
        page = int(request.args.get('page', 1))
        if page < 1 or page > total_pages:
            abort(404)
    except ValueError:
        page = 1

    # year/month for current page
    current_ym = distinct_months[page - 1]
    year_str, month_str = current_ym.split('-')

    # fetch issues for current page's month
    issues = db.execute(
        'SELECT id, created, title, summary, thumbnail, paid'
        ' FROM issue'
        ' WHERE strftime("%Y", created) = ? AND strftime("%m", created) = ?'
        ' ORDER BY created DESC',
        (year_str, month_str)
    ).fetchall()

    # month navigation bar
    max_pages_to_show = 12    
    start_page = page - 6
    end_page = page + 5
    if start_page < 1:
        start_page = 1
        end_page = min(total_pages, start_page + max_pages_to_show - 1)
    if end_page > total_pages:
        end_page = total_pages
        start_page = max(1, end_page - max_pages_to_show + 1)
    
    return render_template(
        'journal/index.html', 
        issues=issues,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page
    )

@bp.route('/issue/<int:id>')
def issue_detail(id):
    db = get_db()
    issue = db.execute(
        'SELECT id, created, title, body, thumbnail, paid'
        ' FROM issue WHERE id = ?', (id,)
    ).fetchone()

    if issue is None:
        abort(404)

    if issue['paid'] and g.user is None:
        flash('Please log in to read this exclusive issue.')
        return redirect(url_for('auth.login'))

    body_html = markdown.markdown(issue['body'])

    comments = db.execute(
        'SELECT c.id, c.created, c.body, c.author_id, c.issue_id, u.username'
        ' FROM comment c JOIN user u ON c.author_id = u.id'
        ' WHERE c.issue_id = ?'
        ' ORDER BY c.created ASC',
        (id,)
    ).fetchall()

    return render_template('journal/issue.html', issue=issue, body_html=body_html, comments=comments)


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

    return redirect(url_for('journal.issue_detail', id=id))


@bp.route('/comment/<int:id>/edit', methods=('POST',))
@login_required
def edit_comment(id):
    body = request.form['body']
    db = get_db()
    comment = db.execute('SELECT * FROM comment WHERE id = ?', (id,)).fetchone()
        
    if comment is None or comment['author_id'] != g.user['id']:
        abort(403)
        
    issue_id = comment['issue_id']

    if body:
        db.execute('UPDATE comment SET body = ? WHERE id = ?', (body, id))
        db.commit()

    return redirect(url_for('journal.issue_detail', id=issue_id))


@bp.route('/comment/<int:id>/delete', methods=('POST',))
@login_required
def delete_comment(id):
    db = get_db()
    comment = db.execute('SELECT * FROM comment WHERE id = ?', (id,)).fetchone()
        
    if comment is None or comment['author_id'] != g.user['id']:
        abort(403)
    
    issue_id = comment['issue_id']

    db.execute('DELETE FROM comment WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('journal.issue_detail', id=issue_id))