const app = new Vue({
    el: "#app",
    data() {
        // 校验图书编号是否存在
        const rules_bid = (rule, value, callback) => {
            if (this.is_edit) {
                callback();
            }
            // 使用Axios进行校验
            axios.post(
                this.baseURL + "bid/check/",
                {
                    bid: value,
                }
            )
                .then((res) => {
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
                .catch((err) => {
                    console.log(err);
                });
        }

        return {
            // msg: "Hello, Vue!",
            books: [], //所有的图书信息
            page_books: [], //分页后当前页的图书
            baseURL: "http://127.0.0.1:8000/",
            inputstr: '', //输入查询条件
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
                bimage_url: "",
            },
            rules: {
                bid: [
                    { required: true, message: "编号不能为空", trigger: "blur" },
                    { pattern: /^[\d]*$/, message: "编号必须是数字", trigger: "blur" },
                    { validator: rules_bid, trigger: "blur" },
                ],
                bname: [
                    { required: true, message: "书名不能为空", trigger: "blur" },
                ],
                bauthor: [
                    { required: true, message: "作者不能为空", trigger: "blur" },
                ],
            }
        }
    },
    mounted() {
        //自动加载数据
        this.get_books();
    },
    methods: {
        //获取所有图书信息
        get_books: function () {
            //记录this的地址
            let that = this //axios会把this赋值为undefined
            //使用Axios实现Ajax请求
            axios
                .get(this.baseURL + "books/")
                .then(function (res) {
                    //请求成功后执行的函数
                    console.log(res);
                    if (res.data.code === 1) {
                        //把数据给books
                        that.books = res.data.data;
                        // 获取返回记录的总行数
                        that.total = res.data.data.length;
                        // 获取当前页的数据
                        that.get_page_books();
                        //提示：
                        that.$message({
                            message: '数据加载成功！',
                            type: 'success'
                        });
                    } else {
                        that.$message.error(res.data.msg);
                    }
                })
                .catch(function (err) {
                    //请求失败后执行的函数
                    console.log(err);
                })
        },
        get_all_books() {
            // 清空输入的inputstr
            this.inputstr = "";
            // 获取所有的数据
            this.get_books();
        },
        // 获取当前页的学生数据
        get_page_books: function () {
            // 清空page_books中的数据
            this.page_books = [];
            // 获得当前页的数据
            for (let i = (this.currentpage - 1) * this.pagesize; i < this.total; i++) {
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
                .post(
                    that.baseURL + "books/query/",
                    {
                        inputstr: that.inputstr
                    }
                )
                .then(function (res) {
                    if (res.data.code === 1) {
                        //把数据给books
                        that.books = res.data.data;
                        // 获取返回记录的总行数
                        that.total = res.data.data.length;
                        // 获取当前页的数据
                        that.get_page_books();
                        //提示：
                        that.$message({
                            message: '查询数据加载成功！',
                            type: 'success'
                        });
                    } else {
                        that.$message.error(res.data.msg);
                    }
                })
                .catch(function (err) {
                    console.log(err);
                    that.$message.error("获取后端查询结果出现异常！");
                })
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
            // console.log(this.book_form);

            // book_form的bimage已被传值
            // 给bimage_url赋值
            this.book_form.bimage_url = this.baseURL + 'media/' + this.book_form.bimage;
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
            this.book_form.bimage_url = this.baseURL + 'media/' + this.book_form.bimage;

        },
        // 提交图书的表单（添加/修改）
        submit_book_form(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    // 校验成功后，执行添加或修改
                    if (this.is_edit) {
                        // 修改
                        this.submit_update_book();
                    } else {
                        // 添加
                        this.submit_add_book();
                    }

                    alert('submit!');
                } else {
                    console.log('error submit!!');
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
                            message: '数据添加成功！',
                            type: 'success'
                        });
                        // 关闭窗体
                        that.close_dialog_form('book_form');
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
                            message: '数据修改成功！',
                            type: 'success'
                        });
                        // 关闭窗体
                        that.close_dialog_form('book_form');
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
            this.$confirm('是否确认删除图书信息【编号：' + row.bid + '\t书名：' + row.bname + '\t作者：' + row.bauthor + '？', '是否继续?',
                '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                // 确认删除响应事件
                let that = this
                // 调用后端接口
                axios
                    .post(that.baseURL + 'books/delete/', { bid: row.bid })
                    .then(res => {
                        if (res.data.code === 1) {
                            //把数据给books
                            that.books = res.data.data;
                            // 获取返回记录的总行数
                            that.total = res.data.data.length;
                            // 获取当前页的数据
                            that.get_page_books();
                            //提示：
                            that.$message({
                                message: '数据删除成功！',
                                type: 'success'
                            });
                        } else {
                            that.$message.error(res.data.msg);
                        }
                    })
                    .catch(err => { // 执行失败
                        console.log(err);
                        that.$message.error("删除时获取后端查询结果出现异常！");
                    });

                this.$message({
                    type: 'success',
                    message: '删除成功!'
                });
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },
        delete_books() {
            // 等待确认
            this.$confirm('是否确认批量删除' + this.selected_books.length + '条图书信息？', '是否继续?',
                '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                // 确认删除响应事件
                let that = this
                // 调用后端接口
                axios
                    .post(that.baseURL + 'books/batch_delete/', { batch_data: that.selected_books })
                    .then(res => {
                        if (res.data.code === 1) {
                            //把数据给books
                            that.books = res.data.data;
                            // 获取返回记录的总行数
                            that.total = res.data.data.length;
                            // 获取当前页的数据
                            that.get_page_books();
                            //提示：
                            that.$message({
                                message: '数据批量删除成功！',
                                type: 'success'
                            });
                        } else {
                            that.$message.error(res.data.msg);
                        }
                    })
                    .catch(err => { // 执行失败
                        console.log(err);
                        that.$message.error("删除时获取后端查询结果出现异常！");
                    });

                this.$message({
                    type: 'success',
                    message: '删除成功!'
                });
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
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
            fileReq.append('avatar', file.file);
            // 使用Axios发起Ajax请求
            axios(
                {
                    method: 'post',
                    url: that.baseURL + 'upload/',
                    data: fileReq
                }
            ).then(res => {
                // 根据code判断是否成功
                if (res.data.code === 1){
                    // 把照片给bimage
                    that.book_form.bimage = res.data.name;
                    // 拼接bimage_url
                    that.book_form.bimage_url = that.baseURL + "media/" + res.data.name;
                }else{
                    // 失败的提示！
                    that.$message.error(res.data.msg);
                }
            }).catch(err => {
                console.log(err);
                that.$message.error("上传图片出现异常");
            })
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

        },
    }
})