from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json


app = Flask(__name__)
api = Api(app)


@app.route("/")
def home():
    return "<h1>Challenge 1</h1>"

from blueprints.user.resources import blueprint_user
app.register_blueprint(blueprint_user, url_prefix="/user")


if __name__ == "__main__":
    app.run(debug=True)