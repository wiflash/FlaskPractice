from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta


class Rents(db.Model):
    __tablename__ = "rents"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    return_date = db.Column(db.DateTime, default=datetime.now()+timedelta(days=7))
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    response_fields = {
        "created_at": fields.DateTime,
        "return_date": fields.DateTime,
        "id": fields.Integer,
        "book_id": fields.Integer,
        "user_id": fields.Integer
    }

    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id

    def __repr__(self):
        return "<Rents %r>" % self.id