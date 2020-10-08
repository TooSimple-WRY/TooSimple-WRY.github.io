<template>
  <!-- HTML结构：只能有一个跟标签 -->
  <div id="stocksDiv">
    <!-- 表单 -->
    <el-form :inline="true" style="margin-top: 20px;" @submit.native.prevent="query_stocks">
      <el-row>
        <el-col :span="12" style="text-align: left;">
          <el-form-item label="请输入查询条件">
            <el-input v-model="inputstr" placeholder="输入查询条件"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8" style="text-align: right; padding-right: 10px;">
          <el-button-group>
            <el-button type="primary" icon="el-icon-search" @click="query_stocks()">查询</el-button>
            <el-button type="primary" icon="el-icon-tickets" @click="get_all_stocks()">全部</el-button>
            <el-button
              v-if="user_type=='1'"
              type="primary"
              icon="el-icon-circle-plus-outline"
              @click="add_stock()"
            >添加</el-button>
          </el-button-group>
        </el-col>
        <el-col :span="2">
          <!-- <el-upload> -->
          <el-button v-if="user_type=='1'" type="primary">导入Excel</el-button>
          <!-- </el-upload> -->
        </el-col>
        <el-col :span="2">
          <el-button v-if="user_type=='1'" type="primary">导出Excel</el-button>
        </el-col>
      </el-row>
    </el-form>
    <!-- 表格 -->
    <el-table
      :data="page_stocks"
      border
      style="width: 100%"
      size="mini"
      @selection-change="handle_selection_change"
    >
      <el-table-column
        v-if="user_type=='1'"
        type="selection"
        :selectable="check_page_stocks_editable"
        align="center"
        min-width="5%"
      ></el-table-column>
      <el-table-column type="index" label="序号" align="center" min-width="5%"></el-table-column>
      <el-table-column prop="bbid" label="库存编号" align="center" min-width="12%"></el-table-column>
      <el-table-column prop="bid" label="图书编号" align="center" min-width="12%"></el-table-column>
      <el-table-column prop="bname" label="书名" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="place" label="书库" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="sheft" label="书架" align="center" min-width="13%"></el-table-column>
      <el-table-column prop="statu" label="借阅状态" align="center" min-width="10%"></el-table-column>
      <el-table-column label="操作" align="center" min-width="13%">
        <template slot-scope="scope">
          <el-button
            v-if="user_type=='1'"
            type="primary"
            icon="el-icon-edit"
            size="mini"
            circle
            @click="update_stock(scope.row)"
          ></el-button>
          <el-button
            v-if="user_type=='1'"
            type="danger"
            icon="el-icon-delete"
            size="mini"
            circle
            @click="delete_stock(scope.row)"
            :disabled="delete_btn_disabled(scope.$index) == false"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-row style="margin-top: 10px;">
      <el-col :span="8" style="text-align: left;">
        <el-button
          v-if="user_type=='1'"
          type="danger"
          icon="el-icon-delete"
          @click="delete_stocks()"
          size="mini"
        >批量删除</el-button>
      </el-col>
      <el-col :span="16" style="text-align: right;">
        <el-pagination
          @size-change="handle_size_change"
          @current-change="handle_current_change"
          :current-page="currentpage"
          :page-sizes="[5, 10, 50, 100]"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        ></el-pagination>
      </el-col>
    </el-row>
    <!-- 弹出框的库存信息表单 -->
    <el-dialog
      :title="dialog_title"
      :visible.sync="dialog_visible"
      width="700px"
      @close="close_dialog_form('stock_form')"
      :close-on-click-modal="false"
    >
      <el-form
        :model="stock_form"
        :rules="rules"
        ref="stock_form"
        style="margin-left: 10px; margin-right: 15px;"
        label-width="90px"
        label-position="right"
        size="mini"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item label="库存编号：" prop="bbid">
              <el-input v-model="stock_form.bbid" :disabled="is_edit" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="图书编号：" prop="bid">
              <el-input v-model="stock_form.bid" :disabled="is_edit" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="书名：">
              <el-input v-model="stock_form.bname" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="书库：">
              <el-input v-model="stock_form.place" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="书架：">
              <el-input v-model="stock_form.sheft" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="借阅状态：">
              <el-input v-model="stock_form.statu" suffix-icon="el-icon-edit" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="mini" @click="submit_stock_form('stock_form')">确 定</el-button>
        <el-button type="info" size="mini" @click="close_dialog_form('stock_form')">取 消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
