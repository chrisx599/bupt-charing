from flask import Flask, render_template, request, redirect, session
from .views.charger_system import ChargeSystem
from .views.billing_system import BillingSystem
from .database import DBConfig

def create_app():
    app = Flask(__name__)
    app.secret_key = "f5ea81gg4s61g68awfa981ber9iuy"
    from .views.login import user_login
    from .views.charge import charge
    from .views.admin import admin
    from .views.bill import bill

    app.register_blueprint(charge)
    app.register_blueprint(user_login)
    app.register_blueprint(admin)
    app.register_blueprint(bill)


    return app

def get_db():
    db = DBConfig()
    return db


def get_charge_system(db):
    charge_system = ChargeSystem(db)
    return charge_system


def get_billing_system(db, charge_system):
    billing_system = BillingSystem(db, charge_system)
    return billing_system

db = get_db()
charge_system = get_charge_system(db)
billing_system = get_billing_system(db, charge_system)
