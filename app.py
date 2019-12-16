from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
from blueprint import *


app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Home page cuy</h1>"


orang = Person()
@app.route("/name", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def name_controller():
    if request.method == "GET":
        return json.dumps(orang.__dict__), 200, {
            "Content-Type": "application/json"
        }
    elif request.method == "POST":
        data = request.get_json()
        orang.name = data["name"]
        orang.age = data["age"]
        orang.sex = data["sex"]
        return json.dumps(orang.__dict__), 200, {
            "Content-Type": "application/json"
        }
    elif request.method == "PUT":
        data = request.get_json()
        orang.name = data["name"]
        orang.age = data["age"]
        orang.sex = data["sex"]
        return json.dumps(orang.__dict__), 200, {
            "Content-Type": "application/json"
        }
    elif request.method == "DELETE":
        return "Deleted", 200
    else:
        return "Not yet to be implemented", 501


if __name__ == "__main__":
    app.run(debug=True)