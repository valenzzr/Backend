import json
import time
import datetime

import jwt
from django.db import IntegrityError
from django.shortcuts import render
from django.http import *
from airport.models import *
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from tools.Login_dec import logging_check
import hashlib



# Create your views here.
flight_arr = []


def save_flight(flight):
    flight_arr.append(flight)


def print_flight():
    for flight in flight_arr:
        print(flight)


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


class UpdateInfoViews(View):
    def put(self, request):
        json_str = request.body
        data = json.loads(json_str)
        user = request.nowuser


class AddFlightViews(View):  # 添加航班信息

    def check_flight_availability(self,flight_number, departure_datetime, runway):  # 判断起飞前后30min是否存在其他飞机起飞
        departure_datetime1 = datetime.datetime.strptime(departure_datetime, "%Y-%m-%d %H:%M:%S")
        thirty_minutes = datetime.timedelta(minutes=30)
        min_datetime = departure_datetime1 - thirty_minutes
        max_datetime = departure_datetime1 + thirty_minutes

        existing_flights = Flight.objects.filter(
            runway=runway,
            departure_datetime__range=(min_datetime, max_datetime)
        )

        if existing_flights.exists():
            return False

        return True

    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        flight_number = data.get("flight_number")
        airline_name = data.get('airline_name')
        departure_datetime = data.get('departure_datetime')
        arrival_datetime = data.get('arrival_datetime')
        origin = data.get('origin')
        destination = data.get('destination')
        price = data.get('price')
        terminal = data.get('terminal')
        gate = data.get('gate')
        runway = data.get('runway')
        status = 'waitForAdd'  # 该航班尚未被管理员添加
        old_flight = Flight.objects.filter(flight_number=flight_number)
        if old_flight:
            return JsonResponse({
                'code': 10300, 'error': '航班已存在'
            })
        if departure_datetime > arrival_datetime:
            return JsonResponse({
                'code': 10301, 'error': '错误的出发和到达时间'
            })
        old_terminal = Terminal.objects.filter(terminal_number=terminal)
        old_runway = Runway.objects.filter(runway_number=runway)
        old_gate = Gate.objects.filter(gate_number=gate)
        old_airline = Airline.objects.filter(name=airline_name)
        if not old_terminal:
            return JsonResponse({
                'code': 10302, 'error': '不存在该航站楼'
            })
        if not old_gate:
            return JsonResponse({
                'code': 10303, 'error': '不存在该登机口'
            })
        if not old_runway:
            return JsonResponse({
                'code': 10305, 'error': '不存在该跑道'
            })
        if not old_airline:
            return JsonResponse({
                'code': 10306, 'error': '不存在该航司'
            })
        if not self.check_flight_availability(flight_number, departure_datetime, runway):
            return JsonResponse({
                'code': 10305, 'error': '该航班所处的跑道前后三十分钟有其他飞机起飞！'
            })
        need_terminal = Terminal.objects.get(terminal_number=terminal)
        need_gate = Gate.objects.get(gate_number=gate)
        need_runway = Runway.objects.get(runway_number=runway)
        need_airline = Airline.objects.get(name=airline_name)
        try:
            flight = Flight.objects.create(flight_number=flight_number, departure_datetime=departure_datetime, arrival_datetime= arrival_datetime, price= price,
                                  status= status,origin= origin,destination= destination,airline_name=need_airline,terminal= need_terminal,gate= need_gate,runway= need_runway)
            save_flight(flight)
            return JsonResponse({
                'message': '恭喜您，添加成功！'
            })
        except IntegrityError as e:
            return JsonResponse({'message': str(e)})
        finally:
            print_flight()


class BuyTicketsViews(View):
    def post(self,request):
        json_str = request.body
        data = json.loads(json_str)
        flight_number = data.get('flight_number')
        try:
            old_flight = Flight.objects.get(flight_number = flight_number)
        except Exception as e:
            return JsonResponse({
                'code': 10401, 'error': '不存在该航班，请重新选择'
            })
        departure_datetime = old_flight.departure_datetime
        arrival_datetime = old_flight.arrival_datetime
        origin = old_flight.origin
        destination = old_flight.destination
        status = "unpaying"
        airline_name = old_flight.airline_name
        terminal = old_flight.terminal
        gate = old_flight.gate
        identification = data.get('identification')
        try:
            old_passenger = Passenger.objects.get(identification = identification)
        except Exception as e:
            return JsonResponse({
                'code': 10402, 'error': '不存在该旅客，是否已注册？'
            })
        try:
            ticket = Ticket.objects.create(passenger = old_passenger, departure_datetime=departure_datetime, arrival_datetime= arrival_datetime,
                                  destination= destination,origin= origin,status= status,airline_name=airline_name,terminal= terminal,gate= gate)
            ticket.save()
            return JsonResponse({'message': '购票成功，请支付'})
        except Exception as e:
            return JsonResponse({
                'message': str(e)
            })
        # TODO：后面实现支付功能，并将状态改为已支付，支付失败则删除信息


class SearchInformationViews(View):
    def post(self,request):
        json_str = request.body
        data = json.loads(json_str)
        origin = data.get('origin')
        destination = data.get('destination')
        flight_list = Flight.objects.filter(origin=origin, destination=destination)  # 查询对应航班
        dict1 = {}
        for i in flight_list:
            if i.departure_datetime > datetime.datetime.now():  # 如果航班现在没有起飞，则传回该航班
                dict1[i.flight_number] = {'flight_number':i.flight_number,'airline_name':i.airline_name.name,'origin':i.origin,'destination':i.destination,
                                      'departure_datetime':i.departure_datetime,'arrival_datetime':i.arrival_datetime,
                                      'price':i.price,'terminal':i.terminal.terminal_number,'gate':i.gate.gate_number,'runway':i.runway.runway_number}

        return JsonResponse(dict1)


class SearchTicketViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        identification = data.get('identification')


# 生成登录令牌用于记录会话状态
def make_token(username, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now_time = time.time()
    payload_data = {'username': username, 'exp': now_time + expire}
    return jwt.encode(payload_data, key, algorithm='HS256')

