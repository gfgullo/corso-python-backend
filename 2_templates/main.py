from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route("/user/<user>")
def hello_user(user):
    user_info = ["Age=29", "Gender=male", "Height=175cm", "Weight=75kg"]
    return render_template("user.html", user=user, user_info=user_info)

if __name__ == '__main__':
    app.run()