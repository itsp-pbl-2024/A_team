from flask import Flask
from flask import request
from roomlist import RoomList
from message import Message

app = Flask(__name__)

all_room = RoomList()


@app.route("/")
def hello():
    return "Hello World!"


# 参加者の人数をから受け取る
@app.route("/register", methods=["POST"])
def register():
    n = request.get_json()["n"]
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
