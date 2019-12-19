import json, hashlib, logging
from unittest import mock
from unittest.mock import patch
from . import client, create_token, reset_db
from password_strength import PasswordPolicy

class TestWeatherGet():
    def weather_api_mock(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if len(args[0]) > 0:
            if args[0] == "https://api.weatherbit.io/v2.0/ip":
                return MockResponse(
                    {
                        "latitude": "123.456789",
                        "longitude": "-123.456789",
                        "city": "Gotham",
                        "organization": "Justice League",
                        "timezone": "Europe/Gotham",
                    },
                    200
                )
            elif args[0] == "https://api.weatherbit.io/v2.0/current":
                return MockResponse(
                    {
                        "data": [{
                            "datetime": "2020-07-22 23:23:00",
                            "temp": 23.0
                        }]
                    },
                    200
                )
        return MockResponse(None, 404)

    @mock.patch("requests.get", side_effect=weather_api_mock)
    def test_get(self, test_reqget_mock, client):
        token = create_token()
        data = {"ip": "112.215.240.165"}
        res = client.get("/weather", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200