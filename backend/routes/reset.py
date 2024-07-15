from flask import Blueprint, request, current_app
from message import Message

reset_blueprint = Blueprint("reset", __name__)


# ルーム内の全員の発言量をリセットする
@reset_blueprint.route("/reset", methods=["POST"])
def reset():
    room = current_app.config["ROOMS"].get_room(current_app.config["ROOM_ID_DEMO"])
    room.reset_latests()
    return f"Reset the speaking amount of all participants in the room {current_app.config['ROOM_ID_DEMO']}."
