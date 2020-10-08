<template>
  <!-- HTML结构：只能有一个跟标签 -->
  <div id="booksDiv">
    <!-- 表单 -->
    <el-form :inline="true" style="margin-top: 20px;" @submit.native.prevent="query_books">
      <el-row>
        <el-col :span="12" style="text-align: left;">
          <el-form-item label="请输入查询条件">
            <el-input v-model="inputstr" placeholder="输入查询条件"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8" style="text-align: right; padding-right: 10px;">
          <el-button-group>
            <el-button type="primary" icon="el-icon-search" @click="query_books()">查询</el-button>
            <el-button type="primary" icon="el-icon-tickets" @click="get_all_books()">全部</el-button>
            <el-button
              v-if="user_type=='1'"
              type="primary"
              icon="el-icon-circle-plus-outline"
              @click="add_book()"
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
      :data="page_books"
      border
      style="width: 100%"
      size="mini"
      @selection-change="handle_selection_change"
    >
      <el-table-column v-if="user_type=='1'" type="selection" align="center" min-width="5%"></el-table-column>
      <el-table-column type="index" label="序号" align="center" min-width="5%"></el-table-column>
      <el-table-column prop="bid" label="编号" align="center" min-width="12%"></el-table-column>
      <el-table-column prop="bname" label="书名" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="bauthor" label="作者" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="bcompany" label="出版社" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="btime" label="出版日期" align="center" min-width="10%"></el-table-column>
      <el-table-column prop="bsort" label="分类" align="center" min-width="10%"></el-table-column>
      <el-table-column label="操作" align="center" min-width="13%">
        <template slot-scope="scope">
          <el-button
            type="success"
            icon="el-icon-more"
            size="mini"
            circle
            @click="view_book(scope.row)"
          ></el-button>

          <el-button
            v-if="user_type=='2'"
            class="el-icon-my-export"
            size="mini"
            @click="popupBorrowDialog(scope.row)"
          ></el-button>

          <el-button
            v-if="user_type=='1'"
            type="primary"
            icon="el-icon-edit"
            size="mini"
            circle
            @click="update_book(scope.row)"
          ></el-button>
          <el-button
            v-if="user_type=='1'"
            type="danger"
            icon="el-icon-delete"
            size="mini"
            circle
            @click="delete_book(scope.row)"
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
          @click="delete_books()"
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
    <!-- 弹出框的学生明细表单 -->
    <el-dialog
      :title="dialog_title"
      :visible.sync="dialog_visible"
      width="700px"
      @close="close_dialog_form('book_form')"
      :close-on-click-modal="false"
    >
      <el-form
        :model="book_form"
        :rules="rules"
        ref="book_form"
        style="margin-left: 10px; margin-right: 15px;"
        label-width="90px"
        label-position="right"
        size="mini"
      >
        <el-upload
          action="#"
          class="avatar-uploader"
          :show-file-list="false"
          :http-request="upload_pic_post"
          :disabled="is_view"
          style="text-align: center; margin-bottom: 20px; "
        >
          <img v-if="book_form.bimage" :src="book_form.bimage_url" class="avatar" />
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <el-row>
          <el-col :span="12">
            <el-form-item label="编号：" prop="bid">
              <el-input
                v-model="book_form.bid"
                :disabled="is_view || is_edit"
                suffix-icon="el-icon-edit"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="书名：" prop="bname">
              <el-input v-model="book_form.bname" :disabled="is_view" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="作者：" prop="bauthor">
              <el-input v-model="book_form.bauthor" :disabled="is_view" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="出版社：">
              <el-input v-model="book_form.bcompany" :disabled="is_view" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="出版日期：">
              <el-input v-model="book_form.btime" :disabled="is_view" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分类：">
              <el-input v-model="book_form.bsort" :disabled="is_view" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="简介：">
              <el-input type="textarea" v-model="book_form.bcontent" :disabled="is_view"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          size="mini"
          @click="submit_book_form('book_form')"
          v-show="!is_view"
        >确 定</el-button>
        <el-button type="info" size="mini" @click="close_dialog_form('book_form')">取 消</el-button>
      </span>
    </el-dialog>

    <!-- 弹出框的图书借阅表单 -->
    <el-dialog
      title="图书借阅"
      :visible.sync="borrow_dialog_visible"
      width="400px"
      @close="close_borrow_dialog_form()"
      :close-on-click-modal="false"
    >
      <div class="form_wrapper" style="width: 300px; margin: auto auto;">
        <el-form
          :model="borrow_form"
          ref="borrow_form"
          style="margin-left: 10px; margin-right: 15px;"
          label-width="90px"
          label-position="right"
          size="mini"
        >
          <el-row>
            <el-col :span="24">
              <el-form-item label="借阅号：">
                <el-input v-model="borrow_form.brid" suffix-icon="el-icon-edit" disabled></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="图书编号：">
                <el-input v-model="borrow_form.bid" suffix-icon="el-icon-edit" disabled></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="书名：">
                <el-input v-model="borrow_form.bname" suffix-icon="el-icon-edit" disabled></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="库存编号：">
                <el-input v-model="borrow_form.bbid" suffix-icon="el-icon-edit" disabled></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="借阅时间：">
                <el-input v-model="borrow_form.brrowdate" suffix-icon="el-icon-edit" disabled></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-form-item label="归还日期：">
                <el-date-picker
                  v-model="borrow_form.returndate"
                  type="date"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期"
                  style="width: 185px;"
                ></el-date-picker>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" size="mini" @click="to_borrow()">确定借阅</el-button>
          <el-button type="info" size="mini" @click="close_borrow_dialog_form()">取消</el-button>
        </span>
      </div>
    </el-dialog>

    <!-- 删除‘借阅中’图书对话框 -->
    <el-dialog
      title="下列图书处于借阅中，不可删除"
      :visible.sync="delete_dialog_visible"
      width="200px"
      @close="close_delete_dialog_form()"
      :close-on-click-modal="false"
    >
      <el-table :data="in_borrowing_list" border style="width: 100%" size="mini">
        <el-table-column prop="bid" label="图书编号" align="center"></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
