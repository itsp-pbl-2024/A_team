from flask import Flask
from flask import request
from rooms import Rooms
from message import Message


def create_app():
    app = Flask(__name__)
    all_room = Rooms()
    ROOM_ID_DEMO = 1

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
        if n <= 0:
            return "Invalid number of people."
        n = request.get_json()["n"]
        all_room.create_room(n)
        return f"You are going to talk with {n} people."

    # ユーザーIDとメッセージの内容を受け取る
    @app.route("/send", methods=["POST"])
    def send():
        data = request.get_json()
        if "id" not in data or "message" not in data:
            return "Invalid request."
        room = all_room.get_room(ROOM_ID_DEMO)
        message = Message(data)
        room.add_message(message)
        return f"User{data['id']} said '{data['message']}'."

    @app.route("/check", methods=["GET"])
    def check():
        room = all_room.get_room(ROOM_ID_DEMO)
        quiet_id = room.search_alone().get_user_name()
        return f"{quiet_id}" + " is quiet"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
