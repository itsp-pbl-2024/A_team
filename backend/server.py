from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


# 参加者の人数をから受け取る
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if "n" not in data:
        return "Invalid request."
    n = data["n"]
    if n < 0:
        return "Invalid number of people."
    return f"You are going to talk with {n} people."


# ユーザーIDとメッセージの内容を受け取る
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    if "id" not in data or "message" not in data:
        return "Invalid request."
    return f"User{data['id']} said '{data['message']}'."


@app.route("/check", methods=["GET"])
def check():
    # id=f()
    return "id" + "is quiet"


if __name__ == "__main__":
    app.run()
