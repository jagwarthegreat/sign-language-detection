from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.utils import secure_filename

db = SQLAlchemy()

UPLOAD_FOLDER = 'website/static/uploads/documents/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docs', 'xls', 'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # NOTE: if password is present : 'mysql://user:password@host/database'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/sld'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, DocumentType, Document, AccreditationTask, AccreditationTaskDetail

    # this will create the models schema
    # create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# def create_database(app):
#     if not path.exists('website/' + "test"):
#         db.create_all(app)
#         print('Created Database!')