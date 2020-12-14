from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "a long and safe secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///heapoverflow_2'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User

if __name__ == '__main__':
    app.run()


# flask db init
# flask db migrate -m "initial migration"
# flask db upgrade
