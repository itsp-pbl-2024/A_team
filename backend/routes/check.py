from flask import Blueprint, current_app

check_blueprint = Blueprint("check", __name__)


@check_blueprint.route("/check", methods=["GET"])
def check():
    room = current_app.config["ROOMS"].get_room(current_app.config["ROOM_ID_DEMO"])
    quiet_id = room.search_alone()
    return f"{quiet_id} is quiet"
