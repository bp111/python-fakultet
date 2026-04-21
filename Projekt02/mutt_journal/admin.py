import os
import datetime
from flask import g, redirect, url_for, request, flash, current_app
from flask_admin import AdminIndexView, BaseView, expose 
from wtforms import Form, StringField, TextAreaField, BooleanField, FileField, DateField, validators 
from werkzeug.utils import secure_filename
from mutt_journal.db import get_db

class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):        
        return g.user is not None and g.user['is_admin'] == 1

    def inaccessible_callback(self, name, **kwargs):
        flash('Insufficient permissions to access the admin panel!')
        return redirect(url_for('auth.login', next=request.url)) 

class IssueForm(Form):
    title = StringField('Title', [validators.DataRequired()])
    created = DateField('Issue Date', format='%Y-%m-%d', default=datetime.date.today, validators=[validators.DataRequired()])
    summary = TextAreaField('Summary', [validators.DataRequired()])
    body = TextAreaField('Body (Markdown)', [validators.DataRequired()])
    thumbnail = FileField('Thumbnail Image') 
    paid = BooleanField('Paid Issue?')    

class IssueAdminView(BaseView):
    def is_accessible(self):
        return g.user is not None and g.user['is_admin'] == 1
        
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = IssueForm(request.form)
        if request.method == 'POST' and form.validate():
            db = get_db()
                        
            thumbnail_filename = None
            file = request.files.get('thumbnail')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                thumbnail_filename = filename

            current_time = datetime.datetime.now().time()
            created_timestamp = datetime.datetime.combine(form.created.data, current_time)

            db.execute(
                'INSERT INTO issue (title, summary, body, thumbnail, paid, created) VALUES (?, ?, ?, ?, ?, ?)',
                (form.title.data, form.summary.data, form.body.data, thumbnail_filename, bool(form.paid.data), created_timestamp)
            )
            db.commit()
            flash('New issue added.', 'success')
            return redirect(url_for('issue_admin.index'))
                
        return self.render('admin/issue_create.html', form=form)