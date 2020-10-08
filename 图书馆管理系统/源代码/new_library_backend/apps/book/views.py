from django.shortcuts import render
# 引入book的类
from book.models import book
from onebook.models import onebook
from bookborrow.models import bookborrow
# 引入JsonResponse模块
from django.http import JsonResponse

# 导入json模块
import json
# 导入Q查询
from django.db.models import Q
# 导入uuid类
import uuid
# 导入哈希库
import hashlib
# 导入Setting
from django.conf import settings
import os


# Create your views here.

def get_books(request):
    """获取所有图书的信息"""
    try:
        # 使用ORM获取所有图书的信息
        obj_books = book.objects.all().values()
        # 把结果转为List
        books = list(obj_books)
        # 返回
        return JsonResponse({'code': 1, 'data': books})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "获取图书信息出现异常，具体错误：" + str(e)})

def query_books(request):
    # 查询图书信息
    # 接收传递过来的查询条件--- axios默认是json --- 字典类型（"inputstr"）-- data['inputstr']
    data = json.loads(request.body.decode('utf-8'))

    try:
        # 使用ORM获取所有满足条件的图书的信息
        obj_books = book.objects.filter(Q(bid__icontains=data['inputstr']) |
                                        Q(bname__icontains=data['inputstr']) |
                                        Q(bauthor__icontains=data['inputstr']) |
                                        Q(bcompany__icontains=data['inputstr']) |
                                        Q(btime__icontains=data['inputstr']) |
                                        Q(bsort__icontains=data['inputstr'])
                                        ).values()
        # 把结果转为List
        books = list(obj_books)
        # 返回
        return JsonResponse({'code': 1, 'data': books})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "获取图书信息出现异常，具体错误：" + str(e)})

def is_exists_bid(request):
    # 判断书号为XXX的图书是否存在(book表)的后端接口
    # 接收传递过来的书号
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_books = book.objects.filter(Q(bid=data['bid'])).values()
        if  obj_books.count() == 0:
            return JsonResponse({'code':1, 'exists':False})
        else:
            books = list(obj_books)
            return JsonResponse({'code':1, 'exists':True, 'bname':books[0]['bname']})
    except Exception as e:
        return JsonResponse({'code':0, 'msg':"校验图书编号失败，具体原因：" + str(e)})

def add_book(request):
    #添加图书(book表)的后端接口
    #添加书籍到数据库
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 添加到数据库
        obj_book = book(bid=data['bid'],bname=data['bname'],bauthor=data['bauthor'],
                        bcompany=data['bcompany'],btime=data['btime'],
                        bsort=data['bsort'],bcontent=data['bcontent'],bimage=data['bimage'])
        #执行添加
        obj_book.save()
        # 使用ORM获取所有图书的信息
        obj_books = book.objects.all().values()
        # 把结果转为List
        books = list(obj_books)
        # 返回
        return JsonResponse({'code': 1, 'data': books})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "添加到数据库异常，具体原因：" + str(e)})

def updata_book(request):
    #修改图书(book表)的后端接口
    #修改图书到数据库
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        #查询到要修改的图书信息
        obj_book = book.objects.get(bid=data['bid'])
        #依次修改
        obj_book.bname = data['bname']
        obj_book.bauthor = data['bauthor']
        obj_book.bcompany = data['bcompany']
        obj_book.btime = data['btime']
        obj_book.bsort = data['bsort']
        obj_book.bcontent = data['bcontent']
        obj_book.bimage = data['bimage']
        #保存
        obj_book.save()
        # 使用ORM获取所有图书的信息
        obj_books = book.objects.all().values()
        # 把结果转为List
        books = list(obj_books)
        # 返回
        return JsonResponse({'code': 1, 'data': books})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "修改保存到数据库异常，具体原因：" + str(e)})

def delete_book(request):
    #删除图书(book表)的后端接口
    #删除一条图书信息
    data = json.loads(request.body.decode("utf-8"))
    # print(data)
    try:
        # 查询到要删除的图书信息
        obj_book = book.objects.get(bid=data['bid'])
        # 删除
        obj_onebooks = onebook.objects.filter(Q(bid=data['bid'])).values()
        for onebook1 in obj_onebooks:
            if onebook1['statu'] == '借阅中':
                return JsonResponse({'code': 1, 'delete_correct': False, 'reason': '库存中有书籍正在被借阅'})
        for onebook2 in obj_onebooks:
            obj_onebook = onebook.objects.get(bbid=onebook2['bbid'])
            obj_onebook.delete()
        obj_book.delete()
        # 使用ORM获取所有图书的信息
        obj_books = book.objects.all().values()
        # 把结果转为List
        books = list(obj_books)
        # 返回
        return JsonResponse({'code': 1, 'delete_correct': True, 'data': books})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "删除图书信息写入数据库异常，具体原因：" + str(e)})

def delete_books(request):
    #批量删除图书(book表)的后端接口
    #批量删除图书信息
    data = json.loads(request.body.decode("utf-8"))
    try:
        bookids = []
        #遍历传递的集合
        for one_book in data['batch_data']:
            #查询当前记录
            flag = True
            obj_book = book.objects.get(bid=one_book['bid'])
            obj_onebooks = onebook.objects.filter(Q(bid=one_book['bid'])).values()
            for onebook1 in obj_onebooks:
                if onebook1['statu'] == '借阅中':
                    flag = False
                    bookids.append({'bid':one_book['bid']})
                    break
            if flag:
                for onebook2 in obj_onebooks:
                    obj_onebook = onebook.objects.get(bbid=onebook2['bbid'])
                    obj_onebook.delete()
                #执行删除
                obj_book.delete()
        # 使用ORM获取所有图书的信息
        obj_books = book.objects.all().values()
        # 把结果转为List
        books = list(obj_books)
        # 返回
        if bookids:
            return JsonResponse({'code': 1, 'delete_correct': False, 'interrupt_ones': bookids, 'data':books})
        return JsonResponse({'code': 1, 'delete_correct': True, 'data': books})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "批量删除图书信息写入数据库异常，具体原因：" + str(e)})


def upload(request):
    """接收上传的文件"""
    # 接收上传的文件
    rev_file = request.FILES.get('avatar')
    # 判断，是否有文件
    if not rev_file:
        return JsonResponse({'code': 0, 'msg': '图片不存在！'})
    # 获得一个唯一的名字：uuid + hash
    new_name = get_random_str()
    # 准备写入的url
    file_path = os.path.join(settings.MEDIA_ROOT, new_name + os.path.splitext(rev_file.name)[1])
    # 开始写入到本地磁盘
    try:
        f = open(file_path, 'wb')
        # 多次写入(大文件)
        for i in rev_file.chunks():
            f.write(i)
        # 关闭
        f.close()
        return JsonResponse({'code': 1, 'name': new_name + os.path.splitext(rev_file.name)[1]})

    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


def get_random_str():

    # 获取uuid的随机数
    uuid_val = uuid.uuid4()
    # 获取uuid的随机数字符串
    uuid_str = str(uuid_val).encode('utf-8')
    # 获取md5实例
    md5 = hashlib.md5()
    # 拿去uuid的md5摘要
    md5.update(uuid_str)
    # 返回固定长度的字符串
    return md5.hexdigest()