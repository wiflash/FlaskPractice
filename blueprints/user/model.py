from blueprints import db
from flask_restful import fields
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(), nullable=False)

    response_fields = {
        "id": fields.Integer,
        "name": fields.String,
        "age": fields.Integer,
        "sex": fields.String
    }

    def __init__(self, user_name, age, sex):
        self.name = user_name
        self.age = age
        self.sex = sex

    def __repr__(self):
        return "<Users %r>" % self.name