from .charger import init_charger, init_wait_area, implement_charge
from flask import Flask, render_template, request, redirect, session, Blueprint
from .login import auth

charge = Blueprint("charge", __name__)
fastcharger, slowcharger = init_charger()
wait_area_queue = init_wait_area()


# 域名后面跟的东西
@charge.route("/", methods=["GET", "POST"])
@auth
def index():
    username = session.get('user')
    charge_wait_area_state = []
    for item in fastcharger:
        charge_wait_area_state.append(list(item.queue.queue))
    for item in slowcharger:
        charge_wait_area_state.append(list(item.queue.queue))
    wait_area_state = list(wait_area_queue.queue)
    if request.method == "GET":
        return render_template("index.html", username=username, 
                            charge_wait_area_state=charge_wait_area_state
                            , wait_area_state=wait_area_state)

    charge_mode = request.form.get('charge_mode')
    car_id = request.form.get('car_id')
    car_need_power = request.form.get('car_need_power')

    imple_state = implement_charge(charge_mode, car_id, car_need_power
                                   , fastcharger, slowcharger, wait_area_queue
                                   , username)



