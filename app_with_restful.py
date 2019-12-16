from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
from blueprint import *


app = Flask(__name__)
api = Api(app)


@app.route("/")
def home():
    return "<h1>Home page cuy</h1>"


class PersonResources(Resource):
    person = Person()
    def get(self):
        return self.person.__dict__, 200, {
            "Content-Type": "application/json"
        }
    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument("name", location="json", required=True)
        parser.add_argument("age", location="json", type=int, required=True)
        parser.add_argument("sex", location="json", required=True)
        args = parser.parse_args()
        self.person.name = args["name"]
        self.person.age = args["age"]
        self.person.sex = args["sex"]
        return self.person.__dict__, 200, {
            "Content-Type": "application/json"
        }
    def put(self):
        parser= reqparse.RequestParser()
        parser.add_argument("name", location="json", required=True)
        parser.add_argument("age", location="json", type=int, required=True)
        parser.add_argument("sex", location="json", required=True)
        args = parser.parse_args()
        self.person.name = args["name"]
        self.person.age = args["age"]
        self.person.sex = args["sex"]
        return self.person.__dict__, 200, {
            "Content-Type": "application/json"
        }
    def delete(self):
        self.person.reset()
        return "Deleted", 200
    def patch(self):
        return "Not yet implemented", 501


api.add_resource(PersonResources,"/name")


if __name__ == "__main__":
    app.run(debug=True)