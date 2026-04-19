from flask import g, redirect, url_for, request, flash
from flask_admin import AdminIndexView, BaseView, expose 
from wtforms import Form, StringField, TextAreaField, BooleanField, validators 
from mutt_journal.db import get_db

class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):        
        return g.user is not None and g.user['is_admin'] == 1

    def inaccessible_callback(self, name, **kwargs):
        flash('Insufficient permissions to access the admin panel!')
        return redirect(url_for('auth.login', next=request.url)) 

class IssueForm(Form):
    title = StringField('Title', [validators.DataRequired()])
    body = TextAreaField('Body', [validators.DataRequired()])
    paid = BooleanField('Paid Issue?')
    tag = StringField('Tag') 

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
            db.execute(
                'INSERT INTO issue (title, body, paid, tag) VALUES (?, ?, ?, ?)',
                (form.title.data, form.body.data, bool(form.paid.data), form.tag.data)
            )
            db.commit()
            flash('New issue added.', 'success')
            return redirect(url_for('issue_admin.index'))
                
        return self.render('admin/issue_create.html', form=form)