from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "a long and safe secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///heapoverflow_2'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(db, app)


    #@app.route('/')
    #def main():
    #    return render_template("index.html")


    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)

    return app