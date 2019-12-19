import json, logging
from . import client, create_token, reset_db
from password_strength import PasswordPolicy

class TestRentCrud():
    reset_db()
    id_rent = 0
    # POST METHOD
    def test_internal_rent_post(self, client):
        token = create_token()
        data = {"book_id":3, "user_id":3}
        res = client.post("/rent", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["book_id"] == data["book_id"]
        assert res_json["user_id"] == data["user_id"]
        self.id_rent = res_json["id"]
    def test_internal_rent_post_but_book_id_is_deleted(self, client):
        token = create_token()
        data = {"book_id":2, "user_id":1}
        res = client.post("/rent", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "book_id not found"
    def test_internal_rent_post_but_book_id_not_found(self, client):
        token = create_token()
        data = {"book_id":100, "user_id":1}
        res = client.post("/rent", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "book_id not found"
    def test_internal_rent_post_but_user_id_is_deleted(self, client):
        token = create_token()
        data = {"book_id":3, "user_id":2}
        res = client.post("/rent", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "user_id not found"
    def test_internal_rent_post_but_user_id_not_found(self, client):
        token = create_token()
        data = {"book_id":3, "user_id":100}
        res = client.post("/rent", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "user_id not found"

    # GET METHOD
    def test_noninternal_rent_get_all(self, client):
        token = create_token(is_internal=False)
        data = {}
        res = client.get("/rent", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_noninternal_rent_get_all_filtered(self, client):
        token = create_token(is_internal=False)
        data = {"p": 1, "rp": 10, "book_id":1, "user_id":1}
        res = client.get("/rent", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_noninternal_rent_get_id(self, client):
        token = create_token(is_internal=False)
        res = client.get("/rent/1", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_noninternal_rent_get_id_not_found(self, client):
        token = create_token(is_internal=False)
        res = client.get("/rent/100", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    def test_noninternal_rent_get_id_but_user_id_doesnt_exist(self, client):
        token = create_token()
        # add new user
        data = {"name":"user5", "age":21, "sex":"Male", "client_id":3}
        client.post("/user", json=data, headers={"Authorization": "Bearer "+token})
        # add new rent
        data = {"book_id":3, "user_id":5}
        client.post("/rent", json=data, headers={"Authorization": "Bearer "+token})
        # delete user with id=5
        client.delete("/user/5", headers={"Authorization": "Bearer "+token})
        # continue test
        token = create_token(is_internal=False)
        res = client.get("/rent/3", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    
    def test_noninternal_rent_get_id_but_book_id_doesnt_exist(self, client):
        token = create_token()
        # add new book
        data = {"title": "Judul Buku4", "isbn": "1234-5678", "writer": "Pengarang4"}
        res = client.post("/book", json=data, headers={"Authorization": "Bearer "+token})
        # add new rent
        data = {"book_id":4, "user_id":1}
        client.post("/rent", json=data, headers={"Authorization": "Bearer "+token})
        # delete book with id=4
        client.delete("/book/4", headers={"Authorization": "Bearer "+token})
        # continue test
        token = create_token(is_internal=False)
        res = client.get("/rent/4", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"

    # NON-INTERNAL ACCESSES TO INTERNAL-ONLY
    def test_noninternal_rent_post(self, client):
        token = create_token(is_internal=False)
        data = {"book_id":3, "user_id":3}
        res = client.post("/rent", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
        assert res_json["message"] == "internal only!"
    
    # INTERNAL ACCESSES TO NON-INTERNAL-ONLY
    def test_noninternal_rent_get_all(self, client):
        token = create_token()
        data = {}
        res = client.get("/rent", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
        assert res_json["message"] == "non-internal only!"