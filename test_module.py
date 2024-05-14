import pytest

# テスト対象APIコードのappをインポート
from backend.server import app

# テスト用コンフィグをtrueに設定
app.config["TESTING"] = True
# テスト対象API呼び出し用テストクライアント生成
client = app.test_client()

#hello
def test_flask_N001():
    # テスト対象API実行
    result = client.get("/")
    assert result.status_code == 200
    assert b"Hello World!" == result.data

#register successful case
def test_flask_N002():
    for i in range(1,3):
        result = client.post("/register", json={"n": i})
        assert result.status_code == 200
        assert f"You are going to talk with {i} people.".encode() == result.data

#register failed case (Invalid request)
def test_flask_N003():
    result = client.post("/register", json={"m": 10})
    assert result.status_code == 200
    assert b"Invalid request." == result.data

#register failed case (Invalid number of people)
def test_flask_N004():
    result = client.post("/register", json={"n": 0})
    assert result.status_code == 200
    assert b"Invalid number of people." == result.data

#send successful case
def test_flask_N005():
    result = client.post("/send", json={"id": 10, "message": "Hello"})
    assert result.status_code == 200
    assert b"User10 said 'Hello'." == result.data