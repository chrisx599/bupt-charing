# -*- coding:utf-8 -*-
# @FileName : admin.py
# @Time     : 2023/6/4 12:46
# @Author   : qingyao
from flask import Flask, render_template, request, redirect, session, Blueprint, make_response,jsonify
from .. import charge_system

admin = Blueprint("admin", __name__)

@admin.route("/a/show/pilesinfo")
def pile_info():
    # 整合时放开注释
    pile_id = int(request.args.get("pile_id"))
    if pile_id < 3:
        pile = charge_system.fast_charger[pile_id - 1]
    else:
        pile = charge_system.slow_charger[pile_id - 3]
    data = {"isWorking": pile.charger_state,
            "totalTimes": pile.total_times,
            "totalTime": pile.total_charge_time,
            "totalEnergy": pile.total_charge_power,
            "isUsing": pile.use_state}
    # print(data)
    return jsonify(data)

@admin.route("/a/changeState")
def changeState():

    pile_id = int(request.args.get("pile_id"))
    if pile_id < 3:
        pile = charge_system.fast_charger[pile_id - 1]
    else:
        pile = charge_system.slow_charger[pile_id - 3]
    pile.charger_state = not pile.charger_state

    data = {"status_code": True}
    return jsonify(data)

@admin.route("/a/home")
def to_home():
    return render_template("admin_home.html")

@admin.route("/a/report")
def to_report():
    return render_template("admin_report.html")

@admin.route("/a/getreports")
def get_reports():
    # 从数据库中取数据，取全表，reports表，已建
    # 构建返还值按照以下格式构建、
    # 查看数据库表得到详细数据类型，以下只是一个样例，数据类型和表中类型不相同
    # 构建jsonData时要求日期必须是字符串

    jsonData = {
        "rows": [
            [1, "2012-5-3", 3, 3, 120, 150, 120, 120, 120],
            [],
            [],
        ]
    }
    return jsonify(jsonData)

@admin.route("/a/waiting")
def to_waiting():
    # 此处通过获取数据库中的reports表创建json对象，直接获取全表内容即可
    # 以下是测试
    return render_template("admin_waiting.html")

@admin.route("/a/logout")
def logout():
    # 重定向到登录页面
    # 退出登录如果需要清除一些数据可以在这里清除
    # 没有cookies，不需要清除cookies
    # session中没有管理员信息
    session.clear()
    return render_template('login.html')
    # return render_template()
    # 前端关联事件未绑定


if __name__ == "__main__":
    jsonData = {
        "rows": [
            [1, 2012 - 5 - 3, 2, 3, 120, 133, 150, 160, 310]
        ]
    }

