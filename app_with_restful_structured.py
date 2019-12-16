from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json


app = Flask(__name__)
api = Api(app)


@app.route("/")
def home():
    return "<h1>Home page cuy</h1>"

from blueprints.person.resources import blueprint_person
app.register_blueprint(blueprint_person, url_prefix="/name")


if __name__ == "__main__":
    app.run(debug=True)