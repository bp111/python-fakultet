import os

from flask import Flask

def create_app(test_config=None):
    # create, config app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',   # should be changed for deployment
        DATABASE=os.path.join(app.instance_path, 'mutt_journal.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)    # can eg set real secret key from that file
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)   # creates instance folder    
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    return app