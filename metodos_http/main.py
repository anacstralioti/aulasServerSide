# imports
from flask import Flask, request
from json import dumps

# instância do site em flask
app = Flask(__name__, static_folder='public')

@app.route("/add", methods=["GET", "POST"])
def add():
    if (request.method == "POST"):
        js = dumps(request.form)
        return js
    else:
        return ("Ok GET")

# main function
if __name__ == '__main__':
    app.run(debug=True, port=3000)