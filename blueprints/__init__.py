from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps
import json, random, string


app = Flask(__name__) # membuat semua blueprint
app.config["APP_DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/latihan_flask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "".join(random.choice(string.ascii_letters) for i in range(32))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
jwt = JWTManager(app)


def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims["internal_status"]:
            return {"status": "FORBIDDEN", "message": "internal only!"}, 403
        return fn(*args, **kwargs)
    return wrapper

def noninternal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims["internal_status"]:
            return {"status": "FORBIDDEN", "message": "non-internal only!"}, 403
        return fn(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    return "<h1>Challenge 1</h1>"

@app.after_request
def after_request(response):
    try:
        request_data = request.get_json()
    except:
        request_data = request.args.to_dict()
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps({
            "method": request.method,
            "code": response.status,
            "request": request_data,
            "response": json.loads(response.data.decode("utf-8"))
        }))
    else:
        app.logger.error("REQUEST_LOG\t%s", json.dumps({
            "method": request.method,
            "code": response.status,
            "request": request_data,
            "response": json.loads(response.data.decode("utf-8"))
        }))
    return response


from blueprints.auth import blueprint_auth
from blueprints.client.resources import blueprint_client
from blueprints.user.resources import blueprint_user
from blueprints.book.resources import blueprint_book
from blueprints.rent.resources import blueprint_rent
from blueprints.weather import blueprint_weather

app.register_blueprint(blueprint_auth, url_prefix="/token")
app.register_blueprint(blueprint_client, url_prefix="/client")
app.register_blueprint(blueprint_user, url_prefix="/user")
app.register_blueprint(blueprint_book, url_prefix="/book")
app.register_blueprint(blueprint_rent, url_prefix="/rent")
app.register_blueprint(blueprint_weather, url_prefix="/weather")

db.create_all()