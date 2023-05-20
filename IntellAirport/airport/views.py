import json

from django.db import IntegrityError
from django.shortcuts import render
from django.http import *
from airport.models import Passenger


# Create your views here.


# 旅客注册功能
def register(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        identification = request.POST.get('identification')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(name, email, phone_number, identification, username, password)

        # json格式提交数据
        # data = json.loads(request.body)
        # print(data)
        # name = data.get('name')
        # email = data.get('email')
        # phone_number = data.get('phone_number')
        # identification = data.get('identification')
        # username = data.get('username')
        # password = data.get('password')
        # password2 = data.get('password2')
        # print(name, email, phone_number, identification, username, password)

    if Passenger.objects.filter(username=username).exists():
        return JsonResponse({
            'message': '该用户已注册，请勿重复注册！'
        })
    else:
        if password != password2:
            return JsonResponse({
                'message': '两次密码不一致，请重新输入密码！'
            })
        try:
            passenger = Passenger.objects.create(name=name, email=email, phone_number=phone_number,
                                                 identification=identification, username=username,
                                                 password=password)
            passenger.save()
            return JsonResponse({
                'message': '恭喜您，注册成功！'
            })
        except IntegrityError as e:
            return JsonResponse({'message': str(e)})


# 旅客登录功能
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
