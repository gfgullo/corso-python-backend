from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail, Message


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
mail = Mail()


def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "a long and safe secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///heapoverflow_2'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'brizzimarco95@gmail.com'
    app.config['MAIL_PASSWORD'] = 'DLbSxHNaPzhs96Wq'

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(db, app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)

    return app


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender="HeapOverflow", recipients=[to])
    msg.body = render_template(template+".txt", **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)