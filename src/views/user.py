from src.views.include import *
user = Blueprint("user", __name__)

@user.route("/register", methods=["GET", "POST"])
def user_register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["user_name"]
        password = request.form["pwd"]


        #密码加密
        s1 = sha1()
        s1.update(repr(password).encode('utf-8'))
        password = s1.hexdigest()

        phone_number = request.form["phone"]
        student_number = request.form["student_number"]
        student_number_info = db.session.query(StudentNumbers).filter(StudentNumbers.student_number == student_number).first()
        realname = student_number_info.realname
        sex = student_number_info.sex
        age = student_number_info.age
        institude = student_number_info.institude
        identity = student_number_info.identity
        u = Users(username=username)
        u.password=password
        u.head_portrait = "../static/images/default.png"
        u.student_number=student_number
        u.phone_number=phone_number
        u.realname=realname
        u.sex=sex
        u.age=age
        u.institute=institude
        u.identity=identity
        db.session.add(u)
        db.session.commit()
        db.session.close()
        return redirect("/login")


@user.route("/username_registered")
def username_registered():
    username = request.args["name"]
    count = db.session.query(Users).filter(Users.username==username).count()
    db.session.close()
    return json.dumps(count)


@user.route("/phone_registered")
def phone_registered():
    phone = request.args["phone"]
    count = db.session.query(Users).filter(Users.phone_number==phone).count()
    db.session.close()
    return json.dumps(count)


@user.route("/student_number_registered")
def student_number_registered():
    student_number = request.args["student_number"]
    count = db.session.query(Users).filter(Users.student_number==student_number).count()
    db.session.close()
    return json.dumps(count)


@user.route("/student_number_exist")
def student_number_exist():
    student_number = request.args["student_number"]
    count = db.session.query(StudentNumbers).filter(StudentNumbers.student_number==student_number).count()
    db.session.close()
    return json.dumps(count)


@user.route("/login",methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        source_url = "http://127.0.0.1:8500/"
        return render_template("login.html", source_url = source_url)
    else:
        username = request.form["user_name"]
        pwd = request.form["pwd"]
        count = db.session.query(Users).filter(Users.username==username).count()
        db.session.close()
        if count == 0:
            return render_template("login.html", error_username="用户名错误")
        #密码加密后与其库里的对比
        s1 = sha1()
        s1.update(repr(pwd).encode("utf-8"))
        pwd = s1.hexdigest()

        password = db.session.query(Users.password).filter(Users.username==username).first()
        if pwd != password[0]:
            return render_template("login.html", error_pwd="密码错误")
        else:
            source_url = request.form["source_url"]
            session["username"] = username
            return redirect(source_url)

@user.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")

@user.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")
    else:
        username = request.form["user_name"]
        phone = request.form["phone"]
        new_password = request.form["pwd"]
        count1 = db.session.query(Users).filter(Users.username==username).count()
        if count1 == 0:
            return render_template("forgot_password.html", error_name = "用户名不存在")
        count2 = db.session.query(Users).filter(Users.username==username, Users.phone_number==phone).count()
        if count2 == 0:
            return render_template("forgot_password.html", error_phone="手机号错误")
        # 密码加密
        s1 = sha1()
        s1.update(repr(new_password).encode('utf-8'))
        new_password = s1.hexdigest()
        old_password = db.session.query(Users.password).filter(Users.username==username).first()[0]
        if old_password == new_password:
            return render_template("forgot_password.html", error_pwd="新密码不能和原来密码一样")
        #修改密码
        u = db.session.query(Users).filter(Users.username==username).first()
        u.password = new_password
        db.session.add(u)
        db.session.commit()
        db.session.close()
        return redirect("/login")

@user.route("/sendcode")
def sendcode():
    phone = request.args["phone"]
    identify_code = main(phone)
    return json.dumps(identify_code)