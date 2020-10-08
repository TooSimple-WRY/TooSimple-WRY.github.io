from django.shortcuts import render

# 引入book的类
from reader.models import reader
from onebook.models import onebook
from bookborrow.models import bookborrow
# 引入JsonResponse模块
from django.http import JsonResponse

# 导入requests模块
import requests
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


def query_readers(request):
    # 查询读者信息
    # 接收传递过来的查询条件--- axios默认是json --- 字典类型（"inputstr"）-- data['inputstr']
    data = json.loads(request.body.decode('utf-8'))

    try:
        # 使用ORM获取所有满足条件的读者的信息
        obj_readers = reader.objects.filter(Q(rid__icontains=data['inputstr']) |
                                        Q(rname__icontains=data['inputstr']) |
                                        Q(rsex__icontains=data['inputstr']) |
                                        Q(rtype__icontains=data['inputstr']) |
                                        Q(rtel__icontains=data['inputstr']) |
                                        Q(remail__icontains=data['inputstr']) |
                                        Q(rpsd__icontains=data['inputstr'])
                                        ).values()
        # 把结果转为List
        readers = list(obj_readers)
        # 返回
        return JsonResponse({'code': 1, 'data': readers})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "查询读者信息失败，具体原因：" + str(e)})

def is_exists_rid(request):
    # 判断id为XXX的读者是否存在(reader表)的后端接口
    # 接收传递过来的id
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_readers = reader.objects.filter(rid = data['rid'])
        if  obj_readers.count() == 0:
            return JsonResponse({'code':1, 'exists':False})
        else:
            return JsonResponse({'code':1, 'exists':True})
    except Exception as e:
        return JsonResponse({'code':0, 'msg':"读者id校验失败，具体原因：" + str(e)})

def is_exists_rpsd(request):
    # 判断id为XXX的读者密码是否正确(reader表)的后端接口
    # 接收传递过来的reader账号密码
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_readers = reader.objects.filter(rid = data['rid'])
        print(type(obj_readers))
        if  obj_readers.count() == 0:
            return JsonResponse({'code': 1, 'psd_correct': False, 'reason': '账号不存在'})
        else:
            # 使用ORM获取所有满足条件的图书的信息
            obj_readers = reader.objects.filter(Q(rid=data['rid'])).values()
            print(type(obj_readers))
            # 把结果转为List
            readers = list(obj_readers)
            search_result = readers[0]['rpsd']
            if (data['rpsd'] == search_result):
                return JsonResponse({'code': 1, 'psd_correct':True})
            # 返回
            else:
                return JsonResponse({'code': 1, 'psd_correct': False, 'reason': '密码错误'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg':"读者密码校验失败，具体原因：" + str(e)})

def add_reader(request):
    #读者注册(reader表)的后端接口
    #添加读者到数据库
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 添加到数据库
        obj_reader = reader(rid=data['rid'],rname=data['rname'],rsex=data['rsex'],
                        rtype=data['rtype'],rtel=data['rtel'],
                        remail=data['remail'],rpsd=data['rpsd'])
        #执行添加
        obj_reader.save()

        # 返回
        return JsonResponse({'code': 1})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "新用户添加到数据库异常，具体原因:" + str(e)})

def updata_reader(request):
    #修改读者(reader表)的后端接口
    #修改读者到数据库
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        #查询到要修改的读者信息
        obj_reader = reader.objects.get(rid=data['rid'])
        #依次修改
        obj_reader.rname = data['rname']
        obj_reader.rsex = data['rsex']
        obj_reader.rtype = data['rtype']
        obj_reader.rtel = data['rtel']
        obj_reader.remail = data['remail']
        #保存
        obj_reader.save()
        # 使用ORM获取所有图书的信息
        obj_readers = reader.objects.all().values()
        # 把结果转为List
        readers = list(obj_readers)
        # 返回
        return JsonResponse({'code': 1, 'data': readers})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "修改保存到数据库异常，具体原因：" + str(e)})

def is_exists_rname(request):
    # 查询id号为XXX的读者的姓名
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_readers = reader.objects.filter(rid=data['rid'])
        if obj_readers.count() == 0:
            return JsonResponse({'code': 1, 'exists': False})
        else:
            obj_readers = reader.objects.filter(Q(rid=data['rid'])).values()
            # 把结果转为List
            readers = list(obj_readers)
            search_result = readers[0]['rname']
            return JsonResponse({'code': 1, 'user_name': search_result})
    except Exception as e:
        return JsonResponse({'code':0, 'msg':"查询读者姓名失败，具体原因：" + str(e)})

def updata_rpsd(request):
    # 读者修改密码
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        #查询到要修改的读者信息
        obj_reader = reader.objects.get(rid=data['rid'])
        #依次修改
        obj_reader.rpsd = data['rpsd']
        #保存
        obj_reader.save()
        # 返回
        return JsonResponse({'code': 1})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "读者密码修改保存到数据库异常，具体原因：" + str(e)})

def get_readers(request):
    """获取所有读者的信息"""
    try:
        # 使用ORM获取所有读者的信息
        obj_readers = reader.objects.all().values()
        # 把结果转为List
        readers = list(obj_readers)
        # 返回
        return JsonResponse({'code': 1, 'data': readers})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "获取所有读者信息失败，具体原因：" + str(e)})

def delete_reader(request):
    #删除读者的后端接口
    #删除一条读者信息
    data = json.loads(request.body.decode("utf-8"))
    try:
        # 查询到要删除的图书信息
        obj_reader = reader.objects.get(rid=data['rid'])
        obj_bookborrows = bookborrow.objects.filter(Q(rid=data['rid'])).values()
        for bookborrow1 in obj_bookborrows:
            obj_onebook = onebook.objects.get(bbid=bookborrow1['bbid'])
            obj_onebook.delete()
            obj_bookborrow = bookborrow.objects.get(brid=bookborrow1['brid'])
            obj_bookborrow.delete()
        # 删除
        obj_reader.delete()
        # 使用ORM获取所有图书的信息
        obj_readers = reader.objects.all().values()
        # 把结果转为List
        readers = list(obj_readers)
        # 返回
        return JsonResponse({'code': 1, 'data': readers})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "删除读者信息写入数据库异常，具体原因：" + str(e)})

def delete_readers(request):
    #批量删除读者的后端接口
    #批量删除读者信息
    data = json.loads(request.body.decode("utf-8"))
    try:
        #遍历传递的集合
        for one_reader in data['batch_data']:
            #查询当前记录
            obj_reader = reader.objects.get(rid=one_reader['rid'])
            obj_bookborrows = bookborrow.objects.filter(Q(rid=one_reader['rid'])).values()
            for bookborrow1 in obj_bookborrows:
                obj_onebook = onebook.objects.get(bbid=bookborrow1['bbid'])
                obj_onebook.delete()
                obj_bookborrow = bookborrow.objects.get(brid=bookborrow1['brid'])
                obj_bookborrow.delete()
            #执行删除
            obj_reader.delete()
        # 使用ORM获取所有读者的信息
        obj_readers = reader.objects.all().values()
        # 把结果转为List
        readers = list(obj_readers)
        # 返回
        return JsonResponse({'code': 1, 'data': readers})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "批量删除读者信息写入数据库异常，具体原因：" + str(e)})