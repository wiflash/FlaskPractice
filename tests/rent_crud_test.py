# import json, logging
# from . import client, create_token, reset_db
# from password_strength import PasswordPolicy

# class TestUserCrud():
#     reset_db()
#     id_user = 0
#     # POST METHOD
#     def test_internal_user_post(self, client):
#         token = create_token()
#         data = {"name":"user2", "age":21, "sex":"Male", "client_id":1}
#         res = client.post("/user", json=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 200
#         assert res_json["name"] == data["name"]
#         assert res_json["age"] == data["age"]
#         assert res_json["sex"] == data["sex"]
#         assert res_json["client_id"] == data["client_id"]
#         self.id_user = res_json["id"]
#     def test_internal_user_post_but_client_id_is_deleted(self, client):
#         token = create_token()
#         data = {"name":"user2", "age":21, "sex":"Male", "client_id":2}
#         res = client.post("/user", json=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "client_id not found"
#     def test_internal_user_post_but_client_id_not_found(self, client):
#         token = create_token()
#         data = {"name":"user2", "age":21, "sex":"Male", "client_id":100}
#         res = client.post("/user", json=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "client_id not found"
    
#     # DELETE METHOD
#     def test_internal_user_delete_id(self, client):
#         token = create_token()
#         res = client.delete("/user/2", headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 200
#         assert res_json["message"] == "Deleted"
#     def test_internal_user_delete_id_but_already_deleted(self, client):
#         token = create_token()
#         res = client.delete("/user/2", headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "NOT_FOUND"
#     def test_internal_user_delete_id_not_found(self, client):
#         token = create_token()
#         res = client.delete("/user/100", headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "NOT_FOUND"
    
#     # PUT METHOD
#     def test_internal_user_put_id(self, client):
#         token = create_token()
#         data = {"name":"user3", "age":21, "sex":"Male", "client_id":1}
#         res = client.post("/user", json=data, headers={"Authorization": "Bearer "+token})
#         data = {"name":"user3 (edited)", "age":21, "sex":"Male", "client_id":1}
#         res = client.put("/user/3", json=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 200
#         assert res_json["name"] == data["name"]
#         assert res_json["age"] == data["age"]
#         assert res_json["sex"] == data["sex"]
#         assert res_json["client_id"] == data["client_id"]
#         self.id_user = res_json["id"]
#     def test_internal_user_put_but_deleted_id(self, client):
#         token = create_token()
#         data = {"name":"user2 (edited)", "age":21, "sex":"Male", "client_id":1}
#         res = client.put("/user/2", json=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "NOT_FOUND"
#     def test_internal_user_put_but_id_not_found(self, client):
#         token = create_token()
#         data = {"name":"user1000 (edited)", "age":21, "sex":"Male", "client_id":1}
#         res = client.put("/user/1000", json=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "NOT_FOUND"
#     def test_internal_user_put_but_client_id_doesnt_exist_or_deleted(self, client):
#         token = create_token()
#         data = {"name":"user1 (edited)", "age":21, "sex":"Male", "client_id":100}
#         res = client.put("/user/1", json=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "client_id not found"
    
#     # GET METHOD
#     def test_internal_user_get_all(self, client):
#         token = create_token()
#         data = {"p": 1, "rp": 10}
#         res = client.get("/user", query_string=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 200
#     def test_internal_user_get_id(self, client):
#         token = create_token()
#         res = client.get("/user/1", headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 200
#     def test_internal_user_get_id_deleted(self, client):
#         token = create_token()
#         res = client.get("/user/2", headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "NOT_FOUND"
#     def test_internal_user_get_id_not_found(self, client):
#         token = create_token()
#         res = client.get("/user/1000", headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "NOT_FOUND"
#     def test_internal_user_get_id_but_client_id_doesnt_exist_or_deleted(self, client):
#         token = create_token()
#         # add new user
#         data = {"name":"user4", "age":21, "sex":"Male", "client_id":4}
#         client.post("/user", json=data, headers={"Authorization": "Bearer "+token})
#         # delete client with id=4
#         client.delete("/client/4", headers={"Authorization": "Bearer "+token})
#         # continue test
#         res = client.get("/user/4", headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 404
#         assert res_json["message"] == "NOT_FOUND"

#     # NON-INTERNAL
#     def test_noninternal_user_post(self, client):
#         token = create_token(is_internal=False)
#         data = {"name":"user5", "age":21, "sex":"Male", "client_id":1}
#         res = client.post("/user", json=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 403
#         assert res_json["status"] == "FORBIDDEN"
#         assert res_json["message"] == "internal only!"