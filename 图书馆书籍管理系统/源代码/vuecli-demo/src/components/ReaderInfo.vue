<template>
  <!-- HTML结构：只能有一个跟标签 -->
  <div v-if="user_type=='1'" id="readerinfoDiv">
    <!-- 表单 -->
    <el-form :inline="true" style="margin-top: 20px;" @submit.native.prevent="query_readers">
      <el-row>
        <el-col :span="12" style="text-align: left;">
          <el-form-item label="请输入查询条件">
            <el-input
              v-model="inputstr"
              placeholder="输入查询条件"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8" style="text-align: right; padding-right: 10px;">
          <el-button-group>
            <el-button type="primary" icon="el-icon-search" @click="query_readers()">查询</el-button>
            <el-button type="primary" icon="el-icon-tickets" @click="get_all_readers()">全部</el-button>
          </el-button-group>
        </el-col>
        <el-col :span="2">
          <!-- <el-upload> -->
          <el-button type="primary">导入Excel</el-button>
          <!-- </el-upload> -->
        </el-col>
        <el-col :span="2">
          <el-button type="primary">导出Excel</el-button>
        </el-col>
      </el-row>
    </el-form>
    <!-- 表格 -->
    <el-table
      :data="page_readers"
      border
      style="width: 100%"
      size="mini"
      @selection-change="handle_selection_change"
    >
      <el-table-column type="selection" align="center" min-width="5%"></el-table-column>
      <el-table-column type="index" label="序号" align="center" min-width="5%"></el-table-column>
      <el-table-column prop="rid" label="读者编号" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="rname" label="姓名" align="center" min-width="12%"></el-table-column>
      <el-table-column prop="rsex" label="性别" align="center" min-width="8%"></el-table-column>
      <el-table-column prop="rtype" label="读者类型" align="center" min-width="12%"></el-table-column>
      <el-table-column prop="rtel" label="联系方式" align="center" min-width="16%"></el-table-column>
      <el-table-column prop="remail" label="邮箱" align="center" min-width="17%"></el-table-column>
      <el-table-column label="操作" align="center" min-width="10%">
        <template slot-scope="scope">
          <el-button
            type="danger"
            icon="el-icon-delete"
            size="mini"
            circle
            @click="delete_reader(scope.row)"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-row style="margin-top: 10px;">
      <el-col :span="8" style="text-align: left;">
        <el-button type="danger" icon="el-icon-delete" @click="delete_readers()" size="mini">批量删除</el-button>
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
  </div>

  <div v-else id="readerinfoDiv">
    <div class="form_wrapper" style="width: 300px; margin: auto auto;">
      <el-form
        :model="readerinfo_form"
        :rules="rules"
        ref="readerinfo_form"
        style="margin-left: 10px; margin-right: 15px;"
        label-width="90px"
        label-position="right"
        size="mini"
      >
        <el-row>
          <el-col :span="24">
            <el-form-item label="读者编号：">
              <el-input v-model="readerinfo_form.rid" suffix-icon="el-icon-edit" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="真实姓名：">
              <el-input v-model="readerinfo_form.rname" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="性别：">
              <el-select v-model="readerinfo_form.rsex">
                <el-option
                  v-for="item in gender_options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="读者类型：">
              <el-select v-model="readerinfo_form.rtype">
                <el-option
                  v-for="item in category_options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="联系方式：">
              <el-input v-model="readerinfo_form.rtel" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="邮箱：">
              <el-input v-model="readerinfo_form.remail" suffix-icon="el-icon-edit"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" size="mini" @click="update_readerinfo()">确定修改</el-button>
      </span>
    </div>
  </div>
</template>

<script>
// js部分 逻辑部分

import axios from "axios";

