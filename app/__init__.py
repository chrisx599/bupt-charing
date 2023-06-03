from flask import Flask, render_template, request, redirect, session
from .database import DBConfig



def create_app():
    app = Flask(__name__)
    app.secret_key = "f5ea81gg4s61g68awfa981ber9iuy"
    from .views.login import user_login, auth

    # 域名后面跟的东西
    @app.route("/", methods=["GET", "POST"])
    @auth
    def index():
        return render_template("index.html")

    app.register_blueprint(user_login)
    return app

def get_db():
    db = DBConfig()
    return db