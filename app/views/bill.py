from flask import Flask, render_template, request, redirect, session, Blueprint, jsonify
from .login import auth
from .. import charge_system
from .. import billing_system

bill = Blueprint("bill", __name__)

@bill.route("/bill",methods=["GET", "POST"])
@auth
def tobill():
    username = session.get('user')
    return render_template('bill.html')

@bill.route("/changebill",methods=["GET", "POST"])
@auth
def tobill():
    username = session.get('user')
    return render_template('bill.html')

@bill.route("/deletebill",methods=["GET", "POST"])
@auth
def tobill():
    username = session.get('user')
    return render_template('bill.html')