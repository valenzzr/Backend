from django.shortcuts import render
from django.http import *
from airport.models import Passenger
# Create your views here.


# 旅客注册功能
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('identification')
        username = request.POST.get('username')
        password = request.POST.get('password')

    if Passenger.objects.filter(username=username).exists():
        return JsonResponse({
            '该用户已注册，请勿重复注册！'
        })
    else:
        passenger = Passenger.objects.create(name=name,email=email,phone_number=phone_number,username=username,password=password)
        passenger.save()
        return JsonResponse({
            '恭喜您，注册成功！'
        })


# # 旅客登录功能
# def login(request):
#     if request.method == 'POST':
