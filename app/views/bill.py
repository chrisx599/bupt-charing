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

@bill.route("/changebill",methods=["GET", "POST"])
@auth
def toedit():
    username = session.get('user')
    data_list = billing_system.get_user_bill(username)
    return render_template('edit_bill.html',order=data_list[0])

@bill.route("/deletebill",methods=["GET", "POST"])
@auth
def deletebill():
    username = session.get('user')
    if request.method == 'GET':
        return render_template('delbill.html')
    order_id = request.form.get("order_id")
    billing_system.del_user_bill(order_id)
    data_list = billing_system.get_user_bill(username)
    return render_template('bill.html', order=data_list)
