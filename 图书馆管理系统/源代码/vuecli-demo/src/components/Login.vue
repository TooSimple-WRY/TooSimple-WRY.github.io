<template>
  <!-- HTML结构：只能有一个跟标签 -->
  <div class="wrapper">
    <div id="loginForm" class="login">
      <p class="title" v-if="state=='login'">
        <el-select v-model="user_type" style="margin-left: 10px; margin-top: 15px;">
          <el-option
            v-for="item in user_type_options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
        <el-link style="color:#999; font-size:20px; margin-left: 10px; ">登 录</el-link>
      </p>
      <p class="title" v-else>
        <el-link style="color:#999; font-size:20px; margin-left: 10px; margin-top: 15px;">新用户注册</el-link>
      </p>

      <el-form :model="register_form" :rules="rules" ref="register_form">
        <el-form-item prop="user_id">
          <el-link style="color:#999; font-size:18px; margin-left: 10px; margin-right: 20px;">用户:</el-link>
          <el-input v-model="register_form.user_id" style="width: 220px;"></el-input>
        </el-form-item>

        <el-form-item>
          <a style="color:#999; font-size:18px; margin-left: 10px; margin-right: 20px;">密码:</a>
          <el-input v-model="register_form.password" type="password" style="width:220px;"></el-input>
        </el-form-item>

        <el-form-item v-if="state=='signup'">
          <a style="color:#999; font-size:18px; margin-left: 10px; margin-right: 20px;">确认密码:</a>
          <el-input v-model="register_form.passwordAgain" type="password" style="width:183px;"></el-input>
        </el-form-item>

        <el-form-item v-if="state=='signup'">
          <a style="color:#999; font-size:18px; margin-left: 10px; margin-right: 20px;">真实姓名:</a>
          <el-input v-model="register_form.realName" style="width:183px;"></el-input>
        </el-form-item>

        <el-form-item v-if="state=='signup'">
          <a style="color:#999; font-size:18px; margin-left: 10px; margin-right: 20px;">性别:</a>
          <el-select v-model="register_form.gender">
            <el-option
              v-for="item in gender_options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item v-if="state=='signup'">
          <a style="color:#999; font-size:18px; margin-left: 10px; margin-right: 20px;">用户类别:</a>
          <el-select v-model="register_form.category" style="width:183px;">
            <el-option
              v-for="item in category_options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item v-if="state=='signup'">
          <a style="color:#999; font-size:18px; margin-left: 10px; margin-right: 20px;">手机号:</a>
          <el-input v-model="register_form.mobile" style="width: 200px;"></el-input>
        </el-form-item>

        <el-form-item v-if="state=='signup'">
          <a style="color:#999; font-size:18px; margin-left: 10px; margin-right: 20px;">邮箱:</a>
          <el-input v-model="register_form.email" style="width: 220px;"></el-input>
        </el-form-item>

        <el-form-item>
          <el-link
            type="primary"
            style="float: right; font-size: 14px;"
            @click="switchState('register_form')"
          >{{ info }}</el-link>
        </el-form-item>

        <el-form-item v-if="state=='login'" style="text-align: center;">
          <el-button
            type="primary"
            @click="login()"
            style="width: 100%; height: 100%; font-size:16px;"
            plain
          >登 录</el-button>
        </el-form-item>

        <el-form-item v-else>
          <el-button
            type="primary"
            @click="signup('register_form') "
            style="width: 100%; height: 100%; font-size:16px;"
            plain
          >注 册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
// js部分 逻辑部分
import axios from "axios";

// import VueRouter from 'vue-router'
// Vue.use(VueRouter)

import Vue from "vue";
import VueCookies from "vue-cookies";
Vue.use(VueCookies);

