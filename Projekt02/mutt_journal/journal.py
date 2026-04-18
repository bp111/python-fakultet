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
    return render_template('journal/index.html', issues=issues)