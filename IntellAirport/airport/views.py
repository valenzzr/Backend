import json
import time

import jwt
from django.db import IntegrityError
from django.shortcuts import render
from django.http import *
from airport.models import Passenger
from django.views import View
from django.conf import settings
import hashlib


# Create your views here.


# 旅客注册功能
class RegisterViews(View):
    def post(self, request):
        # json格式提交数据
        json_str = request.body
        data = json.loads(json_str)
        print(data)
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        identification = data.get('identification')
        username = data.get('username')
        password_1 = data.get('password_1')
        password_2 = data.get('password_2')
        print(name, email, phone_number, identification, username, password_1)

        if password_1 != password_2:
            return JsonResponse({
                'code': 10100, 'error': '两次密码不一致，请重新输入密码'
            })

        old_passenger = Passenger.objects.filter(name=name)
        if old_passenger:
            return JsonResponse({
                'code': 10101, 'error': '用户已存在'
            })

        p_m = hashlib.md5()
        p_m.update(password_1.encode())

        try:
            passenger = Passenger.objects.create(name=name, email=email, phone_number=phone_number,
                                                 identification=identification, username=username,
                                                 password=p_m.hexdigest())
            passenger.save()
            return JsonResponse({
                'message': '恭喜您，注册成功！'
            })
        except IntegrityError as e:
            return JsonResponse({'message': str(e)})


# 旅客登录功能

class LoginViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        name = data.get('name')
        phone_number = data.get('phone_number')
        username = data.get('username')
        password = data.get('password')

        try:
            old_passenger = Passenger.objects.get(username=username)
        except Exception as e:
            return JsonResponse({
                'code': 10200, 'error': '用户名或密码错误'
            })

        p_m = hashlib.md5()
        p_m.update(password.encode())
        if p_m.hexdigest() != old_passenger.password:
            return JsonResponse({
                'code': 10200, 'error': '用户名或密码错误'
            })

        # 记录会话状态
        token = make_token(username)
        return JsonResponse({
            'message': '登陆成功', 'username': username, 'data': {'token': token}
        })


# 生成登录令牌用于记录会话状态
def make_token(username, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now_time = time.time()
    payload_data = {'username': username, 'exp': now_time + expire}
    return jwt.encode(payload_data, key, algorithm='HS256')
