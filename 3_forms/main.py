from flask import Flask
from flask import render_template, redirect
from forms import SignupForm
from flask_bootstrap import Bootstrap
from models import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "a long and safe secret key"

bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if(form.validate_on_submit()):
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        return render_template('profile.html', user=user)

    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run()