export default {
  name: "loginForm",
  data() {
    // 校验读者id是否存在
    const rules_rid = (rule, value, callback) => {
      if (this.state == "login") {
        callback();
      }
      // 使用Axios进行校验
      axios
        .post(this.baseURL + "rid/check/", {
          rid: value
        })
        .then(res => {
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
        .catch(err => {
          console.log(err);
        });
    };

    return {
      baseURL: "http://127.0.0.1:8000/",

      user_type_options: [
        {
          value: "1",
          label: "管理员"
        },
        {
          value: "2",
          label: "读者"
        }
      ],

      gender_options: [
        {
          value: "男",
          label: "男"
        },
        {
          value: "女",
          label: "女"
        }
      ],

      category_options: [
        {
          value: "学生",
          label: "学生"
        },
        {
          value: "教师",
          label: "教师"
        }
      ],

      user_type: "1", // 1管理员，2读者

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
        email: ""
      },

      rules: {
        user_id: [
          { required: true, message: "用户不能为空", trigger: "blur" },
          { pattern: /^[\d]*$/, message: "用户id必须是数字", trigger: "blur" },
          { validator: rules_rid, trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    switchState: function(formName) {
      // 重置表单的校验
      this.$refs[formName].resetFields();

      if (this.state == "login") {
        this.state = "signup";
        this.info = "已有账号？开始登录";

        this.register_form.user_id = "";
        this.register_form.password = "";
      } else {
        this.state = "login";
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

    login: function() {
      if (
        this.register_form.user_id == "" ||
        this.register_form.password == ""
      ) {
        alert("请将登录信息填写完整");
      } else {
        // 定义that
        let that = this;

        // 执行Axios请求
        if (this.user_type === "1") {
          axios
            .post(that.baseURL + "login/admin/", {
              aid: that.register_form.user_id,
              apsd: that.register_form.password
            })
            .then(res => {
              // 执行成功
              if (res.data.code === 1) {
                //提示：
                if (res.data.psd_correct) {
                  that.$message({
                    message: "管理员登录成功！",
                    type: "success"
                  });

                  that.$cookies.set("status", "logined", 60 * 60 * 1); // 1h
                  that.$cookies.set("user_type", that.user_type, 60 * 60 * 1);
                  that.$cookies.set(
                    "user_id",
                    that.register_form.user_id,
                    60 * 60 * 1
                  );
                  // let user_info = that.user_type + " | " + that.user_id + " | " + that.password;
                  // that.$cookies.set("user_info", user_info, 60 * 60 * 1);  // 1h

                  // 页面跳转，传值
                  that.$router.push({
                    name: "library",
                    params: {
                      user_type: that.user_type,
                      user_id: that.register_form.user_id
                    }
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
            .post(that.baseURL + "login/reader/", {
              rid: that.register_form.user_id,
              rpsd: that.register_form.password
            })
            .then(res => {
              // 执行成功
              if (res.data.code === 1) {
                //提示：
                if (res.data.psd_correct) {
                  that.$message({
                    message: "读者登录成功！",
                    type: "success"
                  });

                  that.$cookies.set("status", "logined", 60 * 60 * 1); // 1h
                  that.$cookies.set("user_type", that.user_type, 60 * 60 * 1);
                  that.$cookies.set(
                    "user_id",
                    that.register_form.user_id,
                    60 * 60 * 1
                  );
                  // let user_info = that.user_type + " | " + that.user_id + " | " + that.password;
                  // that.$cookies.set("user_info", user_info, 60 * 60 * 1);  // 1h

                  // 页面跳转，传值
                  that.$router.push({
                    name: "library",
                    params: {
                      user_type: that.user_type,
                      user_id: that.register_form.user_id
                    }
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
        .post(that.baseURL + "register/reader/", {
          rid: that.register_form.user_id,
          rname: that.register_form.realName,
          rsex: that.register_form.gender,
          rtype: that.register_form.category,
          rtel: that.register_form.mobile,
          remail: that.register_form.email,
          rpsd: that.register_form.password
        })
        .then(res => {
          // 执行成功
          if (res.data.code === 1) {
            //提示：
            that.$message({
              message: "新用户注册成功！",
              type: "success"
            });

            // 跳转到登录页面
            that.switchState("register_form");

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
    signup: function(formName) {
      this.register_form.mobile = this.register_form.mobile.replace(/\D/gi, "");
      if (this.register_form.user_id == "") alert("用户名不能为空");
      else if (this.register_form.password != this.register_form.passwordAgain)
        alert("两次密码不一致");
      else if (this.register_form.realName == "") alert("真实姓名不能为空");
      else if (this.register_form.gender == "") alert("性别不能为空");
      else if (this.register_form.category == "") alert("用户类别不能为空");
      else {
        // 校验user_id不重复
        this.$refs[formName].validate((valid, invalidFields) => {
          if (valid) {
            // 校验成功后，执行注册信息添加

            this.post_register_info();

            alert("submit!");
          } else {
            // var obj = {};
            // for (obj in invalidFields) {
            //     console.log(obj);
            //     this.$refs[obj].focus();
            // }
            // this.$refs['user_id'].focus();

            console.log("error submit!!");
            return false;
          }
        });
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style src="../assets/css/login.css" scoped>
/* @import "../assets/css/login.css"; */
</style>
