from django.shortcuts import render

# Create your views here.

# 引入onebook,book的类
from book.models import book
from onebook.models import onebook
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

def get_onebooks(request):
    #获取所有库存信息的接口(onebook表)
    """获取所有库存的信息"""
    try:
        # 使用ORM获取所有图书的信息
        obj_onebooks = onebook.objects.all().values()
        obj_books = book.objects.all().values()
        # 把结果转为List
        onebooks = list(obj_onebooks)
        books = list(obj_books)
        i = 0
        for onebook1 in onebooks:
            for book1 in books:
                if book1['bid'] == onebook1['bid']:
                    onebooks[i]['bname'] = book1['bname']
                    i+=1
        # 返回
        return JsonResponse({'code': 1, 'data': onebooks})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "获取所有库存信息失败，具体原因：" + str(e)})

def query_onebooks(request):
    # 查询库存信息
    # 接收传递过来的查询条件--- axios默认是json --- 字典类型（"inputstr"）-- data['inputstr']
    data = json.loads(request.body.decode('utf-8'))

    try:
        # 使用ORM获取所有满足条件的图书的信息
        obj_books = book.objects.filter(Q(bname__icontains=data['inputstr'])).values()
        # search_result = readers[0]['rpsd']
        if (obj_books.count() > 0):
            # 把结果转为List
            books = list(obj_books)

            onebooks = [] #记录即将返回的所有库存
            for single_book in books:
                obj_onebooks = onebook.objects.filter(Q(bid__icontains=single_book['bid'])).values()
                one_batch = list(obj_onebooks)

                for item in one_batch:
                    onebooks.append(item)
            obj_books = book.objects.all().values()
            # 把结果转为List
            books = list(obj_books)
            i = 0
            for onebook1 in onebooks:
                for book1 in books:
                    if book1['bid'] == onebook1['bid']:
                        onebooks[i]['bname'] = book1['bname']
                        i += 1

            return JsonResponse({'code': 1, 'data': onebooks})
        # 返回
        else:
            obj_onebooks = onebook.objects.filter(Q(bbid__icontains=data['inputstr']) |
                                            Q(bid__icontains=data['inputstr']) |
                                            Q(sheft__icontains=data['inputstr']) |
                                            Q(place__icontains=data['inputstr']) |
                                            Q(statu__icontains=data['inputstr'])
                                            ).values()
            # 把结果转为List
            onebooks = list(obj_onebooks)
            obj_books = book.objects.all().values()
            # 把结果转为List
            books = list(obj_books)
            i = 0
            for onebook1 in onebooks:
                for book1 in books:
                    if book1['bid'] == onebook1['bid']:
                        onebooks[i]['bname'] = book1['bname']
                        i += 1
            # 返回
            return JsonResponse({'code': 1, 'data': onebooks})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "查询库存失败，具体原因" + str(e)})

def is_exists_bbid(request):
    # 判断编号为XXX的图书是否存在(onebook表)的后端接口
    # 接收传递过来的书号
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_onebooks = onebook.objects.filter(bbid = data['bbid'])
        if  obj_onebooks.count() == 0:
            return JsonResponse({'code':1, 'exists':False})
        else:
            return JsonResponse({'code':1, 'exists':True})
    except Exception as e:
        return JsonResponse({'code':0, 'msg':"校验库存编号失败，具体原因：" + str(e)})

def add_onebook(request):
    #添加图书(onebook表)的后端接口
    #添加书籍到数据库
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 添加到数据库
        obj_onebook = onebook(bbid=data['bbid'],bid=data['bid'],sheft=data['sheft'],
                        place=data['place'],statu=data['statu'])
        #执行添加
        obj_onebook.save()
        # 使用ORM获取所有图书的信息
        obj_onebooks = onebook.objects.all().values()
        obj_books = book.objects.all().values()
        # 把结果转为List
        onebooks = list(obj_onebooks)
        books = list(obj_books)
        i = 0
        for onebook1 in onebooks:
            for book1 in books:
                if book1['bid'] == onebook1['bid']:
                    onebooks[i]['bname'] = book1['bname']
                    i += 1
        # 返回
        return JsonResponse({'code': 1, 'data': onebooks})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "新库存添加到数据库异常，具体原因：" + str(e)})

def updata_onebook(request):
    #修改库存(onebook表)的后端接口
    #修改库存到数据库
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        #查询到要修改的图书信息
        obj_onebook = onebook.objects.get(bbid=data['bbid'])
        #依次修改
        obj_onebook.bid = data['bid']
        obj_onebook.sheft = data['sheft']
        obj_onebook.place = data['place']
        obj_onebook.statu = data['statu']
        #保存
        obj_onebook.save()
        # 使用ORM获取所有图书的信息
        obj_onebooks = onebook.objects.all().values()
        obj_books = book.objects.all().values()
        # 把结果转为List
        onebooks = list(obj_onebooks)
        books = list(obj_books)
        i = 0
        for onebook1 in onebooks:
            for book1 in books:
                if book1['bid'] == onebook1['bid']:
                    onebooks[i]['bname'] = book1['bname']
                    i += 1
        # 返回
        return JsonResponse({'code': 1, 'data': onebooks})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "更改库存到数据库异常，具体原因：" + str(e)})

def delete_onebook(request):
    #删除库存(onebook表)的后端接口
    #删除一条图书信息
    data = json.loads(request.body.decode("utf-8"))
    # print(data)
    try:
        # 查询到要删除的图书信息
        obj_onebook = onebook.objects.get(bbid=data['bbid'])
        # 删除
        obj_onebook.delete()
        # 使用ORM获取所有图书的信息
        obj_onebooks = onebook.objects.all().values()
        # 把结果转为List
        onebooks = list(obj_onebooks)
        obj_books = book.objects.all().values()
        books = list(obj_books)
        i = 0
        for onebook1 in onebooks:
            for book1 in books:
                if book1['bid'] == onebook1['bid']:
                    onebooks[i]['bname'] = book1['bname']
                    i += 1
        # 返回
        return JsonResponse({'code': 1, 'data': onebooks})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "删除库存信息写入数据库异常，具体原因：" + str(e)})

def delete_onebooks(request):
    #批量删除库存(onebook)的后端接口
    #批量删除图书信息
    data = json.loads(request.body.decode("utf-8"))
    try:
        #遍历传递的集合
        for one_onebook in data['batch_data']:
            #查询当前记录
            obj_onebook = onebook.objects.get(bbid=one_onebook['bbid'])
            #执行删除
            obj_onebook.delete()
        # 使用ORM获取所有图书的信息
        obj_onebooks = onebook.objects.all().values()
        # 把结果转为List
        onebooks = list(obj_onebooks)
        obj_books = book.objects.all().values()
        books = list(obj_books)
        i = 0
        for onebook1 in onebooks:
            for book1 in books:
                if book1['bid'] == onebook1['bid']:
                    onebooks[i]['bname'] = book1['bname']
                    i += 1
        # 返回
        return JsonResponse({'code': 1, 'data': onebooks})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "批量删除库存信息写入数据库异常，具体原因：" + str(e)})