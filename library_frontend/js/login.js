const app = new Vue({
    el: '#loginForm',
    data() {
        // 校验读者id是否存在
        const rules_rid = (rule, value, callback) => {
            if (this.state == 'login') {
                callback();
            }
            // 使用Axios进行校验
            axios.post(
                this.baseURL + "rid/check/",
                {
                    rid: value,
                }
            )
                .then((res) => {
                    if (res.data.code === 1) {
                        if (res.data.exists) {
                            callback(new Error("读者已存在！"));
                        } else {
                            callback();
                        }
                    } else {
                        // 请求失败
                        callback(new Error(res.data.msg));
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        }

        return {
            baseURL: "http://127.0.0.1:8000/",

            user_type_options: [
                {
                    value: '1',
                    label: '管理员'
                },
                {
                    value: '2',
                    label: '读者'
                }
            ],

            gender_options: [
                {
                    value: '男',
                    label: '男'
                },
                {
                    value: '女',
                    label: '女'
                }
            ],

            category_options: [
                {
                    value: '学生',
                    label: '学生',
                },
                {
                    value: '教师',
                    label: '教师',
                }
            ],

            user_type: '1', // 1管理员，2读者

            state: "login",
            info: "没有账号？注册一个",

            register_form: {
                user_id: "",
                password: "",
                passwordAgain: "",
                realName: "",
                gender: "",
                category: "",
                mobile: "",
                email: "",
            },

            rules: {
                user_id: [
                    { required: true, message: "用户不能为空", trigger: "blur" },
                    { pattern: /^[\d]*$/, message: "用户id必须是数字", trigger: "blur" },
                    { validator: rules_rid, trigger: "blur" },
                ],
            }
        }
    },
    methods: {
        switchState: function (formName) {
            // 重置表单的校验
            this.$refs[formName].resetFields();

            if (this.state == 'login') {
                this.state = 'signup';
                this.info = "已有账号？开始登录";

                this.register_form.user_id = "";
                this.register_form.password = "";
            }
            else {
                this.state = 'login';
                this.info = "没有账号？注册一个";

                this.register_form.user_id = "";
                this.register_form.password = "";
                this.register_form.passwordAgain = "";
                this.register_form.realName = "";
                this.register_form.gender = "";
                this.register_form.category = "";
                this.register_form.mobile = "";
                this.register_form.email = "";
            }
        },

        login: function () {
            if (this.register_form.user_id == "" || this.register_form.password == "") {
                alert("请将登录信息填写完整");
            } else {
                // 定义that
                let that = this;

                // 执行Axios请求
                if (this.user_type === '1') {
                    axios
                        .post(
                            that.baseURL + "login/admin/",
                            {
                                aid: that.register_form.user_id,
                                apsd: that.register_form.password
                            }
                        )
                        .then(res => {
                            // 执行成功
                            if (res.data.code === 1) {
                                //提示：
                                if (res.data.psd_correct) {
                                    that.$message({
                                        message: '管理员登录成功！',
                                        type: 'success'
                                    });
                                } else {
                                    alert(res.data.reason);
                                }
                            } else {
                                that.$message.error(res.data.msg);
                            }
                        })
                        .catch(err => {
                            // 执行失败
                            console.log(err);
                            that.$message.error("管理员登录时后端查询结果出现异常！");
                        });
                } else {
                    axios
                        .post(
                            that.baseURL + "login/reader/",
                            {
                                rid: that.register_form.user_id,
                                rpsd: that.register_form.password
                            }
                        )
                        .then(res => {
                            // 执行成功
                            if (res.data.code === 1) {
                                //提示：
                                if (res.data.psd_correct) {
                                    that.$message({
                                        message: '读者登录成功！',
                                        type: 'success'
                                    });
                                } else {
                                    alert(res.data.reason);
                                }
                            } else {
                                that.$message.error(res.data.msg);
                            }
                        })
                        .catch(err => {
                            // 执行失败
                            console.log(err);
                            that.$message.error("读者登录时后端查询结果出现异常！");
                        });
                }
            }
        },
        post_register_info() {
            // 定义that
            let that = this;
            // 暂存user_id和password，若注册成功，直接传给登录页面
            // 不能是浅拷贝
            let tmp_user_id = this.register_form.user_id;
            let tmp_password = this.register_form.password;
            // 执行Axios请求
            axios
                .post(
                    that.baseURL + "register/reader/",
                    {
                        rid: that.register_form.user_id,
                        rname: that.register_form.realName,
                        rsex: that.register_form.gender,
                        rtype: that.register_form.category,
                        rtel: that.register_form.mobile,
                        remail: that.register_form.email,
                        rpsd: that.register_form.password
                    }
                )
                .then(res => {
                    // 执行成功
                    if (res.data.code === 1) {
                        //提示：
                        that.$message({
                            message: '新用户注册成功！',
                            type: 'success'
                        });

                        // 跳转到登录页面
                        that.switchState('register_form');

                        that.register_form.user_id = tmp_user_id;
                        that.register_form.password = tmp_password;
                        that.user_type = "2";
                        

                    } else {
                        that.$message.error(res.data.msg);
                    }
                })
                .catch(err => {
                    // 执行失败
                    console.log(err);
                    that.$message.error("新用户注册时出现异常！");
                });
        },
        signup: function (formName) {
            this.register_form.mobile = this.register_form.mobile.replace(/\D/gi, "");
            if (this.register_form.user_id == "")
                alert("用户名不能为空");
            else if (this.register_form.password != this.register_form.passwordAgain)
                alert("两次密码不一致");
            else if (this.register_form.realName == "")
                alert("真实姓名不能为空");
            else if (this.register_form.gender == "")
                alert("性别不能为空");
            else if (this.register_form.category == "")
                alert("用户类别不能为空");
            else {
                // 校验user_id不重复
                this.$refs[formName].validate((valid, invalidFields) => {
                    if (valid) {
                        // 校验成功后，执行注册信息添加

                        this.post_register_info();

                        alert('submit!');
                    } else {
                        // var obj = {};
                        // for (obj in invalidFields) {
                        //     console.log(obj);
                        //     this.$refs[obj].focus();
                        // }
                        // this.$refs['user_id'].focus();

                        console.log('error submit!!');
                        return false;
                    }
                });


            }
        },
    },
});