from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token
from blueprints.client.model import *
import hashlib

blueprint_auth = Blueprint("auth", __name__)
api = Api(blueprint_auth)

class CreateTokenResources(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("client_key", location="args", required=True)
        parser.add_argument("client_secret", location="args", required=True)
        args = parser.parse_args()
        client_secret = hashlib.md5(args["client_secret"].encode()).hexdigest()
        if args["client_key"] == "internal" and args["client_secret"] == "th1s1s1nt3n4lcl13nt":
            client_claims_data = {}
            client_claims_data["internal_status"] = True
        else:
            qry = Clients.query.filter_by(client_key=args["client_key"])
            qry = qry.filter_by(client_secret=client_secret).first()
            if qry is None:
                return {"status": "UNAUTHORIZED", "message": "invalid client_key or client_secret"}, 401
            client_claims_data = marshal(qry, Clients.jwt_claim_fields)
            client_claims_data["internal_status"] = False
        token = create_access_token(identity=args["client_key"], user_claims=client_claims_data)
        return {"token": token}, 200

api.add_resource(CreateTokenResources, "")