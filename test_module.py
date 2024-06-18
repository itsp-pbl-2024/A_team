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
    result = client.post("/send", json={"id": 10, "durations": ["6.4"]})
    assert result.status_code == 200
    assert b'User_id: 10, durations: ["6.4"]' == result.data


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
    result = client.post("/send", json={"id": 0, "room_id": 1, "durations": ["3.5"]})
    assert result.status_code == 200
    assert b'User_id: 0, durations: ["3.5"]' == result.data

    result = client.post("/send", json={"id": 1, "room_id": 1, "durations": ["1.1"]})
    assert result.status_code == 200
    assert b'User_id: 1, durations: ["1.1"]' == result.data

    result = client.post("/send", json={"id": 2, "room_id": 1, "durations": ["6.4"]})
    assert result.status_code == 200
    assert b'User_id: 2, durations: ["6.4"]' == result.data

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"1 is quiet" == result.data


# id 0がquietの場合
def test_flask_S002():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 3})

    # send
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["1.6"]})
    client.post("/send", json={"id": 3, "room_id": 1, "durations": ["3.2"]})
    client.post("/send", json={"id": 2, "room_id": 1, "durations": ["4.0"]})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"0 is quiet" == result.data


# id 3が話しておらず、quietの場合
def test_flask_S003():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 5})

    # send
    client.post("/send", json={"id": 0, "room_id": 1, "durations": ["1.4"]})
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["2.4"]})
    client.post("/send", json={"id": 2, "room_id": 1, "durations": ["3.4"]})
    client.post("/send", json={"id": 4, "room_id": 1, "durations": ["0.4"]})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"3 is quiet" == result.data


# 同率の場合はidが一番小さいuserが呼ばれる
def test_flask_S004():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 5})

    # send
    client.post("/send", json={"id": 0, "room_id": 1, "durations": ["3.2"]})
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["1.2"]})
    client.post("/send", json={"id": 2, "room_id": 1, "durations": ["2.2"]})
    client.post("/send", json={"id": 3, "room_id": 1, "durations": ["1.2"]})
    client.post("/send", json={"id": 4, "room_id": 1, "durations": ["1.2"]})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"1 is quiet" == result.data


# 2つ要素
def test_flask_S005():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 5})

    # send
    client.post("/send", json={"id": 0, "room_id": 1, "durations": ["1.9", "9.1"]})
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["2.9", "7.1"]})
    client.post("/send", json={"id": 2, "room_id": 1, "durations": ["3.9", "5.1"]})
    client.post("/send", json={"id": 3, "room_id": 1, "durations": ["4.9", "3.1"]})
    client.post("/send", json={"id": 4, "room_id": 1, "durations": ["5.9", "1.1"]})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"4 is quiet" == result.data


# 3つ以上
def test_flask_S006():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 5})

    # send
    client.post("/send", json={"id": 0, "room_id": 1, "durations": ["1.0", "1.0", "2.2"]})
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["3.0", "0.1", "0.1", "0.1", "0.6"]})
    client.post("/send", json={"id": 2, "room_id": 1, "durations": ["4.0", "1.0"]})
    client.post("/send", json={"id": 3, "room_id": 1, "durations": ["5.0"]})
    client.post("/send", json={"id": 4, "room_id": 1, "durations": ["3.2", "2.3", "4.1", "1.5", "2.2", "0.5"]})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"1 is quiet" == result.data


# 1人が複数回send発行
def test_flask_S007():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 5})

    # send
    client.post("/send", json={"id": 0, "room_id": 1, "durations": ["7.5"]})
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["0.1"]})
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["4.0"]})
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["0.1"]})
    client.post("/send", json={"id": 2, "room_id": 1, "durations": ["0.1", "2.2"]})
    client.post("/send", json={"id": 3, "room_id": 1, "durations": ["0.4"]})
    client.post("/send", json={"id": 3, "room_id": 1, "durations": ["0.5"]})
    client.post("/send", json={"id": 3, "room_id": 1, "durations": ["0.4", "1.1"]})
    client.post("/send", json={"id": 4, "room_id": 1, "durations": ["10.2"]})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"3 is quiet" == result.data


# 複数回check
def test_flask_S008():
    app = create_app()
    # テスト用コンフィグをtrueに設定
    app.config["TESTING"] = True
    # テスト対象API呼び出し用テストクライアント生成
    client = app.test_client()
    # register
    client.post("/register", json={"n": 5})

    # send
    client.post("/send", json={"id": 0, "room_id": 1, "durations": ["3.0"]})
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["2.0"]})
    client.post("/send", json={"id": 2, "room_id": 1, "durations": ["4.0"]})
    client.post("/send", json={"id": 3, "room_id": 1, "durations": ["5.0"]})
    client.post("/send", json={"id": 4, "room_id": 1, "durations": ["6.0"]})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"1 is quiet" == result.data

    # send
    client.post("/send", json={"id": 1, "room_id": 1, "durations": ["18.0"]})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"0 is quiet" == result.data
