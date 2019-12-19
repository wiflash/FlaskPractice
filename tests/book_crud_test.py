import json, logging
from . import client, create_token, reset_db
from password_strength import PasswordPolicy

class TestBookCrud():
    reset_db()
    # POST METHOD
    def test_internal_book_post(self, client):
        token = create_token()
        data = {"title": "Judul Buku2", "isbn": "1234-5678", "writer": "Pengarang2"}
        res = client.post("/book", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["title"] == data["title"]
        assert res_json["isbn"] == data["isbn"]
        assert res_json["writer"] == data["writer"]
    
    # DELETE METHOD
    def test_internal_book_delete_id(self, client):
        token = create_token()
        res = client.delete("/book/2", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["message"] == "Deleted"
    def test_internal_book_delete_id_but_already_deleted(self, client):
        token = create_token()
        res = client.delete("/book/2", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    def test_internal_book_delete_id_not_found(self, client):
        token = create_token()
        res = client.delete("/book/100", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    
    # PUT METHOD
    def test_internal_book_put_id(self, client):
        token = create_token()
        data = {"title": "Judul Buku3", "isbn": "1234-5678", "writer": "Pengarang3"}
        res = client.post("/book", json=data, headers={"Authorization": "Bearer "+token})
        data = {"title": "Judul Buku3 (edited)", "isbn": "1234-5678", "writer": "Pengarang3"}
        res = client.put("/book/3", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["title"] == data["title"]
        assert res_json["isbn"] == data["isbn"]
        assert res_json["writer"] == data["writer"]
    def test_internal_book_put_but_deleted_id(self, client):
        token = create_token()
        data = {"title": "Judul Buku2 (edited)", "isbn": "1234-5678", "writer": "Pengarang2"}
        res = client.put("/book/2", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    def test_internal_book_put_but_id_not_found(self, client):
        token = create_token()
        data = {"title": "Judul Buku1000 (edited)", "isbn": "1234-5678", "writer": "Pengarang1000"}
        res = client.put("/book/1000", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    
    # GET METHOD
    def test_internal_book_get_all(self, client):
        token = create_token()
        data = {"p": 1, "rp": 10, "title": "judul", "isbn": "1234-5678"}
        res = client.get("/book", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_internal_book_get_id(self, client):
        token = create_token()
        res = client.get("/book/1", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_internal_book_get_id_deleted(self, client):
        token = create_token()
        res = client.get("/book/2", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"
    def test_internal_book_get_id_not_found(self, client):
        token = create_token()
        res = client.get("/book/1000", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "NOT_FOUND"

    # NON-INTERNAL
    def test_noninternal_book_post(self, client):
        token = create_token(is_internal=False)
        data = {"title": "Judul Buku4", "isbn": "1234-5678", "writer": "Pengarang4"}
        res = client.post("/book", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
        assert res_json["message"] == "internal only!"