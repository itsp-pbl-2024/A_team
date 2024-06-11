from flask import Blueprint, request, current_app

register_blueprint = Blueprint("register", __name__)


@register_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if "n" not in data:
        return "Invalid request."
    n = data["n"]
    if n <= 0:
        return "Invalid number of people."
    n = request.get_json()["n"]
    all_room = current_app.config["ROOMS"]
    all_room.create_room(n)
    return f"You are going to talk with {n} people."
