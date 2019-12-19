from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask import Blueprint
from flask_jwt_extended import jwt_required
from blueprints import db, internal_required
from sqlalchemy import desc
from password_strength import PasswordPolicy
from datetime import datetime
from blueprints.client.model import *
import hashlib


blueprint_client = Blueprint("client", __name__)
api = Api(blueprint_client)

class ClientResources(Resource):
    @jwt_required
    @internal_required
    def get(self, id=None):
        if id is None:
            rows = []
            parser =reqparse.RequestParser()
            parser.add_argument("p", type=int, location="args", default=1)
            parser.add_argument("rp", type=int, location="args", default=25)
            parser.add_argument("status", location="args", type=inputs.boolean)
            args = parser.parse_args()
            offset = (args["p"] - 1)*args["rp"]
            
            qry = Clients.query.filter_by(deleted_status=False)
            if args["status"] is not None:
                qry = qry.filter_by(status=args["status"])
            qry = qry.limit(args["rp"]).offset(offset)
            for row in qry.all():
                rows.append(marshal(row, Clients.response_fields))
            return rows, 200
        else:
            qry = Clients.query.get(id)
            if qry is None or qry.deleted_status is True:
                return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}
            return marshal(qry, Clients.response_fields), 200, {"Content-Type": "application/json"}

    @jwt_required
    @internal_required
    def post(self):
        policy = PasswordPolicy.from_names(
            length=6,
            uppercase=0,
            numbers=1,
            special=0
        )
        parser = reqparse.RequestParser()
        parser.add_argument("client_key", location="json", required=True)
        parser.add_argument("client_secret", location="json", required=True)
        parser.add_argument("status", type=bool, location="json")
        args = parser.parse_args()
        validation = policy.test(args["client_secret"])
        if validation == []:
            password_digest = hashlib.md5(args["client_secret"].encode()).hexdigest()
            client = Clients(args["client_key"], password_digest, args["status"])
            if Clients.query.filter_by(client_key=args["client_key"]).all() != []:
                return {"status": "FAILED", "message": "client_key already exist"}, 400, {"Content-Type": "application/json"}
            db.session.add(client)
            db.session.commit()
            return marshal(client, Clients.response_fields), 200, {"Content-Type": "application/json"}
        return {"status": "FAILED", "message": "password is not accepted"}, 400, {"Content-Type": "application/json"}

    @jwt_required
    @internal_required
    def put(self, id=None):
        policy = PasswordPolicy.from_names(
            length=6,
            uppercase=0,
            numbers=1,
            special=0
        )
        parser = reqparse.RequestParser()
        parser.add_argument("client_key", location="json", required=True)
        parser.add_argument("client_secret", location="json", required=True)
        parser.add_argument("status", type=bool, location="json", required=True)
        args = parser.parse_args()
        if id is not None:
            qry = Clients.query.get(id)
            if qry is not None and qry.deleted_status is False:
                validation = policy.test(args["client_secret"])
                if validation == []:
                    password_digest = hashlib.md5(args["client_secret"].encode()).hexdigest()
                    if Clients.query.get(id).client_key != args["client_key"]:
                        if Clients.query.filter_by(client_key=args["client_key"]).all() != []:
                            return {"status": "FAILED", "message": "client_key already exist"}, 400, {"Content-Type": "application/json"}
                    qry.client_key = args["client_key"]
                    qry.client_secret = password_digest
                    qry.status = args["status"]
                    qry.updated_at = datetime.now()
                    db.session.commit()
                    return marshal(qry, Clients.response_fields), 200, {"Content-Type": "application/json"}
                return {"status": "FAILED", "message": "password is not accepted"}, 400, {"Content-Type": "application/json"}
        return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}

    @jwt_required
    @internal_required
    def delete(self, id=None):
        if id is not None:
            qry = Clients.query.get(id)
            if qry is not None and qry.deleted_status is False:
                qry.deleted_status = True
                db.session.commit()
                return {"message": "Deleted"}, 200, {"Content-Type": "application/json"}
        return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}


api.add_resource(ClientResources, "", "/<int:id>")