from django.shortcuts import render
import random
import time
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

def query_brid(request):
    # 接收传递过来的书号
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_onebooks = onebook.objects.filter(Q(bid=data['bid'])).values()
        if  obj_onebooks.count() == 0:
            return JsonResponse({'code':1, 'circumstance': 1, 'msg': "十分抱歉，此图书目前没有库存。"})
        else:
            onebooks = list(obj_onebooks)
            # 把结果转为List
            for onebook1 in onebooks:
                if onebook1['statu'] == '可借':
                    bbid1 = onebook1['bbid']
                    obj_bookborrows = bookborrow.objects.all().values()
                    # 把结果转为List
                    bookborrows = list(obj_bookborrows)
                    while True:
                        brid1 = str(random.randint(10000000,9999999999))
                        k = True
                        # i = 0
                        for bookborrow1 in bookborrows:
                            # i += 1
                            if brid1 == bookborrow1['brid']:
                                k = False
                        # if i == 9990000000:
                        #     break
                        if k:
                            brrowdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                            return JsonResponse({'code': 1, 'circumstance': 0,'data':
                                {
                                    'brid': brid1,
                                    'bbid': bbid1,
                                    'brrowdate': brrowdate
                                }
                            })
            return JsonResponse({'code':1, 'circumstance': 2, 'msg': "十分抱歉，此图书处于借阅中，请稍后再来。"})
    except Exception as e:
        return JsonResponse({'code':0, 'msg':"图书借阅查询库存失败，具体原因：" + str(e)})

def reader_add_bookborrow(request):
    #添加图书(bookborrow表)的后端接口
    #添加书籍到数据库
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 添加到数据库
        obj_bookborrow = bookborrow(brid=data['brid'],rid=data['rid'],bbid=data['bbid'],
                        brrowdate=data['brrowdate'],returndate=data['returndate'])
        #执行添加
        obj_bookborrow.save()
        obj_onebook = onebook.objects.get(bbid=data['bbid'])
        # 依次修改
        obj_onebook.statu = '借阅中'
        # 保存
        obj_onebook.save()
        # 返回
        return JsonResponse({'code': 1})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "新库存添加到数据库异常，具体原因：" + str(e)})

def get_bookborrows(request):
    # 获取所有借阅的接口
    try:
        # 使用ORM获取所有图书的信息
        obj_bookborrows = bookborrow.objects.all().values()
        obj_onebooks = onebook.objects.all().values()
        obj_books = book.objects.all().values()
        # 把结果转为List
        bookborrows = list(obj_bookborrows)
        onebooks = list(obj_onebooks)
        books = list(obj_books)
        for bookborrow1 in bookborrows:
            for onebook1 in onebooks:
                if bookborrow1['bbid'] == onebook1['bbid']:
                    bookborrow1['bid'] = onebook1['bid']
                    for book1 in books:
                        if book1['bid'] == bookborrow1['bid']:
                            bookborrow1['bname'] = book1['bname']
        # 返回
        return JsonResponse({'code': 1, 'data': bookborrows})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "获取所有借阅信息失败，具体原因：" + str(e)})

def query_bookborrows(request):
    # 查询借阅信息
    # 接收传递过来的查询条件--- axios默认是json --- 字典类型（"inputstr"）-- data['inputstr']
    data = json.loads(request.body.decode('utf-8'))

    try:
        # 使用ORM获取所有满足条件的图书的信息
        obj_books = book.objects.filter(
            Q(bid__icontains=data['inputstr']) |
            Q(bname__icontains=data['inputstr'])
            ).values()
        if (obj_books.count() > 0):
            # 把结果转为List
            books = list(obj_books)
            onebooks = [] #记录即将返回的所有库存
            for single_book in books:
                obj_onebooks = onebook.objects.filter(Q(bid__icontains=single_book['bid'])).values()
                one_batch = list(obj_onebooks)
                for item in one_batch:
                    onebooks.append(item)
            bookborrows = []  # 记录即将返回的所有借阅信息
            for single_onebook in onebooks:
                if single_onebook['statu'] == '借阅中':
                    obj_bookborrows = bookborrow.objects.filter(Q(bbid__icontains=single_onebook['bbid'])).values()
                    one_batch = list(obj_bookborrows)
                    for item in one_batch:
                        bookborrows.append(item)
            # 把结果转为List
            obj_onebooks = onebook.objects.all().values()
            obj_books = book.objects.all().values()
            onebooks = list(obj_onebooks)
            books = list(obj_books)
            for bookborrow1 in bookborrows:
                for onebook1 in onebooks:
                    if bookborrow1['bbid'] == onebook1['bbid']:
                        bookborrow1['bid'] = onebook1['bid']
                        for book1 in books:
                            if book1['bid'] == bookborrow1['bid']:
                                bookborrow1['bname'] = book1['bname']
            return JsonResponse({'code': 1, 'data': bookborrows})
        # 返回
        else:
            obj_bookborrows = bookborrow.objects.filter(Q(brid__icontains=data['inputstr']) |
                                            Q(rid__icontains=data['inputstr']) |
                                            Q(bbid__icontains=data['inputstr']) |
                                            Q(brrowdate__icontains=data['inputstr']) |
                                            Q(returndate__icontains=data['inputstr'])
                                            ).values()
            # 把结果转为List
            bookborrows = list(obj_bookborrows)
            obj_onebooks = onebook.objects.all().values()
            obj_books = book.objects.all().values()
            onebooks = list(obj_onebooks)
            books = list(obj_books)
            for bookborrow1 in bookborrows:
                for onebook1 in onebooks:
                    if bookborrow1['bbid'] == onebook1['bbid']:
                        bookborrow1['bid'] = onebook1['bid']
                        for book1 in books:
                            if book1['bid'] == bookborrow1['bid']:
                                bookborrow1['bname'] = book1['bname']
            # 返回
            return JsonResponse({'code': 1, 'data': bookborrows})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "查询借阅信息失败，具体原因" + str(e)})

