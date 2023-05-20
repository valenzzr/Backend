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
        # data = request.json

        data = json.loads(request.body)
        print(data)
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        identification = data.get('identification')
        username = data.get('username')
        password = data.get('password')
        print(name, email, phone_number, identification, username, password)

    if Passenger.objects.filter(username=username).exists():
        return JsonResponse({
            'message': '该用户已注册，请勿重复注册！'
        })
    else:
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
# # 旅客登录功能
# def login(request):
#     if request.method == 'POST':
