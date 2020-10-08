"""new_library_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book import views
from reader import views as view1
from administrator import views as view2
from onebook import views as view3
from bookborrow import views as view4
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', views.get_books), # 获取所有图书信息的接口
    path('books/query/', views.query_books), # 查询图书信息
    path('bid/check/', views.is_exists_bid), # 校验编号是否存在
    path('books/add/', views.add_book), #添加图书(book表)的后端接口
    path('books/update/', views.updata_book), #修改图书(book表)的后端接口
    path('books/delete/', views.delete_book), #删除图书(book表)的后端接口
    path('books/batch_delete/', views.delete_books), #批量删除图书(book表)的后端接口
    path('upload/', views.upload), #上传文件的接口
    path('rid/check/', view1.is_exists_rid), #判断id为XXX的读者是否存在(reader表)的后端接口
    path('login/reader/', view1.is_exists_rpsd),#判断id为XXX的读者密码是否正确(reader表)的后端接口
    path('login/admin/', view2.is_exists_apsd), #查询id为XXX的管理员密码是否正确(admin表)的后端接口
    path("register/reader/", view1.add_reader), #读者注册(reader表)的后端接口
    path("all_stocks/", view3.get_onebooks), #获取所有库存信息的接口(onebook表)
    path("stocks/query/", view3.query_onebooks), #查询库存信息
    path('bbid/check/', view3.is_exists_bbid), #判断编号为XXX的图书是否存在(onebook表)的后端接口
    path('stocks/add/', view3.add_onebook), #添加图书(onebook表)的后端接口
    path('stocks/update/', view3.updata_onebook), #更改库存(onebook表)的后端接口
    path('stocks/delete/', view3.delete_onebook), #删除库存的后端接口
    path('stocks/batch_delete/', view3.delete_onebooks), #批量删除库存的后端接口
    path('username/admin/', view2.is_exists_aname), # 查询id号为XXX的管理员的姓名
    path('username/reader/', view1.is_exists_rname), #查询id为XXX的读者姓名
    path('password/update/admin/', view2.updata_apsd), #管理员修改密码
    path('password/update/reader/', view1.updata_rpsd), #读者修改密码
    path('all_readers/', view1.get_readers), #获取所有读者信息的接口
    path('readers/query/', view1.query_readers), #查询读者信息的后端接口
    path('readers/delete/', view1.delete_reader), #删除读者的后端接口
    path('readers/batch_delete/', view1.delete_readers), #批量删除读者的后端接口
    path('readerinfo/update/', view1.updata_reader), #读者修改个人信息
    path('bookborrow/query_stock/', view4.query_brid), #查询可借阅的库存
    path('bookborrow/newborrow/', view4.reader_add_bookborrow), #读者添加借阅归还日期
    path('all_borrows/', view4.get_bookborrows), #获取所有借阅的接口
    path('borrows/query/', view4.query_bookborrows), #查询借阅的后端接口
    path('borrows/delete/', view4.delete_bookborrow), #删除借阅（还书）的后端接口
    path('my_borrows/', view4.query_readers), #获取“我的借阅”的后端接口
    path('borrows/query/reader/', view4.query_bookborrows_reader) #读者查询借阅的后端接口
]
# 添加这行--- 允许所有的media文件被访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)