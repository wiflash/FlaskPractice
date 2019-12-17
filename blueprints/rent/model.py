from blueprints import db
from flask_restful import fields
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(), default=datetime.now())
    deleted_status = db.Column(db.Boolean, default=False)

    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "name": fields.String,
        "age": fields.Integer,
        "sex": fields.String,
        "client_id": fields.Integer
    }

    def __init__(self, user_name, age, sex, client_id):
        self.name = user_name
        self.age = age
        self.sex = sex
        self.client_id = client_id

    def __repr__(self):
        return "<Users %r>" % self.id