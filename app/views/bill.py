from flask import Flask, render_template, request, redirect, session, Blueprint, jsonify
from .login import auth
from .. import charge_system
from .. import billing_system

bill = Blueprint("bill",__name__)

@bill.route("/bill",methods=["GET", "POST"])
@auth
def bill():
    username = session.get('username')
    return render_template('bill.html')