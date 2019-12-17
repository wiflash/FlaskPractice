from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db
from sqlalchemy import desc
from datetime import datetime
from blueprints.user.model import *
from blueprints.client.model import *


blueprint_user = Blueprint("user", __name__)
api = Api(blueprint_user)

class UserResources(Resource):
    def get(self, id=None):
        if id is None:
            rows = []
            parser =reqparse.RequestParser()
            parser.add_argument("p", type=int, location="args", default=1)
            parser.add_argument("rp", type=int, location="args", default=25)
            # parser.add_argument("orderby", location="args", help="invalid order-by value", choices=("id", "sex"))
            # parser.add_argument("sort", location="args", help="invalid sort value", choices=("desc","asc"))
            args = parser.parse_args()
            offset = (args["p"] - 1)*args["rp"]
            
            qry = Users.query.filter_by(deleted_status=False)
            # if args["orderby"] == "id":
            #     if args["sort"] == "desc":
            #         qry = qry.order_by(desc(Users.id))
            #     else: qry = qry.order_by(Users.id)
            # else:
            #     if args["sort"] == "desc":
            #         qry = qry.order_by(desc(Users.sex))
            #     else: qry = qry.order_by(Users.sex)
            qry = qry.limit(args["rp"]).offset(offset)
            for row in qry.all():
                client_with_id = Clients.query.get(marshal(row, Users.response_fields)["client_id"])
                if client_with_id.deleted_status is False:
                    rows.append(marshal(row, Users.response_fields))
            return rows, 200
        else:
            qry = Users.query.get(id)
            client_with_id = Clients.query.get(qry.client_id)
            if qry.deleted_status is True or qry is None or client_with_id.deleted_status is True:
                return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}
            return marshal(qry, Users.response_fields), 200, {"Content-Type": "application/json"}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", location="json", required=True)
        parser.add_argument("age", location="json", type=int, required=True)
        parser.add_argument("sex", location="json", required=True)
        parser.add_argument("client_id", location="json", type=int, required=True)
        args = parser.parse_args()
        client_with_id = Clients.query.get(args["client_id"])
        if client_with_id is None or client_with_id.deleted_status is True:
            return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}
        user = Users(args["name"], args["age"], args["sex"], args["client_id"])
        db.session.add(user)
        db.session.commit()
        return marshal(user, Users.response_fields), 200, {"Content-Type": "application/json"}

    def put(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument("name", location="json", required=True)
        parser.add_argument("age", location="json", type=int, required=True)
        parser.add_argument("sex", location="json", required=True)
        parser.add_argument("client_id", location="json", type=int, required=True)
        args = parser.parse_args()
        if id is not None:
            qry = Users.query.get(id)
            if qry.deleted_status is False and qry is not None:
                qry.name = args["name"]
                qry.age = args["age"]
                qry.sex = args["sex"]
                qry.client_id = args["client_id"]
                db.session.commit()
                return marshal(qry, Users.response_fields), 200, {"Content-Type": "application/json"}
        return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}

    def delete(self, id=None):
        if id is not None:
            qry = Users.query.get(id)
            if qry.deleted_status is False and qry is not None:
                qry.deleted_status = True
                db.session.commit()
                return {"message": "Deleted"}, 200, {"Content-Type": "application/json"}
        return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}
#     def patch(self):
#         return {"message": "Not yet implemented"}, 501, {
#             "Content-Type": "application/json"
#         }

api.add_resource(UserResources, "", "/<int:id>")