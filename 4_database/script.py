from app import db
from models import User

db.create_all()
user = User(username="Giuseppe", email="giuseppe@mail.com", password="qwerty")
db.session.add(user)
db.session.commit()

db.session.add(User(username="Francesco", email="francesco@mail.com", password="qwerty"))
db.session.add(User(username="Giovanni", email="giovanni@mail.com", password="qwerty"))
db.session.commit()

db.session.add_all([User(username="Guglielmo", email="guglielmo@mail.com", password="qwerty"),
                    User(username="Antonio", email="antonio@mail.com", password="qwerty"),
                    User(username="Ferdinando", email="ferdinando@mail.com", password="qwerty")])
db.session.commit()

user.username = "gfgullo"
db.session.add(user)
db.session.commit()

User.query.all()
User.query.filter_by(email="antonio@mail.com").all()
User.query.filter_by(email="antonio@mail.com").first()

db.drop_all()