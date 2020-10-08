from django.shortcuts import render

# 引入book的类
from administrator.models import administrator
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

def is_exists_apsd(request):
    # 查询id为XXX的管理员密码是否正确(admin表)的后端接口
    # 接收传递过来的administrator账号密码
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_administrators = administrator.objects.filter(aid = data['aid'])
        if  obj_administrators.count() == 0:
            return JsonResponse({'code': 1, 'psd_correct': False, 'reason': '账号不存在'})
        else:
            # 使用ORM获取所有满足条件的图书的信息
            obj_administrators = administrator.objects.filter(Q(aid=data['aid'])).values()
            # 把结果转为List
            administrators = list(obj_administrators)
            search_result = administrators[0]['apsd']
            if (data['apsd'] == search_result):
                return JsonResponse({'code': 1, 'psd_correct':True})
            # 返回
            else:
                return JsonResponse({'code': 1, 'psd_correct': False, 'reason': '密码错误'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg':"管理员密码校验失败，具体原因：" + str(e)})

def is_exists_aname(request):
    # 查询id号为XXX的管理员的姓名
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_administrators = administrator.objects.filter(Q(aid=data['aid'])).values()
        if  obj_administrators.count() == 0:
            return JsonResponse({'code':1, 'exists':False})
        else:
            administrators = list(obj_administrators)
            return JsonResponse({'code':1, 'user_name':administrators[0]['aname']})
    except Exception as e:
        return JsonResponse({'code':0, 'msg':"查询管理员姓名失败，具体原因：" + str(e)})

def updata_apsd(request):
    # 管理员修改密码
    #接收前端传递过来的值
    data = json.loads(request.body.decode("utf-8"))
    try:
        #查询到要修改的管理员信息
        obj_admin = administrator.objects.get(aid=data['aid'])
        #依次修改
        obj_admin.apsd = data['apsd']
        #保存
        obj_admin.save()
        # 返回
        return JsonResponse({'code': 1})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "管理员密码修改保存到数据库异常，具体原因：" + str(e)})