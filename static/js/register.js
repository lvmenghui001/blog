$(function() {
    var error_name = false;
    var error_pwd = false;
    var error_cpwd = false;
    var error_phone = false;
    var phone_registered = false;
    var error_student_number = false;
    var username_registered = false;
    var student_number_registered = false;
    var student_number_exist = false;
    $('#user_name').blur(function () {
        check_user_name();
    });

    $('#pwd').blur(function () {
        check_pwd();
    });

    $('#cpwd').blur(function () {
        check_cpwd();
    });

    $('#phone').blur(function () {
        check_phone();
    });

    $('#student_number').blur(function(){
        check_student_number();
    });

    //判断用户名格式是否正确
    function check_user_name() {
        var len = $('#user_name').val().length;
        if (len < 5 || len > 20) {
            $('#user_name').next().html('请输入5-20个字符的用户名');
            $('#user_name').next().show();
            error_name = true;
        } else {
            $('#user_name').next().hide();
            error_name = false;
        }
    }

    //判断密码格式
    function check_pwd() {
        var len = $('#pwd').val().length;
        if (len < 8 || len > 20) {
            $('#pwd').next().html('密码最少8位，最长20位');
            $('#pwd').next().show();
            error_pwd = true;
        } else {
            $('#pwd').next().hide();
            error_pwd = false;
        }
    }

    //判断两次密码是否一致
    function check_cpwd() {
        var pass = $('#pwd').val();
        var cpass = $('#cpwd').val();
        if (cpass.length < 1) {
            $('#cpwd').next().html('请再次输入密码');
            $('#cpwd').next().show();
            error_cpwd = true;
        } else {
            if (pass != cpass) {
                $('#cpwd').next().html('两次输入的密码不一致');
                $('#cpwd').next().show();
                error_cpwd = true;
            } else {
                $('#cpwd').next().hide();
                error_cpwd = false;
            }
        }
    }

    //判断手机号格式
    function check_phone() {
        var reg_phone = /(^1[3|4|5|7|8]\d{9}$)|(^09\d{8}$)/;
        if (reg_phone.test($('#phone').val())) {
            $('#phone').next().hide();
            error_phone = false;
        } else {
            $('#phone').next().html('手机号格式不正确');
            $('#phone').next().show();
            error_phone = true;
        }
    }

    //判断手机号是否已注册
    function check_phone_registered() {
        var phone = $('#phone').val();
        data = {"phone": phone};
        $.get("/phone_registered",data,function(data){
            if (data != 0) {
                $('#phone').next().html('此手机号已被注册');
                $('#phone').next().show();
                phone_registered = true;
            }else{
                $('#phone').next().hide();
                phone_registered = false;
            }
        }, "json");
    }

    //判断学号或教工号格式（12位数字）
    function check_student_number(){
        var reg_student_number = /(^[0-9]{12}$)/;
        //var reg_student_number = /(^1[3|4|5|7|8]\d{9}$)|(^09\d{8}$)/;
        if (reg_student_number.test($('#student_number').val())) {
            $('#student_number').next().hide();
            error_student_number = false;
        } else {
            $('#student_number').next().html('学号或教工号格式不正确');
            $('#student_number').next().show();
            error_student_number = true;
        }
    }

    //判断用户名是否已注册
    function check_username_registered() {
        var name = $('#user_name').val();
        data = {"name": name};
        $.get("/username_registered",data,function(data) {
            if (data != 0) {
                $('#user_name').next().html('此用户名已被注册');
                $('#user_name').next().show();
                username_registered = true;
            }else{
                $('#user_name').next().hide();
                username_registered = false;
            }
        }, "json");
    }

    //判断学号或教工号是否已注册
    function check_student_number_registered() {
        var student_number = $('#student_number').val();
        data = {"student_number": student_number};
        $.get("/student_number_registered",data,function(data) {
            if (data != 0) {
                $('#student_number').next().html('此学号或教工号已被注册');
                $('#student_number').next().show();
                student_number_registered = true;
            } else {
                $('#student_number').next().hide();
                student_number_registered = false;
            }
        }, "json");
    }

    //判断学号或教工号是否存在
    function check_student_number_exist() {
        var student_number = $('#student_number').val();
        data = {"student_number": student_number};
        $.get("/student_number_exist", data, function (data) {
            if (data == 0) {
                $('#student_number').next().html('此学号或教工号不存在');
                $('#student_number').next().show();
                student_number_exist = false;
            } else {
               $('#student_number').next().hide();
                student_number_exist = true;
            }
        }, "json");
    }

    $('#reg_form').submit(function () {
        check_user_name();
        check_pwd();
        check_cpwd();
        check_phone();
        check_phone_registered();
        check_student_number();
        check_username_registered();
        check_student_number_registered();
        if(student_number_registered==false){
            check_student_number_exist();
        }
        if (error_name == false && error_pwd == false && error_cpwd == false && error_phone == false && phone_registered == false &&username_registered == false && student_number_registered == false && student_number_exist == true && phone_registered == false){
            var code_indetify = $("#code_identify").val();
            if (code_indetify.length < 1) {
                $("#code_identify").next().next().html("请输入验证码");
                $("#code_identify").next().next().show();
                return false;
            } else if($("#code").val() != code_indetify) {
                alert(333)
                $("#code_identify").next().next().html("验证码错误");
                $("#code_identify").next().next().show();
                return false;
            } else {
                return true;
            }
        } else {
            return false;
        }
    });
});