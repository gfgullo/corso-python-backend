from .. import db
from . import auth
from flask import render_template, redirect, url_for, flash
from app.auth.forms import SignupForm, LoginForm
from app.models import User


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if(form.validate_on_submit()):
        flash("Check your inbox")
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # qui dobbiamo autenticare l'utente ...

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()

        if(user is not None and user.check_password(form.password.data)):
            # qui dobbiamo autenticare l'utente ...
            return redirect(url_for("main.index"))
        else:
            flash("Invalid email or password")

    return render_template('login.html', form=form)