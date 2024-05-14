from flask import Flask
from flask import request
from rooms import Rooms
from message import Message

app = Flask(__name__)

all_room = Rooms()


@app.route("/")
def hello():
    return "Hello World!"


# 参加者の人数をから受け取る
@app.route("/register", methods=["POST"])
def register():
    n = request.get_json()["n"]
    room_id = all_room.create_room(n)
    return f"You are going to talk with {n} people."


# ユーザーIDとメッセージの内容を受け取る
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    room = all_room.get_room(data["room_id"])
    message = Message(data)
    room.add_message(message)
    return f"User{data['id']} said '{data['message']}'."


if __name__ == "__main__":
    app.run()
