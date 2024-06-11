from flask import Blueprint, request, current_app
from message import Message

send_blueprint = Blueprint("send", __name__)


# ユーザーIDとメッセージの内容を受け取る
@send_blueprint.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    if "id" not in data or "message" not in data:
        return "Invalid request."
    room = current_app.config["ROOMS"].get_room(current_app.config["ROOM_ID_DEMO"])
    message = Message(data)
    room.add_message(message)
    return f"User{data['id']} said '{data['message']}'."
