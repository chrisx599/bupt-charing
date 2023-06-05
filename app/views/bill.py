from flask import Flask, render_template, request, redirect, session, Blueprint, jsonify
from .login import auth
from .. import charge_system
from .. import billing_system

bill = Blueprint("bill", __name__)

@bill.route("/bill",methods=["GET", "POST"])
@auth
def tobill():
    username = session.get('user')
    data_list = billing_system.get_user_bill(username)
    print(data_list)
    return render_template('bill.html',order=data_list)
