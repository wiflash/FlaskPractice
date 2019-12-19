import json, logging
from . import reset_db, client
from password_strength import PasswordPolicy

class TestAuthCrud():
    reset_db()
    def test_invalid_client(self, client):
        data = {"client_key": "wawawaw", "client_secret": "wawew123"}
        res = client.get("/token", query_string=data)
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 401
        assert res_json["status"] == "UNAUTHORIZED"
        assert res_json["message"] == "invalid client_key or client_secret"