// js部分 逻辑部分

import axios from "axios";

export default {
  // el: "#app",
  name: "stocksDiv",

  props: ["user_type", "user_id"], // 等价于data里面的user_type, user_id

  data() {
    // 校验库存编号是否存在
    const rules_bbid = (rule, value, callback) => {
      if (this.is_edit) {
        callback();
      }
      // 使用Axios进行校验
      axios
        .post(this.baseURL + "bbid/check/", {
          bbid: value
        })
        .then(res => {
          if (res.data.code === 1) {
            if (res.data.exists) {
              callback(new Error("编号已存在！"));
            } else {
              callback();
            }
          } else {
            // 请求失败
            // callback(new Error("校验图书编号后端出现异常！"))
            callback(new Error(res.data.msg));
          }
        })
        .catch(err => {
          console.log(err);
        });
    };

    // 校验图书编号是否不存在
    const rules_bid = (rule, value, callback) => {
      if (this.is_edit) {
        callback();
      }
      let that = this;
      // 使用Axios进行校验
      axios
        .post(this.baseURL + "bid/check/", {
          bid: value
        })
        .then(res => {
          if (res.data.code === 1) {
            if (res.data.exists === false) {
              callback(new Error("该图书不存在！"));
            } else {
              that.stock_form.bname = res.data.bname; // 把查询到的书名更新到表单上

              callback();
            }
          } else {
            // 请求失败
            // callback(new Error("校验图书编号后端出现异常！"))
            callback(new Error(res.data.msg));
          }
        })
        .catch(err => {
          console.log(err);
        });
    };

    return {
      // msg: "Hello, Vue!",
      // 从login页面传过来的user_type, user_id
      login_user_type: "",
      login_user_id: "",

      stocks: [], //所有的图书信息
      page_stocks: [], //分页后当前页的图书
      page_stocks_editable: [],
      baseURL: "http://127.0.0.1:8000/",
      inputstr: "", //输入查询条件
      selected_stocks: [], // 选择复选框时的记录

      //分页相关的变量
      total: 0, //数据总行数
      currentpage: 1, //当前所在的页
      pagesize: 10, //每页显示多少行
      // 弹出框表单
      dialog_visible: false,
      dialog_title: "", // 弹出框的标题
      is_edit: false, // 标识是否是修改
      stock_form: {
        bbid: "",
        bid: "",
        bname: "",
        place: "",
        sheft: "",
        statu: ""
      },
      rules: {
        bbid: [
          { required: true, message: "编号不能为空", trigger: "blur" },
          { pattern: /^[\d]*$/, message: "编号必须是数字", trigger: "blur" },
          { validator: rules_bbid, trigger: "blur" }
        ],
        bid: [
          { required: true, message: "编号不能为空", trigger: "blur" },
          { pattern: /^[\d]*$/, message: "编号必须是数字", trigger: "blur" },
          { validator: rules_bid, trigger: "blur" }
        ]
      }
    };
  },
  mounted() {
    //自动加载数据
    this.get_stocks();
  },
  methods: {
    //获取所有图书信息
    get_stocks: function() {
      //记录this的地址
      let that = this; //axios会把this赋值为undefined
      //使用Axios实现Ajax请求
      axios
        .get(this.baseURL + "all_stocks/")
        .then(function(res) {
          //请求成功后执行的函数
          // console.log(res);
          if (res.data.code === 1) {
            //把数据给stocks
            that.stocks = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_stocks();
            //提示：
            that.$message({
              message: "数据加载成功！",
              type: "success"
            });

            // console.log("PPPPPPPPPPPPPP");
            // console.log(that.stocks);
          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(function(err) {
          //请求失败后执行的函数
          console.log(err);
        });
    },
    get_all_stocks() {
      // 清空输入的inputstr
      this.inputstr = "";
      // 获取所有的数据
      this.get_stocks();
    },
    check_page_stocks_editable(row, index) {
      return this.page_stocks_editable[index];
    },
    delete_btn_disabled(index) {
      // console.log("btn_disabled: index = " + index);
      return this.page_stocks_editable[index];
    },
    // 获取当前页的学生数据
    get_page_stocks: function() {
      // 清空page_stocks中的数据
      this.page_stocks = [];
      this.page_stocks_editable = [];
      // 获得当前页的数据
      for (
        let i = (this.currentpage - 1) * this.pagesize;
        i < this.total;
        i++
      ) {
        this.page_stocks.push(this.stocks[i]);

        // 借阅中的库存不可被管理员操作
        if (this.stocks[i].statu == "借阅中") {
          this.page_stocks_editable.push(false);
        } else {
          this.page_stocks_editable.push(true);
        }

        // 判断是否达到一页的要求
        if (this.page_stocks.length === this.pagesize) break;
      }
    },
    // 实现图书信息查询
    query_stocks() {
      // 使用Ajax请求--POST-->传递inputstr
      let that = this;
      // 开始Ajax请求
      axios
        .post(that.baseURL + "stocks/query/", {
          inputstr: that.inputstr
        })
        .then(function(res) {
          if (res.data.code === 1) {
            //把数据给stocks
            that.stocks = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_stocks();
            //提示：
            that.$message({
              message: "查询数据加载成功！",
              type: "success"
            });
          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(function(err) {
          console.log(err);
          that.$message.error("获取后端查询结果出现异常！");
        });
    },
    // 添加图书打开表单
    add_stock() {
      // 修改标题
      this.dialog_title = "添加库存";

      this.stock_form.statu = "可借";

      // 弹出表单
      this.dialog_visible = true;
    },
    // 修改图书详情
    update_stock(row) {
      // 修改标题
      this.dialog_title = "修改库存信息";
      // 修改is_edit变量
      this.is_edit = true;
      // 弹出表单
      this.dialog_visible = true;
      //this.stock_form = row; //浅拷贝
      // 深拷贝方法2
      this.stock_form = JSON.parse(JSON.stringify(row));
    },
    // 提交图书的表单（添加/修改）
    submit_stock_form(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 校验成功后，执行添加或修改
          if (this.is_edit) {
            // 修改
            this.submit_update_stock();
          } else {
            // 添加
            this.submit_add_stock();
          }

          alert("submit!");
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 添加到数据库的函数
    submit_add_stock() {
      let submit_form = {
        bbid: this.stock_form.bbid,
        bid: this.stock_form.bid,
        place: this.stock_form.place,
        sheft: this.stock_form.sheft,
        statu: this.stock_form.statu
      };

      // 定义that
      let that = this;
      // 执行Axios请求
      axios
        .post(that.baseURL + "stocks/add/", submit_form)
        .then(res => {
          // 执行成功
          if (res.data.code === 1) {
            //把数据给stocks
            that.stocks = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_stocks();
            //提示：
            that.$message({
              message: "数据添加成功！",
              type: "success"
            });
            // 关闭窗体
            that.close_dialog_form("stock_form");
          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(err => {
          // 执行失败
          console.log(err);
          that.$message.error("添加时获取后端查询结果出现异常！");
        });
    },
    // 修改更新到数据库
    submit_update_stock() {
      let submit_form = {
        bbid: this.stock_form.bbid,
        bid: this.stock_form.bid,
        place: this.stock_form.place,
        sheft: this.stock_form.sheft,
        statu: this.stock_form.statu
      };
      // 定义that
      let that = this;
      // 执行Axios请求
      axios
        .post(that.baseURL + "stocks/update/", submit_form)
        .then(res => {
          // 执行成功
          if (res.data.code === 1) {
            //把数据给stocks
            that.stocks = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_stocks();
            //提示：
            that.$message({
              message: "数据修改成功！",
              type: "success"
            });
            // 关闭窗体
            that.close_dialog_form("stock_form");
          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(err => {
          // 执行失败
          console.log(err);
          that.$message.error("修改时获取后端查询结果出现异常！");
        });
    },
    // 删除一条图书信息
    delete_stock(row) {
      // 等待确认
      this.$confirm(
        "是否确认删除库存信息【编号：" + row.bbid + "】？",
        "是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      )
        .then(() => {
          // 确认删除响应事件
          let that = this;
          // 调用后端接口
          axios
            .post(that.baseURL + "stocks/delete/", { bbid: row.bbid })
            .then(res => {
              if (res.data.code === 1) {
                //把数据给stocks
                that.stocks = res.data.data;
                // 获取返回记录的总行数
                that.total = res.data.data.length;
                // 获取当前页的数据
                that.get_page_stocks();
                //提示：
                that.$message({
                  message: "数据删除成功！",
                  type: "success"
                });
              } else {
                that.$message.error(res.data.msg);
              }
            })
            .catch(err => {
              // 执行失败
              console.log(err);
              that.$message.error("删除时获取后端查询结果出现异常！");
            });

          this.$message({
            type: "success",
            message: "删除成功!"
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    delete_stocks() {
      // 等待确认
      this.$confirm(
        "是否确认批量删除" + this.selected_stocks.length + "条库存信息？",
        "是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      )
        .then(() => {
          // 确认删除响应事件
          let that = this;
          // 调用后端接口
          axios
            .post(that.baseURL + "stocks/batch_delete/", {
              batch_data: that.selected_stocks
            })
            .then(res => {
              if (res.data.code === 1) {
                //把数据给stocks
                that.stocks = res.data.data;
                // 获取返回记录的总行数
                that.total = res.data.data.length;
                // 获取当前页的数据
                that.get_page_stocks();
                //提示：
                that.$message({
                  message: "数据批量删除成功！",
                  type: "success"
                });
              } else {
                that.$message.error(res.data.msg);
              }
            })
            .catch(err => {
              // 执行失败
              console.log(err);
              that.$message.error("删除时获取后端查询结果出现异常！");
            });

          this.$message({
            type: "success",
            message: "删除成功!"
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    // 关闭弹出框的表单
    close_dialog_form(formName) {
      // 重置表单的校验
      this.$refs[formName].resetFields();
      // 清空
      this.stock_form.bbid = "";
      this.stock_form.bid = "";
      this.stock_form.bname = "";
      this.stock_form.sheft = "";
      this.stock_form.place = "";
      this.stock_form.statu = "";

      // 关闭
      this.dialog_visible = false;
      // 初始化is_edit的值
      this.is_edit = false;
    },
    // 分页时修改每页的行数
    handle_size_change(size) {
      // 修改当前每页数据行数
      this.pagesize = size;
      // 数据重新分页
      this.get_page_stocks();
    },
    // 调整当前的页码
    handle_current_change(page_number) {
      // 修改当前的页码
      this.currentpage = page_number;
      // 数据重新分页
      this.get_page_stocks();
    },
    // 选择复选框时触发的操作
    handle_selection_change(data) {
      this.selected_stocks = data;
      // console.log(data);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>
/* 注意：这里不加scoped, home.css的样式会污染全局，但加上之后el-upload的样式会默认是element-ui的自带样式，故先不加 */
#stocksDiv {
  margin: 0px;
  padding: 0px;
  height: 100%;
}
</style>