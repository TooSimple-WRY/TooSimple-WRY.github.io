<template>
  <!-- HTML结构：只能有一个跟标签 -->
  <div id="libraryPage">
    <el-container>
      <el-header style="height: 70px;">
        图书馆书籍管理系统
        <div style="float: right; width: 100px; height: 100%; text-align: center;">
          <el-popover placement="bottom" trigger="hover">
            <p style="text-align: center;" v-if="user_type=='1'">管理员</p>
            <p style="text-align: center;" v-else>读者</p>
            <p style="text-align: center;">{{ user_name }}</p>
            <p style="text-align: center;" @click="popupDialog()">修改密码</p>
            <el-divider></el-divider>
            <p style="text-align: center;" @click="logout()">退出</p>

            <el-button
              slot="reference"
              icon="el-icon-user"
              @click=";"
              style="width:50px; height: 50px; display: inline-block; vertical-align: middle;"
              circle
            ></el-button>
          </el-popover>
        </div>
      </el-header>
      <el-container>
        <el-aside width="180px">
          <el-menu
            v-if="user_type=='1'"
            :router="true"
            default-active="$route.name"
            class="el-menu-vertical-demo"
          >
            <el-menu-item index="books">
              <i class="el-icon-reading"></i>
              <span slot="title">{{ breadsName["books"] }}</span>
            </el-menu-item>
            <el-menu-item index="stocks">
              <i class="el-icon-document"></i>
              <span slot="title">{{ breadsName["stocks"] }}</span>
            </el-menu-item>
            <el-menu-item index="borrowing">
              <i class="el-icon-info"></i>
              <span slot="title">{{ breadsName["borrowing"] }}</span>
            </el-menu-item>
            <el-menu-item index="readerinfo">
              <i class="el-icon-user"></i>
              <span slot="title">{{ breadsName["readerinfo"] }}</span>
            </el-menu-item>
          </el-menu>

          <el-menu v-else :router="true" default-active="$route.name" class="el-menu-vertical-demo">
            <el-menu-item index="books">
              <i class="el-icon-reading"></i>
              <span slot="title">{{ readerBreadsName["books"] }}</span>
            </el-menu-item>
            <el-menu-item index="borrowing">
              <i class="el-icon-info"></i>
              <span slot="title">{{ readerBreadsName["borrowing"] }}</span>
            </el-menu-item>
            <el-menu-item index="readerinfo">
              <i class="el-icon-user"></i>
              <span slot="title">{{ readerBreadsName["readerinfo"] }}</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <el-main>
            <!-- 面包屑导航 -->
            <el-breadcrumb v-if="user_type=='1'" separator-class="el-icon-arrow-right">
              <el-breadcrumb-item :to="{ path: '/library/welcome' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ breadsName[$route.name] }}</el-breadcrumb-item>
            </el-breadcrumb>
            <el-breadcrumb v-else separator-class="el-icon-arrow-right">
              <el-breadcrumb-item :to="{ path: '/library/welcome' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ readerBreadsName[$route.name] }}</el-breadcrumb-item>
            </el-breadcrumb>

            <router-view :user_type="user_type" :user_id="user_id" />
          </el-main>
          <el-footer style="height: 30px;">图书馆书籍管理系统 版权所有：zyx, wry | 2020</el-footer>
        </el-container>
      </el-container>
    </el-container>

    <!-- 弹出框修改密码表单 -->
    <el-dialog
      title="修改密码"
      :visible.sync="dialog_visible"
      width="400px"
      @close=";"
      :close-on-click-modal="false"
    >
      <el-form
        :model="pwd_form"
        :rules="rules"
        ref="pwd_form"
        style="margin-left: 10px; margin-right: 15px;"
        label-width="150px"
        label-position="right"
        size="mini"
      >
        <el-row>
          <el-col :span="24">
            <el-form-item label="原始密码：" prop="password">
              <el-input type="password" v-model="pwd_form.password" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="新密码：" prop="new_password">
              <el-input type="password" v-model="pwd_form.new_password" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="再次输入新密码：" prop="new_password_again">
              <el-input
                type="password"
                v-model="pwd_form.new_password_again"
                suffix-icon="el-icon-edit"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="mini" @click="submit_pwd_form('pwd_form')">确 定</el-button>
        <el-button type="info" size="mini" @click="close_pwd_form('pwd_form')">取 消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
// js部分 逻辑部分
import axios from "axios";

