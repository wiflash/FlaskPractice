from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required
import requests


blueprint_weather = Blueprint("weather", __name__)
api = Api(blueprint_weather)


class WeatherResources(Resource):
    wio_host = "https://api.weatherbit.io/v2.0"
    wio_key = "1389da161d44471ba20afb597430e41a"

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("ip", location="args")
        args = parser.parse_args()

        requseted_data = requests.get(self.wio_host+"/ip", params={"ip":args["ip"], "key":self.wio_key})
        geo_location = requseted_data.json()
        lat = geo_location["latitude"]
        lon = geo_location["longitude"]

        requseted_data = requests.get(self.wio_host+"/current", params={"lat":lat, "lon":lon, "key":self.wio_key})
        current_weather = requseted_data.json()

        return {
            "city": geo_location["city"],
            "organization": geo_location["organization"],
            "timezone": geo_location["timezone"],
            "current_weather": {
                "date": current_weather["data"][0]["datetime"],
                "temp": current_weather["data"][0]["temp"]
            }
        }

api.add_resource(WeatherResources, "")