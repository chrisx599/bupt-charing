from flask import Flask, render_template, request, redirect, session, Blueprint
import functools
from app import db

# db = get_db()
user_login = Blueprint("login", __name__)

def auth(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            username = session.get('user')
            if not username:
                return redirect("/login")
            return func(*args, **kwargs)
        return inner

@user_login.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    passward = request.form.get("password")

    # 创建游标对象
    # app.config
    cursor = db.connection.cursor()
    # sql语句
    sql = """
        select username, password
        from `user`
        where `username` = %s
    """
    # 执行sql语句
    cursor.execute(sql, [username])
    result = cursor.fetchone()
    if result:
        print(f"result{result}")
        if passward == result[1]:
            session['user'] = username
            return redirect("/")
        pwd_error = "密码错误"
        return render_template("login.html", error=pwd_error)
    else:
        name_error = "用户名不存在"
        return render_template("login.html", error=name_error)

@user_login.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get("username")
    passward = request.form.get("password")

    # 创建游标对象
    cursor = db.connection.cursor()
    # 首先保证用户名唯一
    sql = """
        select username, password
        from `user`
        where `username` = %s
        """
    cursor.execute(sql, [username])
    result = cursor.fetchone()
    if result:
        name_error = "用户名已存在"
        return render_template("register.html", error=name_error)

    sql = """
            insert into user (username, password)
            values (%s, %s);
        """
    # 执行sql语句
    cursor.execute(sql, [username, passward])
    db.connection.commit()
    return redirect("/login")