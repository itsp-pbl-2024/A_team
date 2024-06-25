from flask import Blueprint, request, current_app
from util import is_int
import json

get_speaking_time_blueprint = Blueprint("get_speaking_time", __name__)


@get_speaking_time_blueprint.route("/get_speaking_time", methods=["GET"])
def get_speaking_time():
    data = request.get_json()
    if "id" not in data:
        return "Invalid request."
    room = current_app.config["ROOMS"].get_room(current_app.config["ROOM_ID_DEMO"])
    id = data["id"]
    if not is_int(id) or id < 0 or id >= len(room.get_participants().get_participants()):
        return "Invalid request."
    latests = room.get_latests()
    return f"'id': {id}, 'duration': {latests[int(id)]}"
