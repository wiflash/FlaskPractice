from blueprints import db
from flask_restful import fields
from datetime import datetime


class Clients(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(100), unique=True, nullable=False)
    client_secret = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(), default=datetime.now())
    deleted_status = db.Column(db.Boolean, default=False)

    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "client_key": fields.String,
        "client_secret": fields.String,
        "status": fields.Boolean
    }

    def __init__(self, key, secret, status):
        self.client_key = key
        self.client_secret = secret
        self.status = status

    def __repr__(self):
        return "<Clients %r>" % self.id