from flask import Flask, render_template, request, redirect, session
from .database import DBConfig
from .views.charger_system import ChargeSystem


def create_app():
    app = Flask(__name__)
    app.secret_key = "f5ea81gg4s61g68awfa981ber9iuy"
    from .views.login import user_login
    from .views.charge import charge
    from .views.admin import admin

    app.register_blueprint(charge)
    app.register_blueprint(user_login)
    app.register_blueprint(admin)


    return app

def get_db():
    db = DBConfig()
    return db


def get_charge_system():
    charge_system = ChargeSystem()
    return charge_system

charge_system = get_charge_system()