def delete_bookborrow(request):
    #删除借阅（还书）的后端接口
    #删除一条借阅信息
    data = json.loads(request.body.decode("utf-8"))
    # print(data)
    try:
        # 查询到要删除的图书信息
        obj_bookborrow = bookborrow.objects.get(brid=data['brid'])
        obj_onebook = onebook.objects.get(bbid=obj_bookborrow.bbid)
        # 依次修改
        obj_onebook.statu = '可借'
        # 保存
        obj_onebook.save()
        # 删除
        obj_bookborrow.delete()
        # 使用ORM获取所有图书的信息
        obj_bookborrows = bookborrow.objects.filter(Q(rid__icontains=data['rid'])).values()
        # 把结果转为List
        bookborrows = list(obj_bookborrows)
        obj_onebooks = onebook.objects.all().values()
        obj_books = book.objects.all().values()
        onebooks = list(obj_onebooks)
        books = list(obj_books)
        for bookborrow1 in bookborrows:
            for onebook1 in onebooks:
                if bookborrow1['bbid'] == onebook1['bbid']:
                    bookborrow1['bid'] = onebook1['bid']
                    for book1 in books:
                        if book1['bid'] == bookborrow1['bid']:
                            bookborrow1['bname'] = book1['bname']
        # 返回
        return JsonResponse({'code': 1, 'data': bookborrows})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "还书信息写入数据库异常，具体原因：" + str(e)})

def query_readers(request):
    # 查询读者信息
    # 接收传递过来的查询条件--- axios默认是json --- 字典类型（"inputstr"）-- data['inputstr']
    data = json.loads(request.body.decode('utf-8'))

    try:
        # 使用ORM获取所有满足条件的借阅的信息
        obj_bookborrow = bookborrow.objects.filter(Q(rid=data['rid'])).values()
        bookborrows = list(obj_bookborrow)
        obj_onebooks = onebook.objects.all().values()
        obj_books = book.objects.all().values()
        onebooks = list(obj_onebooks)
        books = list(obj_books)
        for bookborrow1 in bookborrows:
            for onebook1 in onebooks:
                if bookborrow1['bbid'] == onebook1['bbid']:
                    bookborrow1['bid'] = onebook1['bid']
                    for book1 in books:
                        if book1['bid'] == bookborrow1['bid']:
                            bookborrow1['bname'] = book1['bname']
        return JsonResponse({'code': 1, 'data': bookborrows})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "获取我的借阅失败，具体原因：" + str(e)})

def query_bookborrows_reader(request):
    # 查询借阅信息
    # 接收传递过来的查询条件--- axios默认是json --- 字典类型（"inputstr"）-- data['inputstr']
    data = json.loads(request.body.decode('utf-8'))

    try:
        # 使用ORM获取所有满足条件的图书的信息
        obj_books = book.objects.filter(
            Q(bid__icontains=data['inputstr']) |
            Q(bname__icontains=data['inputstr'])
            ).values()
        if (obj_books.count() > 0):
            # 把结果转为List
            books = list(obj_books)
            onebooks = [] #记录即将返回的所有库存
            for single_book in books:
                obj_onebooks = onebook.objects.filter(Q(bid__icontains=single_book['bid'])).values()
                one_batch = list(obj_onebooks)
                for item in one_batch:
                    onebooks.append(item)
            bookborrows = []  # 记录该读者的所有借阅信息
            for single_onebook in onebooks:
                if single_onebook['statu'] == '借阅中':
                    obj_bookborrows = bookborrow.objects.filter(Q(bbid__icontains=single_onebook['bbid'])).values()
                    one_batch = list(obj_bookborrows)
                    for item in one_batch:
                        if item['rid'] == data['rid']:
                            bookborrows.append(item)
            # 把结果转为List
            obj_onebooks = onebook.objects.all().values()
            obj_books = book.objects.all().values()
            onebooks = list(obj_onebooks)
            books = list(obj_books)
            for bookborrow1 in bookborrows:
                for onebook1 in onebooks:
                    if bookborrow1['bbid'] == onebook1['bbid']:
                        bookborrow1['bid'] = onebook1['bid']
                        for book1 in books:
                            if book1['bid'] == bookborrow1['bid']:
                                bookborrow1['bname'] = book1['bname']
            return JsonResponse({'code': 1, 'data': bookborrows})
        # 返回
        else:
            obj_bookborrows = bookborrow.objects.filter(Q(brid__icontains=data['inputstr']) |
                                            Q(rid__icontains=data['inputstr']) |
                                            Q(bbid__icontains=data['inputstr']) |
                                            Q(brrowdate__icontains=data['inputstr']) |
                                            Q(returndate__icontains=data['inputstr'])
                                            ).values()
            # 把结果转为List
            bookborrows = []  # 记录该读者的所有借阅信息
            one_batch = list(obj_bookborrows)
            for item in one_batch:
                if item['rid'] == data['rid']:
                    bookborrows.append(item)
            obj_onebooks = onebook.objects.all().values()
            obj_books = book.objects.all().values()
            onebooks = list(obj_onebooks)
            books = list(obj_books)
            for bookborrow1 in bookborrows:
                for onebook1 in onebooks:
                    if bookborrow1['bbid'] == onebook1['bbid']:
                        bookborrow1['bid'] = onebook1['bid']
                        for book1 in books:
                            if book1['bid'] == bookborrow1['bid']:
                                bookborrow1['bname'] = book1['bname']
            # 返回
            return JsonResponse({'code': 1, 'data': bookborrows})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "查询借阅信息失败，具体原因" + str(e)})