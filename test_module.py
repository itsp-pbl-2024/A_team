import pytest

# テスト対象APIコードのappをインポート
from backend.server import create_app


# hello
def test_flask_N001():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # テスト対象API実行
    result = client.get("/")
    assert result.status_code == 200
    assert b"Hello World!" == result.data


# register successful case
def test_flask_N002():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    for i in range(1, 3):
        result = client.post("/register", json={"n": i})
        assert result.status_code == 200
        assert f"You are going to talk with {i} people.".encode() == result.data


# register failed case (Invalid request)
def test_flask_N003():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    result = client.post("/register", json={"m": 10})
    assert result.status_code == 200
    assert b"Invalid request." == result.data


# register failed case (Invalid number of people)
def test_flask_N004():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    result = client.post("/register", json={"n": 0})
    assert result.status_code == 200
    assert b"Invalid number of people." == result.data


# send successful case
def test_flask_N005():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    client.post("/register", json={"n": 11})
    result = client.post("/send", json={"id": 10, "message": "Hello"})
    assert result.status_code == 200
    assert b"User10 said 'Hello'." == result.data


# registerで人数登録して、sendで複数人のメッセージを送信する。最後にcheckでメッセージを確認する
def test_flask_S001():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    result = client.post("/register", json={"n": 3})
    assert result.status_code == 200
    assert b"You are going to talk with 3 people." == result.data

    # send
    result = client.post("/send", json={"id": 1, "room_id": 1, "message": "Hello"})
    assert result.status_code == 200
    assert b"User1 said 'Hello'." == result.data

    result = client.post("/send", json={"id": 2, "room_id": 1, "message": "Hi"})
    assert result.status_code == 200
    assert b"User2 said 'Hi'." == result.data

    result = client.post(
        "/send", json={"id": 3, "room_id": 1, "message": "Good morning"}
    )
    assert result.status_code == 200
    assert b"User3 said 'Good morning'." == result.data

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"2 is quiet" == result.data


# id 1がquietの場合
def test_flask_S002():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 3})

    # send
    client.post("/send", json={"id": 1, "room_id": 1, "message": "Hi"})
    client.post("/send", json={"id": 3, "room_id": 1, "message": "Good morning"})
    client.post("/send", json={"id": 2, "room_id": 1, "message": "How are you?"})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"1 is quiet" == result.data


# id 4が話しておらず、quietの場合
def test_flask_S003():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 5})

    # send
    client.post("/send", json={"id": 1, "room_id": 1, "message": "Hello"})
    client.post("/send", json={"id": 2, "room_id": 1, "message": "Hi"})
    client.post("/send", json={"id": 3, "room_id": 1, "message": "Good morning"})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"4 is quiet" == result.data
