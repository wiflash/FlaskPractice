from flask_restful import Resource, Api, reqparse
from flask import Blueprint
from datetime import datetime
from . import *


blueprint_user = Blueprint("user", __name__)
api = Api(blueprint_user)

class UserResources(Resource):
    users = Users()
    def get(self, id=None):
        if id is not None:
            result = self.users.get_by_id(id)
            if result is not None:
                return result, 200, {
                    "Content-Type": "application/json"
                }
            else:
                return {"status": "NOT_FOUND"}, 404, {
                    "Content-Type": "application/json"
                }
        else:
            return self.users.get_all(), 200, {
                "Content-Type": "application/json"
            }
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", location="json", required=True)
        parser.add_argument("age", location="json", type=int, required=True)
        parser.add_argument("sex", location="json", required=True)
        parser.add_argument("client_id", location="json", type=int, required=True)
        args = parser.parse_args()
        args["created_at"] = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        args["updated_at"] = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        if self.users.users != []: args["id"] = self.users.users[-1]["id"] + 1
        else: args["id"] = 1
        self.users.add_new(args)
        return args, 200, {
            "Content-Type": "application/json"
        }
    def put(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument("name", location="json", required=True)
        parser.add_argument("age", location="json", type=int, required=True)
        parser.add_argument("sex", location="json", required=True)
        parser.add_argument("client_id", location="json", type=int, required=True)
        args = parser.parse_args()
        if id is not None:
            result = self.users.update_by_id(args, id)
            if result is not None:
                return result, 200, {
                    "Content-Type": "application/json"
                }
        return {"status": "NOT_FOUND"}, 404, {
            "Content-Type": "application/json"
        }
    def delete(self, id=None):
        if id is not None:
            result = self.users.delete_by_id(id)
            if result is True:
                return "Deleted", 200
        return {"status": "NOT_FOUND"}, 404, {
            "Content-Type": "application/json"
        }
    def patch(self):
        return "Not yet implemented", 501

api.add_resource(UserResources, "", "/<int:id>")