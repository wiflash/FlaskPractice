from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json, logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
api = Api(app, catch_all_404s=True)


@app.route("/")
def home():
    return "<h1>Challenge 1</h1>"


from blueprints.user.resources import blueprint_user
app.register_blueprint(blueprint_user, url_prefix="/user")
 

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


if __name__ == "__main__":
    log_path = "/storage/log"
    logging.basicConfig(level=logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    log_handler = RotatingFileHandler(
        "%s/%s" %(app.root_path, log_path+"/app.log"), maxBytes=100000, backupCount=10
    )
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)
    app.run(debug=True)