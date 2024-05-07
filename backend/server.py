from flask import Flask
from flask import request

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
    return f"User{data['id']} said '{data['message']}'."


if __name__ == "__main__":
    app.run()
