from flask import Flask, render_template, request, redirect

from config import Config

app = Flask(__name__)
# app.config.from_object(Config)
db = Config()

# 域名后面跟的东西
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    passward = request.form.get("password")
    # print(username, passward)

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
            return redirect("/")
        pwd_error = "密码错误"
        return render_template("login.html", error=pwd_error)
    else:
        # print("66666666")
        name_error = "用户名不存在"
        return render_template("login.html", error=name_error)
    # 获取全部数据
    # all_ = cursor.fetchall()
    # for i in all_:
    #         print(i[0])
    #         print(i[1])

    
@app.route("/register", methods=["GET", "POST"])
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
    # result = cursor.fetchone()
    # print(result)
    return redirect("/login")
    

if __name__ == "__main__":
    # import os
    # print(os.getcwd())
    app.run()