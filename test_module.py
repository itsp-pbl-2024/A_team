import pytest

# テスト対象APIコードのappをインポート
from backend.server import app


def test_flask_N001():
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()

    # テスト対象API実行
    result = client.get("/")
    assert result.status_code == 200
    assert b"Hello World!" == result.data


def test_flask_N002():
    app.config["TESTING"] = True
    client = app.test_client()

    # テスト対象API実行
    result = client.post("/register", json={"n": 3})
    assert result.status_code == 200
    assert b"You are going to talk with 3 people." == result.data


def test_flask_N003():
    app.config["TESTING"] = True
    client = app.test_client()

    # テスト対象API実行
    result = client.post("/send", json={"id": 1, "message": "Hello"})
    assert result.status_code == 200
    assert b"User1 said 'Hello'." == result.data

#register if n<=0 value error
def test_flask_N004():
    app.config["TESTING"] = True
    client = app.test_client()

    # テスト対象API実行
    result = client.get("/register", json={"n": 0})
    assert result.status_code == 200
    assert b"Invalid number of people." == result.data

#send if id<=0 value error
def test_flask_N005():
    app.config["TESTING"] = True
    client = app.test_client()

    # テスト対象API実行
    result = client.post("/send", json={"id": 0, "message": "Hello"})
    assert result.status_code == 200
    assert b"Invalid request." == result.data