export default {
  // el: "#app",
  name: "readersDiv",

  props: ["user_type", "user_id"], // 等价于data里面的user_type, user_id

  data() {
    return {
      readers: [], //所有的读者信息
      page_readers: [], //分页后当前页的图书
      baseURL: "http://127.0.0.1:8000/",
      inputstr: "", //输入查询条件
      selected_readers: [], // 选择复选框时的记录

      //分页相关的变量
      total: 0, //数据总行数
      currentpage: 1, //当前所在的页
      pagesize: 10, //每页显示多少行

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

      readerinfo_form: {
        rid: "",
        rname: "",
        rsex: "",
        rtype: "",
        rtel: "",
        remail: ""
      },
      rules: {
        rname: [{ required: true, message: "编号不能为空", trigger: "blur" }]
      }
    };
  },
  mounted() {
    if (this.user_type == "1") {
      //自动加载数据
      this.get_readers();
      // console.log(this.readers);
    } else {
      this.query_reader();
    }
  },
  methods: {
    //获取所有图书信息
    get_readers: function() {
      //记录this的地址
      let that = this; //axios会把this赋值为undefined
      //使用Axios实现Ajax请求
      axios
        .get(this.baseURL + "all_readers/")
        .then(function(res) {
          //请求成功后执行的函数
          // console.log(res);
          if (res.data.code === 1) {
            //把数据给readers
            that.readers = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_readers();
            //提示：
            that.$message({
              message: "数据加载成功！",
              type: "success"
            });

            // console.log(that.readers);
          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(function(err) {
          //请求失败后执行的函数
          console.log(err);
        });
    },
    get_all_readers() {
      // 清空输入的inputstr
      this.inputstr = "";
      // 获取所有的数据
      this.get_readers();
    },
    // 获取当前页的学生数据
    get_page_readers: function() {
      // 清空page_readers中的数据
      this.page_readers = [];
      // 获得当前页的数据
      for (
        let i = (this.currentpage - 1) * this.pagesize;
        i < this.total;
        i++
      ) {
        this.page_readers.push(this.readers[i]);
        // 判断是否达到一页的要求
        if (this.page_readers.length === this.pagesize) break;
      }
    },
    query_reader() {
      this.readerinfo_form.rid = this.user_id;

      let that = this;
      // 开始Ajax请求
      axios
        .post(that.baseURL + "readers/query/", {
          inputstr: that.readerinfo_form.rid
        })
        .then(function(res) {
          if (res.data.code === 1) {
            let data = res.data.data[0]; //这样赋值？？？

            that.readerinfo_form.rname = data.rname;
            that.readerinfo_form.rsex = data.rsex;
            that.readerinfo_form.rtype = data.rtype;
            that.readerinfo_form.rtel = data.rtel;
            that.readerinfo_form.remail = data.remail;
          } else {
            that.$message.error(res.data.msg);
          }
        })
        .catch(function(err) {
          console.log(err);
          that.$message.error("获取后端查询结果出现异常！");
        });
    },
    update_readerinfo() {
      // 定义that
      let that = this;
      // 执行Axios请求
      axios
        .post(that.baseURL + "readerinfo/update/", that.readerinfo_form)
        .then(res => {
          // 执行成功
          if (res.data.code === 1) {
            //提示：
            that.$message({
              message: "个人信息修改成功！",
              type: "success"
            });
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
    // 实现图书信息查询
    query_readers() {
      // 使用Ajax请求--POST-->传递inputstr
      let that = this;
      // 开始Ajax请求
      axios
        .post(that.baseURL + "readers/query/", {
          inputstr: that.inputstr
        })
        .then(function(res) {
          if (res.data.code === 1) {
            //把数据给readers
            that.readers = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_readers();
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
    // 删除一条图书信息
    delete_reader(row) {
      // 等待确认
      this.$confirm(
        "是否确认删除读者【编号：" + row.rid + "？",
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
            .post(that.baseURL + "readers/delete/", { rid: row.rid })
            .then(res => {
              if (res.data.code === 1) {
                //把数据给readers
                that.readers = res.data.data;
                // 获取返回记录的总行数
                that.total = res.data.data.length;
                // 获取当前页的数据
                that.get_page_readers();
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
    delete_readers() {
      // 等待确认
      this.$confirm(
        "是否确认批量删除" + this.selected_readers.length + "条读者信息？",
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
            .post(that.baseURL + "readers/batch_delete/", {
              batch_data: that.selected_readers
            })
            .then(res => {
              if (res.data.code === 1) {
                //把数据给readers
                that.readers = res.data.data;
                // 获取返回记录的总行数
                that.total = res.data.data.length;
                // 获取当前页的数据
                that.get_page_readers();
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
    // 分页时修改每页的行数
    handle_size_change(size) {
      // 修改当前每页数据行数
      this.pagesize = size;
      // 数据重新分页
      this.get_page_readers();
    },
    // 调整当前的页码
    handle_current_change(page_number) {
      // 修改当前的页码
      this.currentpage = page_number;
      // 数据重新分页
      this.get_page_readers();
    },
    // 选择复选框时触发的操作
    handle_selection_change(data) {
      this.selected_readers = data;
      // console.log(data);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>
/* 注意：这里不加scoped, home.css的样式会污染全局，但加上之后el-upload的样式会默认是element-ui的自带样式，故先不加 */
#readerinfoDiv {
  margin-top: 20px;
  padding: 0px;
  height: 100%;
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