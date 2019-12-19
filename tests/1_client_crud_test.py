import json, hashlib, logging
from . import client, create_token, reset_db
from password_strength import PasswordPolicy

class TestClientCrud():
    id_client = 0
    reset_db()
    # POST METHOD
    def test_internal_client_post(self, client):
        token = create_token()
        data = {"client_key": "wawew2", "client_secret": "wawew123", "status": True}
        res = client.post("/client", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["id"] > 0
        assert res_json["client_key"] == data["client_key"]
        assert res_json["client_secret"] == hashlib.md5(data["client_secret"].encode()).hexdigest()
        self.id_client = res_json["id"]
    def test_internal_client_post_invalid_key_double(self, client):
        token = create_token()
        data = {"client_key": "wawew2", "client_secret": "wawew123", "status": True}
        res = client.post("/client", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "client_key already exist"
    def test_internal_client_post_invalid_pwd(self, client):
        token = create_token()
        data = {"client_key": "wawew3", "client_secret": "waw", "status": True}
        res = client.post("/client", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "password is not accepted"
    
    # DELETE METHOD
    def test_internal_client_delete_id(self, client):
        token = create_token()
        res = client.delete("/client/2", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["message"] == "Deleted"
    def test_internal_client_delete_id_but_already_deleted(self, client):
        token = create_token()
        res = client.delete("/client/2", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    def test_internal_client_delete_id_not_found(self, client):
        token = create_token()
        res = client.delete("/client/100", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    
    # PUT METHOD
    def test_internal_client_put_id(self, client):
        token = create_token()
        data = {"client_key": "wawew3", "client_secret": "wawew123", "status": True}
        res = client.post("/client", json=data, headers={"Authorization": "Bearer "+token})
        data = {"client_key": "wawew3", "client_secret": "wawew1234", "status": True}
        res = client.put("/client/3", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["id"] > 0
        assert res_json["client_key"] == data["client_key"]
        assert res_json["client_secret"] == hashlib.md5(data["client_secret"].encode()).hexdigest()
        self.id_client = res_json["id"]
    def test_internal_client_put_but_deleted_id(self, client):
        token = create_token()
        data = {"client_key": "wawew4", "client_secret": "wawew123", "status": True}
        res = client.put("/client/2", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    def test_internal_client_put_id_not_found(self, client):
        token = create_token()
        data = {"client_key": "wawew1000new", "client_secret": "wawew123", "status": True}
        res = client.put("/client/1000", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    def test_internal_client_put_invalid_key(self, client):
        token = create_token()
        data = {"client_key": "wawew1", "client_secret": "wawew123", "status": True}
        res = client.put("/client/3", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["message"] == "client_key already exist"
        assert res_json["status"] == "FAILED"
    def test_internal_client_put_invalid_pwd(self, client):
        token = create_token()
        data = {"client_key": "wawew3", "client_secret": "wawewawawa", "status": True}
        res = client.put("/client/3", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["message"] == "password is not accepted"
        assert res_json["status"] == "FAILED"

        # add new client
        data = {"client_key": "wawew4", "client_secret": "wawew123", "status": True}
        res = client.post("/client", json=data, headers={"Authorization": "Bearer "+token})
    
    # GET METHOD
    def test_internal_client_get_all(self, client):
        token = create_token()
        data = {}
        res = client.get("/client", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_internal_client_get_all_filtered(self, client):
        token = create_token()
        data = {"p": 1, "rp": 10, "status": True}
        res = client.get("/client", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_internal_client_get_id(self, client):
        token = create_token()
        res = client.get("/client/1", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_internal_client_get_id_deleted(self, client):
        token = create_token()
        res = client.get("/client/2", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    def test_internal_client_get_id_not_found(self, client):
        token = create_token()
        res = client.get("/client/1000", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"

    # NON-INTERNAL
    def test_noninternal_client_post(self, client):
        token = create_token(is_internal=False)
        data = {"client_key": "wawew4", "client_secret": "wawew123", "status": True}
        res = client.post("/client", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
        assert res_json["message"] == "internal only!"