from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_moment import Moment
from flask import render_template

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
mail = Mail()
migrate = Migrate()
moment = Moment()

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'A very complex and long secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///heapoverflow'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'brizzimarco95@gmail.com'
    app.config['MAIL_PASSWORD'] = 'DLbSxHNaPzhs96Wq'

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)

    from app.models import User, AnonymousUser
    login_manager.anonymous_user = AnonymousUser

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender="HeapOverflow", recipients=[to])
    msg.body = render_template(template+".txt", **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)