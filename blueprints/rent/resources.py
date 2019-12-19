from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from blueprints import db, internal_required, noninternal_required
from sqlalchemy import desc
from datetime import datetime
from blueprints.rent.model import *
from blueprints.book.model import *
from blueprints.user.model import *


blueprint_rent = Blueprint("rent", __name__)
api = Api(blueprint_rent)

class RentResources(Resource):
    @jwt_required
    @noninternal_required
    def get(self, id=None):
        client_claims_data = get_jwt_claims()
        if id is None:
            rows = []
            parser =reqparse.RequestParser()
            parser.add_argument("p", type=int, location="args", default=1)
            parser.add_argument("rp", type=int, location="args", default=25)
            parser.add_argument("book_id", type=int, location="args")
            parser.add_argument("user_id", type=int, location="args")
            args = parser.parse_args()
            offset = (args["p"] - 1)*args["rp"]
            
            qry = Rents.query
            if args["book_id"] is not None:
                qry = qry.filter_by(book_id=args["book_id"])
            if args["user_id"] is not None:
                qry = qry.filter_by(user_id=args["user_id"])
            users_with_selected_client = Users.query.filter_by(client_id=client_claims_data["id"])
            qry = qry.filter(Rents.user_id.in_([entry.id for entry in users_with_selected_client.all()]))
            qry = qry.limit(args["rp"]).offset(offset)
            for row in qry.all():
                marshal_rent = marshal(row, Rents.response_fields)
                book_with_id = Books.query.get(marshal_rent["book_id"])
                user_with_id = Users.query.get(marshal_rent["user_id"])
                if book_with_id.deleted_status is False and user_with_id.deleted_status is False:
                    marshal_book = marshal(book_with_id, Books.response_fields)
                    marshal_user = marshal(user_with_id, Users.response_fields)
                    marshal_rent["user"] = marshal_user
                    marshal_rent["book"] = marshal_book
                    rows.append(marshal_rent)
            return rows, 200
        else:
            qry = Rents.query.get(id)
            if qry is not None:
                marshal_rent = marshal(qry, Rents.response_fields)
                book_with_id = Books.query.get(marshal_rent["book_id"])
                user_with_id = Users.query.get(marshal_rent["user_id"])
                if book_with_id is None or book_with_id.deleted_status is True:
                    return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}
                if user_with_id is None or user_with_id.deleted_status is True:
                    return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}
                if user_with_id.client_id == client_claims_data["id"]:
                    marshal_book = marshal(book_with_id, Books.response_fields)
                    marshal_user = marshal(user_with_id, Users.response_fields)
                    marshal_rent["user"] = marshal_user
                    marshal_rent["book"] = marshal_book
                    return marshal_rent, 200, {"Content-Type": "application/json"}
            return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}


    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("book_id", location="json", type=int, required=True)
        parser.add_argument("user_id", location="json", type=int, required=True)
        args = parser.parse_args()
        book_with_id = Books.query.get(args["book_id"])
        user_with_id = Users.query.get(args["user_id"])
        if book_with_id is None or book_with_id.deleted_status is True:
            return {"message": "book_id not found"}, 404, {"Content-Type": "application/json"}
        if user_with_id is None or user_with_id.deleted_status is True:
            return {"message": "user_id not found"}, 404, {"Content-Type": "application/json"}
        Rent = Rents(args["book_id"], args["user_id"])
        db.session.add(Rent)
        db.session.commit()
        marshal_rent = marshal(Rent, Rents.response_fields)
        marshal_book = marshal(book_with_id, Books.response_fields)
        marshal_user = marshal(user_with_id, Users.response_fields)
        marshal_rent["user"] = marshal_user
        marshal_rent["book"] = marshal_book
        return marshal_rent, 200, {"Content-Type": "application/json"}


api.add_resource(RentResources, "", "/<int:id>")