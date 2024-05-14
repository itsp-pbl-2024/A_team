import pytest

"""
# 参加者の人数をから受け取る
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if "n" not in data:
        return "Invalid request."
    n = data["n"]
    if n <= 0:
        return "Invalid number of people."
    n = request.get_json()["n"]
    room_id = all_room.create_room(n)
    return f"You are going to talk with {n} people."


# ユーザーIDとメッセージの内容を受け取る
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    if "id" not in data or "message" not in data:
        return "Invalid request."
    room = all_room.get_room(data["room_id"])
    message = Message(data)
    room.add_message(message)
    return f"User{data['id']} said '{data['message']}'."


@app.route("/check", methods=["GET"])
def check():
    # id=f()
    return "id" + " is quiet"
"""
# テスト対象APIコードのappをインポート
from backend.server import app

# テスト用コンフィグをtrueに設定
app.config["TESTING"] = True
# テスト対象API呼び出し用テストクライアント生成
client = app.test_client()


# hello
def test_flask_N001():
    # テスト対象API実行
    result = client.get("/")
    assert result.status_code == 200
    assert b"Hello World!" == result.data


# register successful case
def test_flask_N002():
    for i in range(1, 3):
        result = client.post("/register", json={"n": i})
        assert result.status_code == 200
        assert f"You are going to talk with {i} people.".encode() == result.data


# register failed case (Invalid request)
def test_flask_N003():
    result = client.post("/register", json={"m": 10})
    assert result.status_code == 200
    assert b"Invalid request." == result.data


# register failed case (Invalid number of people)
def test_flask_N004():
    result = client.post("/register", json={"n": 0})
    assert result.status_code == 200
    assert b"Invalid number of people." == result.data


# send successful case
def test_flask_N005():
    result = client.post("/send", json={"id": 10, "message": "Hello"})
    assert result.status_code == 200
    assert b"User10 said 'Hello'." == result.data


# registerで人数登録して、sendで複数人のメッセージを送信する。最後にcheckでメッセージを確認する
def test_flask_S001():
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
    assert b"id is quiet" == result.data  # TODO: id 2 is quiet


# id 1がquietの場合
def test_flask_S002():
    # register
    client.post("/register", json={"n": 3})

    # send
    client.post("/send", json={"id": 2, "room_id": 1, "message": "Hi"})
    client.post("/send", json={"id": 3, "room_id": 1, "message": "Good morning"})
    client.post("/send", json={"id": 2, "room_id": 1, "message": "How are you?"})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"id is quiet" == result.data  # TODO: id 1 is quiet


def test_flask_S003():
    # register
    client.post("/register", json={"n": 5})

    # send
    client.post("/send", json={"id": 1, "room_id": 1, "message": "Hello"})
    client.post("/send", json={"id": 2, "room_id": 1, "message": "Hi"})
    client.post("/send", json={"id": 3, "room_id": 1, "message": "Good morning"})

    # check
    result = client.get("/check")
    assert result.status_code == 200
    assert b"id is quiet" == result.data  # TODO: id 4 is quiet
