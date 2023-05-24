import json
import time
import datetime

import jwt
from django.core.mail import send_mail
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


# 生成登录令牌用于记录会话状态
def make_token(username, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now_time = time.time()
    payload_data = {'username': username, 'exp': now_time + expire}
    return jwt.encode(payload_data, key, algorithm='HS256')


# 发送邮件函数
def send_email(request):
    # 邮件主题
    subject = "ACF activate"
    # 邮件内容
    message = "Hello"
    # 发件人
    from_email = "949011578@qq.com"
    # 收件人，可以是多个，以列表的形式存储
    recipient_list = ["152xxxx7756@sina.cn", "iino-miko@outlook.com", ]
    send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)
    return HttpResponse("Send email success")


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
            send_email(request)
            return JsonResponse({
                'message': '恭喜您，注册成功！'
            })
        except IntegrityError as e:
            return JsonResponse({'message': str(e)})


# 测试Token
class CheckToken(View):
    @method_decorator(logging_check)
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        name = data.get('name')
        # phone_number = data.get('phone_number')
        username = data.get('username')
        password = data.get('password')

        try:
            old_passenger = Passenger.objects.get(username=username, name=name)
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
        # Token
        token = make_token(username)
        return HttpResponse('okk')
        # return JsonResponse({
        #     'message': '登陆成功', 'username': username, 'data': {'token': token}
        # })


# 旅客登录功能
class LoginViews(View):
    @method_decorator(logging_check)
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        name = data.get('name')
        # phone_number = data.get('phone_number')
        username = data.get('username')
        password = data.get('password')

        try:
            old_passenger = Passenger.objects.get(username=username, name=name)
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
        # Token
        # token = make_token(username)
        # return JsonResponse({
        #     'message': '登陆成功', 'username': username, 'data': {'token': token}
        # })

        # Session
        request.session['username'] = username
        request.session['name'] = name
        print(username, name)

        return JsonResponse({
            'code': 200,
            'message': '登录成功'
        })


@logging_check
# 更新用户信息
class UpdateInfoViews(View):
    @method_decorator(logging_check)
    def put(self, request):
        json_str = request.body
        data = json.loads(json_str)

        # user = request.myuser

        username = request.session.get('username')
        name = request.session.get('name')
        try:
            user = Passenger.objects.get(username=username, name=name)
        except Exception as e:
            return JsonResponse({
                'code': 10201,
                'error': '未登录或登录已过期，请重新登录'
            })
        phone_number = data.get('phone_number')
        email = data.get('email')
        password = data.get('password')
        if phone_number:
            user.phone_number = phone_number
        if email:
            user.email = email
        if password:
            user.password = password
        user.save()
        return JsonResponse({
            'code': 200, 'message': '修改个人信息成功'
        })


# 上传用户头像
@logging_check
def UploadImage(request):
    if request.method != 'POST':
        return JsonResponse({
            'code': 10103, 'error': 'Please use POST'
        })

    user = request.myuser

    avatar = request.FILES['avatar']
    user.avatar = avatar
    user.save()
    return JsonResponse({
        'code': 200, 'message': '上传头像成功'
    })


class AddFlightViews(View):  # 添加航班信息

    def check_flight_availability(self, flight_number, departure_datetime, arrive_datetime, runway):  # 判断起飞降落时间是否合法
        departure_datetime1 = datetime.datetime.strptime(departure_datetime, "%Y-%m-%d %H:%M:%S")
        arrival_datetime2 = datetime.datetime.strptime(arrive_datetime, "%Y-%m-%d %H:%M:%S")
        if arrival_datetime2 < departure_datetime1:
            return False
        if arrival_datetime2 < datetime.datetime.now() or departure_datetime1 < datetime.datetime.now():
            return False
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
        if not self.check_flight_availability(flight_number, departure_datetime, arrival_datetime, runway):
            return JsonResponse({
                'code': 10305, 'error': '航班时间设置存在问题，请检查是否航班时间已过、起飞时间晚于降落时间或在同一跑道上前后30min有其他航班起飞'
            })
        need_terminal = Terminal.objects.get(terminal_number=terminal)
        need_gate = Gate.objects.get(gate_number=gate)
        need_runway = Runway.objects.get(runway_number=runway)
        need_airline = Airline.objects.get(name=airline_name)
        try:
            flight = Flight.objects.create(flight_number=flight_number, departure_datetime=departure_datetime,
                                           arrival_datetime=arrival_datetime, price=price,
                                           status=status, origin=origin, destination=destination,
                                           airline_name=need_airline, terminal=need_terminal, gate=need_gate,
                                           runway=need_runway)
            save_flight(flight)
            return JsonResponse({
                'message': '恭喜您，添加成功！'
            })
        except IntegrityError as e:
            return JsonResponse({'message': str(e)})
        finally:
            print_flight()


# 删除航班信息
class DeleteFlightViews(View):
    def delete(self, request):
        json_str = request.body
        data = json.loads(json_str)
        flight_number = data.get('flight_number')

        try:
            flight = Flight.objects.get(flight_number=flight_number)
        except Exception as e:
            return JsonResponse({
                'code': 10307, 'error': '删除航班信息失败'
            })

        flight.delete()
        return JsonResponse({
            'code': 200, 'message': '删除航班信息成功'
        })


# 调整航班价格
class UpdateFlightPriceViews(View):
    def put(self, request):
        json_str = request.body
        data = json.loads(json_str)
        flight_number = data.get('flight_number')
        price = data.get('price')

        try:
            flight = Flight.objects.get(flight_number=flight_number)
        except Exception as e:
            return JsonResponse({
                'code': 10308, 'error': '更新航班价格'
            })

        flight.price = price
        flight.save()
        return JsonResponse({
            'code': 200, 'message': '调整航班价格成功'
        })


class BuyTicketsViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        flight_number = data.get('flight_number')
        try:
            old_flight = Flight.objects.get(flight_number=flight_number)
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
            old_passenger = Passenger.objects.get(identification=identification)
        except Exception as e:
            return JsonResponse({
                'code': 10402, 'error': '不存在该旅客，是否已注册？'
            })
        try:
            ticket = Ticket.objects.create(passenger=old_passenger, departure_datetime=departure_datetime,
                                           arrival_datetime=arrival_datetime,
                                           destination=destination, origin=origin, status=status,
                                           airline_name=airline_name, terminal=terminal, gate=gate)
            ticket.save()
            return JsonResponse({'message': '购票成功，请支付'})
        except Exception as e:
            return JsonResponse({
                'message': str(e)
            })
        # TODO：后面实现支付功能，并将状态改为已支付，支付失败则删除信息


class SearchInformationViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        origin = data.get('origin')
        destination = data.get('destination')
        flight_list = Flight.objects.filter(origin=origin, destination=destination)  # 查询对应航班
        dict1 = {}
        for i in flight_list:
            if i.departure_datetime > datetime.datetime.now():  # 如果航班现在没有起飞，则传回该航班
                dict1[i.flight_number] = {'flight_number': i.flight_number, 'airline_name': i.airline_name.name,
                                          'origin': i.origin, 'destination': i.destination,
                                          'departure_datetime': i.departure_datetime,
                                          'arrival_datetime': i.arrival_datetime,
                                          'price': i.price, 'terminal': i.terminal.terminal_number,
                                          'gate': i.gate.gate_number, 'runway': i.runway.runway_number}

        return JsonResponse(dict1)


class SearchTicketViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        identification = data.get('identification')
        try:
            passenger = Passenger.objects.get(identification=identification)
        except Exception as e:
            return JsonResponse({
                'code': '10501',
                'error': '不存在该旅客'
            })
        ticket_list = Ticket.objects.filter(passenger=passenger)
        dict1 = {}
        for i in ticket_list:
            if i.departure_datetime > datetime.datetime.now():  # 如果航班现在没有起飞，则返回该机票
                dict1[i.ticket_number_random] = {
                    'ticket_number_random': i.ticket_number_random,
                    'origin': i.origin,
                    'destination': i.destination,
                    'airline_name': i.airline_name.name,
                    'departure_datetime': i.departure_datetime,
                    'arrival_datetime': i.arrival_datetime,
                    'terminal': i.terminal.terminal_number,
                    'gate': i.gate.gate_number,
                    'passenger': i.passenger.identification,
                    'name': i.passenger.name
                }
        return JsonResponse(dict1)


class AddLuggageViews(View):
    def convert_weight_string(self, weight_string):
        try:
            weight = float(weight_string)
            # 限制小数位数为2位，可根据需求进行调整
            formatted_weight = round(weight, 2)
            return formatted_weight
        except ValueError:
            return None

    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        luggage_number = data.get('luggage_number')
        weight = self.convert_weight_string(data.get('weight'))
        print(weight)
        if weight > 10.00:
            return JsonResponse({
                'code': '10502',
                'error': '行李超重'
            })
        status = '等待运送'
        position = 'Airport'
        identification = data.get('identification')
        try:
            passenger = Passenger.objects.get(identification=identification)
        except Exception as e:
            return JsonResponse({
                'code': '10501',
                'error': '不存在该旅客'
            })
        try:
            luggage = Luggage.objects.create(luggage_number=luggage_number, weight=weight, position=position,
                                             status=status, passenger=passenger)
            luggage.save()
            return JsonResponse({
                'message': '添加成功'
            })
        except Exception as e:
            return JsonResponse({
                'message': str(e)
            })


# 旅客追踪自己的行李
class TrackLuggage(View):
    def get(self, request):
        json_str = request.body
        data = json.loads(json_str)
        identification = data.get('identification')

        try:
            passenger = Passenger.objects.get(identification=identification)
        except Exception as e:
            return JsonResponse({
                'code': 10502, 'message': '未找到该旅客'
            })

        luggage_list = Luggage.objects.filter(identification=identification)
        dict1 = {}
        for i in luggage_list:
            dict1[i.luggage_number] = {
                'luggage_number': i.luggage_number,
                'weight': i.weight,
                'status': i.status,
                'position': i.position,
                'passenger_id': i.passenger.identification
            }
        return JsonResponse({
            'code': 200,
            'message': '成功找到您的行李信息',
            'data': dict1
        })


# 查询当前可用的停车位
class SearchParking(View):
    def get(self):
        all_parking = Parking.objects.all()
        dict1 = {}
        for i in all_parking:
            if i.status == '空闲':
                dict1[i.parking_number] = {
                    'parking_number': i.parking_number,
                    'status': i.status
                }
        if not dict1:
            return JsonResponse({
                'code': 10601, 'message': '车位已满'
            })
        else:
            return JsonResponse({
                'code': 200,
                'message': '成功查询到当前空闲车位',
                'data': dict1
            })


# 预约停车位
class ReserveParking(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        parking_number = data.get('parking_number')
        passenger_id = data.get('passenger_id')
        start_time = data.get('start_time')

        try:
            parking = Parking.objects.get(parking_number=parking_number)
        except Exception as e:
            return JsonResponse({
                'code': 10602,
                'error': '未找到该停车位，请确认该停车位是否空闲'
            })

        parking.status = '占用'
        parking.passenger_id = passenger_id
        parking.duration = "None"
        parking.save()

        return JsonResponse({
            'code': 200,
            'message': '车位预约成功',
        })
