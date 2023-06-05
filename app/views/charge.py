from .charger_system import Car
from flask import Flask, render_template, request, redirect, session, Blueprint, jsonify
from .login import auth
from .. import charge_system

charge = Blueprint("charge", __name__)

# 域名后面跟的东西
@charge.route("/", methods=["GET", "POST"])
@auth
def index():
    username = session.get('user')
    if username == "admin":
        return render_template("admin_home.html")
    if request.method == "GET":
        return render_template("index.html", username=username)

    charge_mode = request.form.get('charge_mode')
    car_id = request.form.get('car_id')
    car_need_power = request.form.get('car_need_power')
    # 充电模式分类
    if charge_mode == 'fast':
        # 查看等待区是否还有位置
        if not charge_system.is_wait_area_full():
            request_car = Car(username, car_id, car_need_power, charge_mode)
            charge_system.fast_wait_area_queue.put(request_car)
            print("快充等待区数量:", charge_system.fast_wait_area_queue.qsize())
            return "add fast true"
        else:
            return "add fast false"
    elif charge_mode == 'slow':
        if not charge_system.is_wait_area_full():
            request_car = Car(username, car_id, car_need_power, charge_mode)
            charge_system.slow_wait_area_queue.put(request_car)
            return "add slow true"
        else:
            return "add slow false"
    else:
        return "error"

@charge.route('/api/data', methods=['GET'])
def get_data():
    # 返回最新的数据
    # 分两个区充电区和等待区
    data = {'charge_area': {'fast_charger': [{'charger_queue_size': str(charge_system.fast_charger[0].queue.qsize())},
                                              {'charger_queue_size': str(charge_system.fast_charger[1].queue.qsize())}],
                             'slow_charger': [{'charger_queue_size': str(charge_system.slow_charger[0].queue.qsize())},
                                              {'charger_queue_size': str(charge_system.slow_charger[1].queue.qsize())},
                                              {'charger_queue_size': str(charge_system.slow_charger[2].queue.qsize())}]},
            'wait_area': {'fast_wait_car_number': str(charge_system.fast_wait_area_queue.qsize()),
                          'slow_wait_car_number': str(charge_system.slow_wait_area_queue.qsize())},
            'charger_state': {'fast_charger1': str(charge_system.fast_charger[0].charger_state),
                              'fast_charger2': str(charge_system.fast_charger[1].charger_state),
                              'slow_charger1': str(charge_system.slow_charger[0].charger_state),
                              'slow_charger2': str(charge_system.slow_charger[1].charger_state),
                              'slow_charger3': str(charge_system.slow_charger[2].charger_state),
            }}
    return jsonify(data)






