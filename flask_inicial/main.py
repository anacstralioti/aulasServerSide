from flask import Flask, redirect, url_for

app = Flask(__name__, static_folder='public')

# criar index
@app.route("/")
def index():
    return "Index"

# rota admin
@app.route("/admin")
def admin(nome = ""):
    return "<h1>admin</h1>"

# rota do guest
@app.route("/guest/<guest>")
def guest(guest):
    aux = "<p> Hello guest {}</p>".format(guest)
    aux += "</br>"
    aux += "<p> Hello guest <b>%s</b</p>" % guest
    return aux

# url dinâmica
@app.route("/user/<name>")
def user(name):
    if name == "admin":
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('guest', guest=name))

@app.route("/google")
def google():
    return redirect("http://google.com")

if __name__ == '__main__':
    app.run(debug=True, port=3000)
