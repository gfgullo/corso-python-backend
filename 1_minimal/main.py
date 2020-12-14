from flask import Flask
from flask import request
from flask import make_response
from flask import abort, redirect

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello Flask!"


@app.route('/bye')
def bye():
    return "<h1>Bye Flask!</h1>"\


@app.route('/user/<user>')
def hello_user(user):
    if (user != "giuseppe"):
        abort(403)
        # return "<h1>Forbidden</h1>",403
    # return "Hello "+user+"!",200
    return redirect("https://giuseppegullo.com")


@app.route('/info')
def info():

    info_list = "<ul>"
    info_list += "<li>User-Agent="+request.headers.get('User-Agent')+"</li>"
    info_list += "<li>Server IP="+request.remote_addr+"</li>"

    for env_info in request.environ:
        info_list += "<li>"+env_info+"="+str(request.environ[env_info])+"</li>"

    info_list += "</ul>"
    return info_list



# app.add_url_rule("/", "hello", hello)

if __name__ == '__main__':
    print(app.url_map)
    app.run()