// js部分 逻辑部分

import axios from "axios";

export default {
  // el: "#app",
  name: "booksDiv",
  props: ["user_type", "user_id"], // 等价于data里面的user_type, user_id

  data() {
    // 校验图书编号是否存在
    const rules_bid = (rule, value, callback) => {
      if (this.is_edit) {
        callback();
      }
      // 使用Axios进行校验
      axios
        .post(this.baseURL + "bid/check/", {
          bid: value
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

    return {
      // msg: "Hello, Vue!",

      books: [], //所有的图书信息
      page_books: [], //分页后当前页的图书
      baseURL: "http://127.0.0.1:8000/",
      inputstr: "", //输入查询条件
      selected_books: [], // 选择复选框时的记录

      //分页相关的变量
      total: 0, //数据总行数
      currentpage: 1, //当前所在的页
      pagesize: 10, //每页显示多少行
      // 弹出框表单
      dialog_visible: false,
      dialog_title: "", // 弹出框的标题
      is_view: false, // 标识是否是查看
      is_edit: false, // 标识是否是修改
      book_form: {
        bid: "",
        bname: "",
        bauthor: "",
        bcompany: "",
        btime: "",
        bsort: "",
        bcontent: "",
        bimage: "",
        bimage_url: ""
      },
      rules: {
        bid: [
          { required: true, message: "编号不能为空", trigger: "blur" },
          { pattern: /^[\d]*$/, message: "编号必须是数字", trigger: "blur" },
          { validator: rules_bid, trigger: "blur" }
        ],
        bname: [{ required: true, message: "书名不能为空", trigger: "blur" }],
        bauthor: [{ required: true, message: "作者不能为空", trigger: "blur" }]
      },

      borrow_dialog_visible: false,
      borrow_form: {
        brid: "",
        bid: "", // 不发给后端
        bname: "", // 不发给后端
        rid: "",
        bbid: "",
        brrowdate: "",
        returndate: ""
      },

      delete_dialog_visible: false,
      in_borrowing_list: []
    };
  },
  mounted() {
    //自动加载数据
    this.get_books();

    // console.log("HHHHHHHHHHHHHHHHHHHHHHH");
    // console.log(this.books);
  },
  methods: {
    //获取所有图书信息
    get_books: function() {
      //记录this的地址
      let that = this; //axios会把this赋值为undefined
      //使用Axios实现Ajax请求
      axios
        .get(this.baseURL + "books/")
        .then(function(res) {
          //请求成功后执行的函数
          // console.log(res);
          if (res.data.code === 1) {
            //把数据给books
            that.books = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_books();
            //提示：
            that.$message({
              message: "数据加载成功！",
              type: "success"
            });

          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(function(err) {
          //请求失败后执行的函数
          console.log(err);
        });
    },
    get_all_books() {
      // 清空输入的inputstr
      this.inputstr = "";
      // 获取所有的数据
      this.get_books();
    },
    // 获取当前页的学生数据
    get_page_books: function() {
      // 清空page_books中的数据
      this.page_books = [];
      // 获得当前页的数据
      for (
        let i = (this.currentpage - 1) * this.pagesize;
        i < this.total;
        i++
      ) {
        this.page_books.push(this.books[i]);
        // 判断是否达到一页的要求
        if (this.page_books.length === this.pagesize) break;
      }
    },
    // 实现图书信息查询
    query_books() {
      // 使用Ajax请求--POST-->传递inputstr
      let that = this;
      // 开始Ajax请求
      axios
        .post(that.baseURL + "books/query/", {
          inputstr: that.inputstr
        })
        .then(function(res) {
          if (res.data.code === 1) {
            //把数据给books
            that.books = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_books();
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
    add_book() {
      // 修改标题
      this.dialog_title = "添加图书详情";
      // 弹出表单
      this.dialog_visible = true;
    },
    // 查看图书详情
    view_book(row) {
      // 修改标题
      this.dialog_title = "查看图书详情";
      // 修改is_view变量
      this.is_view = true;
      // 弹出表单
      this.dialog_visible = true;
      //this.book_form = row; //浅拷贝
      // 深拷贝方法2
      this.book_form = JSON.parse(JSON.stringify(row));

      // book_form的bimage已被传值
      // 给bimage_url赋值
      this.book_form.bimage_url =
        this.baseURL + "media/" + this.book_form.bimage;
    },
    // 修改图书详情
    update_book(row) {
      // 修改标题
      this.dialog_title = "修改图书详情";
      // 修改is_edit变量
      this.is_edit = true;
      // 弹出表单
      this.dialog_visible = true;
      //this.book_form = row; //浅拷贝
      // 深拷贝方法2
      this.book_form = JSON.parse(JSON.stringify(row));
      // book_form的bimage已被传值
      // 给bimage_url赋值
      this.book_form.bimage_url =
        this.baseURL + "media/" + this.book_form.bimage;
    },
    // 提交图书的表单（添加/修改）
    submit_book_form(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 校验成功后，执行添加或修改
          if (this.is_edit) {
            // 修改
            this.submit_update_book();
          } else {
            // 添加
            this.submit_add_book();
          }

          alert("submit!");
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 添加到数据库的函数
    submit_add_book() {
      // 定义that
      let that = this;
      // 执行Axios请求
      axios
        .post(that.baseURL + "books/add/", that.book_form)
        .then(res => {
          // 执行成功
          if (res.data.code === 1) {
            //把数据给books
            that.books = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_books();
            //提示：
            that.$message({
              message: "数据添加成功！",
              type: "success"
            });
            // 关闭窗体
            that.close_dialog_form("book_form");
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
    submit_update_book() {
      // 定义that
      let that = this;
      // 执行Axios请求
      axios
        .post(that.baseURL + "books/update/", that.book_form)
        .then(res => {
          // 执行成功
          if (res.data.code === 1) {
            //把数据给books
            that.books = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_books();
            //提示：
            that.$message({
              message: "数据修改成功！",
              type: "success"
            });
            // 关闭窗体
            that.close_dialog_form("book_form");
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
    delete_book(row) {
      // 等待确认
      this.$confirm(
        "是否确认删除图书信息【编号：" +
          row.bid +
          "\t书名：" +
          row.bname +
          "\t作者：" +
          row.bauthor +
          "？",
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
            .post(that.baseURL + "books/delete/", { bid: row.bid })
            .then(res => {
              if (res.data.code === 1) {
                if (res.data.delete_correct) {
                  //把数据给books
                  that.books = res.data.data;
                  // 获取返回记录的总行数
                  that.total = res.data.data.length;
                  // 获取当前页的数据
                  that.get_page_books();
                  //提示：
                  that.$message({
                    message: "数据删除成功！",
                    type: "success"
                  });
                } else {
                  // 该图书有库存被借阅中
                  that.$message.error(res.data.reason);
                }
              } else {
                that.$message.error(res.data.msg);
              }
            })
            .catch(err => {
              // 执行失败
              console.log(err);
              that.$message.error("删除时获取后端查询结果出现异常！");
            });

          // this.$message({
          //   type: "success",
          //   message: "删除成功!"
          // });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    delete_books() {
      // 等待确认
      this.$confirm(
        "是否确认批量删除" + this.selected_books.length + "条图书信息？",
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
            .post(that.baseURL + "books/batch_delete/", {
              batch_data: that.selected_books
            })
            .then(res => {
              if (res.data.code === 1) {
                //把数据给books
                that.books = res.data.data;
                // 获取返回记录的总行数
                that.total = res.data.data.length;
                // 获取当前页的数据
                that.get_page_books();

                if (res.data.delete_correct) {
                  //提示：
                  that.$message({
                    message: "数据批量删除成功！",
                    type: "success"
                  });
                } else {
                  // that.$message.error(res.data.interrupt_ones);

                  that.in_borrowing_list = res.data.interrupt_ones;
                  // 弹出表单
                  that.delete_dialog_visible = true;
                }
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
      this.book_form.bid = "";
      this.book_form.bname = "";
      this.book_form.bauthor = "";
      this.book_form.bcompany = "";
      this.book_form.btime = "";
      this.book_form.bsort = "";
      this.book_form.bcontent = "";

      // 清空image内容
      this.book_form.bimage = "";
      this.book_form.bimage_url = "";

      // 关闭
      this.dialog_visible = false;
      // 初始化is_edit和is_view的值
      this.is_edit = false;
      this.is_view = false;
    },
    // 选择图书图片后点击确定触发的事件
    upload_pic_post(file) {
      // 定义that
      let that = this;
      // 定义一个FormData类
      let fileReq = new FormData();
      // 把照片传进去
      fileReq.append("avatar", file.file);
      // 使用Axios发起Ajax请求
      axios({
        method: "post",
        url: that.baseURL + "upload/",
        data: fileReq
      })
        .then(res => {
          // 根据code判断是否成功
          if (res.data.code === 1) {
            // 把照片给bimage
            that.book_form.bimage = res.data.name;
            // 拼接bimage_url
            that.book_form.bimage_url = that.baseURL + "media/" + res.data.name;
          } else {
            // 失败的提示！
            that.$message.error(res.data.msg);
          }
        })
        .catch(err => {
          console.log(err);
          that.$message.error("上传图片出现异常");
        });
    },

    // 以下是图书借阅的函数
    popupBorrowDialog(row) {
      // 先查询有没有库存
      let that = this;
      // 开始Ajax请求
      axios
        .post(that.baseURL + "bookborrow/query_stock/", {
          bid: row.bid
        })
        .then(function(res) {
          if (res.data.code === 1) {
            if (res.data.circumstance === 0) {
              that.borrow_form.brid = res.data.data.brid;

              that.borrow_form.bid = row.bid;
              that.borrow_form.bname = row.bname;

              that.borrow_form.bbid = res.data.data.bbid;

              that.borrow_form.rid = that.user_id;
              that.borrow_form.brrowdate = res.data.data.brrowdate;
              that.borrow_form.returndate = "";

              // 弹出表单
              that.borrow_dialog_visible = true;
            } else if (
              res.data.circumstance === 1 ||
              res.data.circumstance === 2
            ) {
              that.$message.error(res.data.msg);
            }
          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(function(err) {
          console.log(err);
          that.$message.error("图书借阅获取后端查询结果出现异常！");
        });
    },

    to_borrow() {
      console.log("returndate = " + this.borrow_form.returndate);

      let borrow_request_form = {
        brid: this.borrow_form.brid,
        rid: this.borrow_form.rid,
        bbid: this.borrow_form.bbid,
        brrowdate: this.borrow_form.brrowdate,
        returndate: this.borrow_form.returndate
      };

      // 定义that
      let that = this;
      // 执行Axios请求
      axios
        .post(that.baseURL + "bookborrow/newborrow/", borrow_request_form)
        .then(res => {
          // 执行成功
          if (res.data.code === 1) {
            //提示：
            that.$message({
              message: "借阅成功！",
              type: "success"
            });
            // 关闭窗体
            that.close_borrow_dialog_form();
          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(err => {
          // 执行失败
          console.log(err);
          that.$message.error("借阅提交时获取后端查询结果出现异常！");
        });
    },

    close_borrow_dialog_form() {
      this.borrow_form.brid = "";

      this.borrow_form.bid = "";
      this.borrow_form.bname = "";

      this.borrow_form.bbid = "";

      this.borrow_form.rid = "";
      this.borrow_form.brrowdate = "";
      this.borrow_form.returndate = "";

      // 弹出表单
      this.borrow_dialog_visible = false;
    },

    close_delete_dialog_form() {
      this.in_borrowing_list = [];

      // 弹出表单
      this.delete_dialog_visible = false;
    },

    // 分页时修改每页的行数
    handle_size_change(size) {
      // 修改当前每页数据行数
      this.pagesize = size;
      // 数据重新分页
      this.get_page_books();
    },
    // 调整当前的页码
    handle_current_change(page_number) {
      // 修改当前的页码
      this.currentpage = page_number;
      // 数据重新分页
      this.get_page_books();
    },
    // 选择复选框时触发的操作
    handle_selection_change(data) {
      this.selected_books = data;
      // console.log(data);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>
#booksDiv {
  margin: 0px;
  padding: 0px;
  height: 100%;
}

/* 借阅按钮的图标 */
.el-icon-my-export {
  width: 28px;
  height: 32px;
  margin-bottom: 0px;
  background: url("../assets/image/borrowbook.jpg") center no-repeat;
  background-size: cover;
}

.form_wrapper {
  border-radius: 2px 2px 5px 5px;
  padding: 30px 30px 30px 30px;
  width: 90%;
  max-width: 360px;
  background: #e9eef3;
  position: relative;
  /* padding-bottom: 80px; */
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.3);
  border-radius: 20px;
}
.form_wrapper input {
  display: block;
  padding: 15px 10px;
  margin-bottom: 10px;
  width: 100%;
  border: 1px solid #ddd;
  /* transition: border-width 0.2s ease; */
  border-radius: 2px;
  color: #ccc;
}
</style>