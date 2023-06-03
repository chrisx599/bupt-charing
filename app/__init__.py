from flask import Flask, render_template, request, redirect, session
from .database import DBConfig
from .views.charger import charge_system



def create_app():
    app = Flask(__name__)
    app.secret_key = "f5ea81gg4s61g68awfa981ber9iuy"
    from .views.login import user_login
    from .views.charge import charge


    app.register_blueprint(charge)
    app.register_blueprint(user_login)

    charge_system()

    return app

def get_db():
    db = DBConfig()
    return db
