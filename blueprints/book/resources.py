from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db
from sqlalchemy import desc
from datetime import datetime
from blueprints.book.model import *


blueprint_book = Blueprint("book", __name__)
api = Api(blueprint_book)

class BookResources(Resource):
    def get(self, id=None):
        if id is None:
            rows = []
            parser =reqparse.RequestParser()
            parser.add_argument("p", type=int, location="args", default=1)
            parser.add_argument("rp", type=int, location="args", default=25)
            parser.add_argument("title", location="args")
            parser.add_argument("isbn", location="args")
            args = parser.parse_args()
            offset = (args["p"] - 1)*args["rp"]
            
            qry = Books.query.filter_by(deleted_status=False)
            if args["title"] is not None:
                qry = qry.filter(Books.title.like("%"+args["title"]+"%"))
            if args["isbn"] is not None:
                qry = qry.filter_by(isbn=args["isbn"])
            qry = qry.limit(args["rp"]).offset(offset)
            for row in qry.all():
                rows.append(marshal(row, Books.response_fields))
            return rows, 200
        else:
            qry = Books.query.get(id)
            if qry.deleted_status is True or qry is None:
                return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}
            return marshal(qry, Books.response_fields), 200, {"Content-Type": "application/json"}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", location="json", required=True)
        parser.add_argument("isbn", location="json", required=True)
        parser.add_argument("writer", location="json", required=True)
        args = parser.parse_args()
        book = Books(args["title"], args["isbn"], args["writer"])
        db.session.add(book)
        db.session.commit()
        return marshal(book, Books.response_fields), 200, {"Content-Type": "application/json"}

    def put(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument("title", location="json", required=True)
        parser.add_argument("isbn", location="json", required=True)
        parser.add_argument("writer", type=bool, location="json", required=True)
        args = parser.parse_args()
        if id is not None:
            qry = Books.query.get(id)
            if qry.deleted_status is False and qry is not None:
                qry.title = args["title"]
                qry.isbn = args["isbn"]
                qry.writer = args["writer"]
                db.session.commit()
                return marshal(qry, Books.response_fields), 200, {"Content-Type": "application/json"}
        return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}

    def delete(self, id=None):
        if id is not None:
            qry = Books.query.get(id)
            if qry.deleted_status is False and qry is not None:
                qry.deleted_status = True
                db.session.commit()
                return {"message": "Deleted"}, 200, {"Content-Type": "application/json"}
        return {"message": "NOT_FOUND"}, 404, {"Content-Type": "application/json"}
#     def patch(self):
#         return {"message": "Not yet implemented"}, 501, {
#             "Content-Type": "application/json"
#         }

api.add_resource(BookResources, "", "/<int:id>")