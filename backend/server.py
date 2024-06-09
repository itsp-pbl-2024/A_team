from flask import Flask
from rooms import Rooms
from routes.register import register_blueprint
from routes.send import send_blueprint
from routes.check import check_blueprint


def create_app():
    app = Flask(__name__)
    app.config["ROOMS"] = Rooms()
    app.config["ROOM_ID_DEMO"] = 1

    # 参加者の人数をJSONファイルから受け取りROOMを作成
    app.register_blueprint(register_blueprint)

    # ユーザーIDとメッセージの内容を受け取る
    app.register_blueprint(send_blueprint)

    app.register_blueprint(check_blueprint)

    @app.route("/")
    def hello():
        return "Hello World!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
