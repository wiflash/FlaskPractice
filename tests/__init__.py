import pytest, logging, hashlib, json
from blueprints import app, db
from blueprints.client.model import *
from blueprints.book.model import *
from blueprints.user.model import *
from flask import Flask, request
from app import cache


def call_client(request):
    client = app.test_client()
    return client

def reset_db():
    db.drop_all()
    db.create_all()
    client = Clients("wawew1", hashlib.md5("wawew123".encode()).hexdigest(), True)
    book = Books("Judul Buku1", "12-2399-2", "Pengarang1")
    db.session.add(client)
    db.session.add(book)
    db.session.commit()
    
    user = Users("user1", 21, "Male", 1)
    db.session.add(user)
    db.session.commit()

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(is_internal=True):
    if is_internal: cache_client = "test_token_internal"
    else: cache_client = "test_token_noninternal"
    token = cache.get(cache_client)
    if token is None:
        # prepare request input
        if is_internal:
            data = {
                "client_key": "internal",
                "client_secret": "th1s1s1nt3n4lcl13nt"
            }
        else:
            data = {
                "client_key": "wawew1",
                "client_secret": "wawew123"
            }
        # do request
        req = call_client(request)
        res = req.get("/token", query_string=data)
        # store response
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        # compare with expected result
        assert res.status_code == 200
        assert res_json["message"] == "token created"
        # save token into cache
        cache.set(cache_client, res_json["token"], timeout=30)
        # return
        return res_json["token"]
    return token