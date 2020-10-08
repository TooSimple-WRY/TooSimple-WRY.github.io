<template>
  <!-- HTML结构：只能有一个跟标签 -->
  <div id="borrowDiv">
    <!-- 表单 -->
    <el-form :inline="true" style="margin-top: 20px;" @submit.native.prevent="query_borrows">
      <el-row>
        <el-col :span="12" style="text-align: left;">
          <el-form-item label="请输入查询条件">
            <el-input v-model="inputstr" placeholder="输入查询条件"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8" style="text-align: right; padding-right: 10px;">
          <el-button-group>
            <el-button type="primary" icon="el-icon-search" @click="query_borrows()">查询</el-button>
            <el-button type="primary" icon="el-icon-tickets" @click="get_all_borrows()">全部</el-button>
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
    <el-table :data="page_borrows" border style="width: 100%" size="mini">
      <el-table-column type="index" label="序号" align="center" min-width="5%"></el-table-column>
      <el-table-column prop="brid" label="借阅号" align="center" min-width="12%"></el-table-column>
      <el-table-column prop="bid" label="图书编号" align="center" min-width="12%"></el-table-column>
      <el-table-column prop="bname" label="书名" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="bbid" label="库存编号" align="center" min-width="15%"></el-table-column>
      <el-table-column v-if="user_type=='1'" prop="rid" label="读者编号" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="brrowdate" label="借出日期" align="center" min-width="15%"></el-table-column>
      <el-table-column prop="returndate" label="归还日期" align="center" min-width="13%"></el-table-column>
      <el-table-column v-if="user_type=='2'" label="操作" align="center" min-width="13%">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="delete_borrow(scope.row)"
            plain
          >归还</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-row style="margin-top: 10px;">
      <el-col :span="8" style="text-align: left;"></el-col>
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
</template>

<script>
// js部分 逻辑部分

import axios from "axios";

export default {
  // el: "#app",
  name: "borrowDiv",

  props: ["user_type", "user_id"], // 等价于data里面的user_type, user_id

  data() {
    return {
      borrows: [], //所有的图书信息
      page_borrows: [], //分页后当前页的图书
      baseURL: "http://127.0.0.1:8000/",
      inputstr: "", //输入查询条件

      //分页相关的变量
      total: 0, //数据总行数
      currentpage: 1, //当前所在的页
      pagesize: 10, //每页显示多少行

      borrow_form: {
        brid: "",
        bid: "",
        bname: "",
        bbid: "",
        rid: "",
        brrowdate: "",
        returndate: ""
      }
    };
  },
  mounted() {
    //自动加载数据
    if (this.user_type == "1") {
      this.get_borrows();
    } else {
      this.get_my_borrows();
    }
  },
  methods: {
    //获取所有图书信息
    get_borrows: function() {
      //记录this的地址
      let that = this; //axios会把this赋值为undefined
      //使用Axios实现Ajax请求
      axios
        .get(this.baseURL + "all_borrows/")
        .then(function(res) {
          //请求成功后执行的函数
          if (res.data.code === 1) {
            //把数据给borrows
            that.borrows = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_borrows();
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
    get_my_borrows: function() {
      // 使用Ajax请求--POST-->传递inputstr
      let that = this;
      // 开始Ajax请求
      axios
        .post(that.baseURL + "my_borrows/", {
          rid: that.user_id
        })
        .then(function(res) {
          if (res.data.code === 1) {
            //把数据给borrows
            that.borrows = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_borrows();
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
    get_all_borrows() {
      // 清空输入的inputstr
      this.inputstr = "";
      // 获取所有的数据
      if (this.user_type == '1'){
      this.get_borrows();
      }else{
        this.get_my_borrows();
      }
    },
    // 获取当前页的学生数据
    get_page_borrows: function() {
      // 清空page_borrows中的数据
      this.page_borrows = [];
      // 获得当前页的数据
      for (
        let i = (this.currentpage - 1) * this.pagesize;
        i < this.total;
        i++
      ) {
        this.page_borrows.push(this.borrows[i]);
        // 判断是否达到一页的要求
        if (this.page_borrows.length === this.pagesize) break;
      }
    },
    // 实现图书信息查询
    query_borrows() {
      // 使用Ajax请求--POST-->传递inputstr
      let that = this;
      // 开始Ajax请求
      axios
        .post(that.baseURL + "borrows/query/", {
          inputstr: that.inputstr
        })
        .then(function(res) {
          if (res.data.code === 1) {
            //把数据给borrows
            that.borrows = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_borrows();
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

     // 实现图书信息查询
    reader_query_borrows() {
      // 使用Ajax请求--POST-->传递inputstr
      let that = this;
      // 开始Ajax请求
      axios
        .post(that.baseURL + "borrows/query/reader/", {
          inputstr: that.inputstr,
          rid: that.user_id
        })
        .then(function(res) {
          if (res.data.code === 1) {
            //把数据给borrows
            that.borrows = res.data.data;
            // 获取返回记录的总行数
            that.total = res.data.data.length;
            // 获取当前页的数据
            that.get_page_borrows();
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
    delete_borrow(row) {
      // 等待确认
      this.$confirm(
        "是否确认归还图书【库存编号：" + row.bbid + "】？",
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
            .post(that.baseURL + "borrows/delete/", 
            { 
              brid: row.brid,
              rid: that.user_id 
            })
            .then(res => {
              if (res.data.code === 1) {
                //把数据给borrows
                that.borrows = res.data.data;
                // 获取返回记录的总行数
                that.total = res.data.data.length;
                // 获取当前页的数据
                that.get_page_borrows();
                //提示：
                that.$message({
                  message: "还书成功！",
                  type: "success"
                });
              } else {
                that.$message.error(res.data.msg);
              }
            })
            .catch(err => {
              // 执行失败
              console.log(err);
              that.$message.error("还书时获取后端查询结果出现异常！");
            });

          this.$message({
            type: "success",
            message: "还书成功!"
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消还书"
          });
        });
    },

    // 分页时修改每页的行数
    handle_size_change(size) {
      // 修改当前每页数据行数
      this.pagesize = size;
      // 数据重新分页
      this.get_page_borrows();
    },
    // 调整当前的页码
    handle_current_change(page_number) {
      // 修改当前的页码
      this.currentpage = page_number;
      // 数据重新分页
      this.get_page_borrows();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>
/* 注意：这里不加scoped, home.css的样式会污染全局，但加上之后el-upload的样式会默认是element-ui的自带样式，故先不加 */
#borrowDiv {
  margin: 0px;
  padding: 0px;
  height: 100%;
}
</style>