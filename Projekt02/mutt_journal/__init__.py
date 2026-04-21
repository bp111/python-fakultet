import os

from flask import Flask, render_template

def create_app(test_config=None):
    # create, config app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',   # should be changed for deployment
        DATABASE=os.path.join(app.instance_path, 'mutt_journal.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.root_path, 'static', 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024 # so max 16MB
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)    # can eg set real secret key from that file
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)   # creates instance folder    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    from . import db
    db.init_app(app)    

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import journal
    app.register_blueprint(journal.bp)
    app.add_url_rule('/', endpoint='index')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    from flask_admin import Admin
    from .admin import SecureAdminIndexView, IssueAdminView

    admin = Admin(app, name='admin', index_view=SecureAdminIndexView())
    admin.add_view(IssueAdminView(name='Add Issue', endpoint='issue_admin'))    

    return app