export default {
  // el: "#app",
  name: "libraryPage",
  data() {
    const rules_original_pwd = (rule, value, callback) => {
      if (this.check_original_pwd) {
        if (this.user_type === "1") {
          let that = this;
          // 使用Axios进行校验
          axios
            .post(this.baseURL + "login/admin/", {
              aid: that.user_id,
              apsd: value
            })
            .then(res => {
              if (res.data.code === 1) {
                if (res.data.psd_correct) {
                  callback();
                } else {
                  callback(new Error(res.data.reason));
                }
              } else {
                // 请求失败
                callback(new Error(res.data.msg));
              }
            })
            .catch(err => {
              console.log(err);
            });
        } else {
          let that = this;
          // 使用Axios进行校验
          axios
            .post(this.baseURL + "login/reader/", {
              rid: that.user_id,
              rpsd: value
            })
            .then(res => {
              if (res.data.code === 1) {
                if (res.data.psd_correct) {
                  callback();
                } else {
                  callback(new Error(res.data.reason));
                }
              } else {
                // 请求失败
                callback(new Error(res.data.msg));
              }
            })
            .catch(err => {
              console.log(err);
            });
        }
      } else {
        callback();
      }
    };

    const rules_pwd_again = (rule, value, callback) => {
      if (value == this.pwd_form.new_password) {
        callback();
      } else {
        callback(new Error("两次输入的密码不一致！"));
      }
    };

    return {
      // msg: "Hello, Vue!",
      // 从login页面传过来的user_type, user_id
      baseURL: "http://127.0.0.1:8000/",

      user_type: "",
      user_id: "",
      user_name: "",
      dialog_visible: false,

      breadsName: {
        books: "书籍管理",
        stocks: "库存管理",
        borrowing: "借阅信息",
        readerinfo: "读者信息"
      },
      readerBreadsName: {
        books: "图书查阅",
        borrowing: "我的借阅",
        readerinfo: "我的信息"
      },

      check_original_pwd: false,

      pwd_form: {
        password: "",
        new_password: "",
        new_password_again: ""
      },

      rules: {
        password: [
          { required: true, message: "密码不能为空", trigger: "blur" },
          { validator: rules_original_pwd, trigger: "blur" } // 只有最后提交时才被触发
        ],
        new_password: [
          { required: true, message: "新密码不能为空", trigger: "blur" }
        ],
        new_password_again: [
          { required: true, message: "新密码不能为空", trigger: "blur" },
          { validator: rules_pwd_again, trigger: "blur" }
        ]
      }
    };
  },

  // mounted() {
  beforeMount(){
    if (this.$route.params.user_type && this.$route.params.user_id) {
      console.log(this.$route.params);
      this.user_type = this.$route.params.user_type;
      this.user_id = this.$route.params.user_id;

      this.query_user_name();

      this.$router.push({
        path: "/library/welcome"
        // params: {
        //   user_type: that.user_type,
        //   user_id: that.register_form.user_id
        // }
      });
    } else {
      // console.log("页面刷新");

      const status = this.$router.app.$cookies.get("status");
      // console.log("cookie: status = " + status);
      if (status) {
        // 表示当前页面只是单纯的刷新，user_type, user_id需要重新获取
        this.user_type = this.$router.app.$cookies.get("user_type");
        this.user_id = this.$router.app.$cookies.get("user_id");

        // console.log("cookie: user_id = " + this.user_id);
        // console.log("cookie: user_type = " + this.user_type);

        this.query_user_name();
      }
    }
  },
  methods: {
    query_user_name() {
      // 定义that
      let that = this;

      // 执行Axios请求
      if (this.user_type === "1") {
        axios
          .post(that.baseURL + "username/admin/", {
            aid: that.user_id
          })
          .then(res => {
            // 执行成功
            if (res.data.code === 1) {
              //提示：
              that.user_name = res.data.user_name;
            } else {
              that.$message.error(res.data.msg);
            }
          })
          .catch(err => {
            // 执行失败
            console.log(err);
            that.$message.error("管理员登录后查询姓名出现异常！");
          });
      } else {
        axios
          .post(that.baseURL + "username/reader/", {
            rid: that.user_id
          })
          .then(res => {
            // 执行成功
            if (res.data.code === 1) {
              //提示：
              that.user_name = res.data.user_name;
            } else {
              that.$message.error(res.data.msg);
            }
          })
          .catch(err => {
            // 执行失败
            console.log(err);
            that.$message.error("读者登录后查询姓名出现异常！");
          });
      }
    },
    popupDialog() {
      this.dialog_visible = true;
    },

    submit_pwd_form(formName) {
      this.check_original_pwd = true; // 开始原始密码的校验

      this.$refs[formName].validate(valid => {
        if (valid) {
          // 校验成功后
          this.check_original_pwd = false;
          this.submit_update_pwd();
        }
      });
    },

    submit_update_pwd() {
      if (this.user_type === "1") {
        // 定义that
        let that = this;
        // 执行Axios请求
        axios
          .post(that.baseURL + "password/update/admin/", {
            aid: that.user_id,
            apsd: that.pwd_form.new_password
          })
          .then(res => {
            // 执行成功
            if (res.data.code === 1) {
              //提示：
              that.$message({
                message: "密码修改成功！",
                type: "success"
              });
              // 关闭窗体
              that.close_pwd_form("pwd_form");

              // 跳转到登录页
              that.logout();
            } else {
              that.$message.error(res.data.msg);
            }
          })
          .catch(err => {
            // 执行失败
            console.log(err);
            that.$message.error("修改时获取后端查询结果出现异常！");
          });
      } else {
        // 定义that
        let that = this;
        // 执行Axios请求
        axios
          .post(that.baseURL + "password/update/reader/", {
            rid: that.user_id,
            rpsd: that.pwd_form.new_password
          })
          .then(res => {
            // 执行成功
            if (res.data.code === 1) {
              //提示：
              that.$message({
                message: "密码修改成功！",
                type: "success"
              });
              // 关闭窗体
              that.close_pwd_form("pwd_form");

              // 跳转到登录页
              that.logout();
            } else {
              that.$message.error(res.data.msg);
            }
          })
          .catch(err => {
            // 执行失败
            console.log(err);
            that.$message.error("修改时获取后端查询结果出现异常！");
          });
      }
    },

    close_pwd_form(formName) {
      // 重置表单的校验
      this.$refs[formName].resetFields();
      // 清空
      this.pwd_form.password = "";
      this.pwd_form.new_password = "";
      this.pwd_form.new_password_again = "";

      // 关闭
      this.dialog_visible = false;
    },

    logout() {
      this.$cookies.remove("status");
      this.$cookies.remove("user_type");
      this.$cookies.remove("user_id");

      // 页面跳转，传值
      this.$router.push({
        name: "login"
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style src="../assets/css/library.css">
/* 注意：这里不加scoped, library.css的样式会污染全局，但加上之后el-upload的样式会默认是element-ui的自带样式，故先不加 */
</style>
