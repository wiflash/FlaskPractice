from blueprints import db
from flask_restful import fields
from datetime import datetime


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    writer = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    deleted_status = db.Column(db.Boolean, default=False)

    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "title": fields.String,
        "isbn": fields.String,
        "writer": fields.String
    }

    def __init__(self, title, isbn, writer):
        self.title = title
        self.isbn = isbn
        self.writer = writer

    def __repr__(self):
        return "<Books %r>" % self.id