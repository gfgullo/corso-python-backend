from app import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime as dt

class Permission:
    WRITE_ANSWER = 2
    WRITE_QUESTION = 4
    ADMIN = 8

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():

        roles = {
            'User' : [Permission.WRITE_ANSWER, Permission.WRITE_QUESTION],
            'Admin' : [Permission.WRITE_ANSWER, Permission.WRITE_QUESTION, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = 0
            for perm in roles[r]:
                role.permissions+=perm
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


    def has_permission(self, perm):
        return self.permissions & perm == perm


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    posts = db.relationship('Question', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    upvotes = db.relationship('Upvote', foreign_keys='Upvote.user_id', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def upvote(self, question):
        if not self.has_upvoted_question(question):
            upvote = Upvote(user_id = self.id, question_id = question.id)
            db.session.add(upvote)

    def downvote(self, question):
        if self.has_upvoted_question(question):
            Upvote.query.filter_by(user_id=self.id, question_id=question.id).delete()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.role is not None and self.role.has_permission(Permission.ADMIN)


    def has_upvoted_question(self, question):
        return Upvote.query.filter(
            Upvote.user_id == self.id,
            Upvote.question_id == question.id).count() > 0


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)
    comments = db.relationship('Comment', back_populates='question', lazy='dynamic', cascade="all, delete-orphan", foreign_keys='[Comment.question_id]')
    correct_answer_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    correct_answer = db.relationship('Comment', uselist=False,  post_update=True, foreign_keys=[correct_answer_id])
    upvotes = db.relationship('Upvote', backref='question', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship("Question", back_populates='comments', foreign_keys=[question_id])


class Upvote(db.Model):
    __tablename__ = "upvotes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
