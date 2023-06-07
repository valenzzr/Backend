import base64
import codecs
import json
import time
import datetime
import os
import jwt
from decimal import Decimal
from alipay import AliPay
from django.core.mail import send_mail
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render
from django.http import *
from airport.models import *
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from tools.Login_dec import logging_check
from .tasks import send_email_celery
import hashlib

# Create your views here.
flight_arr = []

credit_card = [{'card_number': '54387609', 'password': 'asdfg', 'money': 200.00},
               {'card_number': '87651093', 'password': 'qwert', 'money': 109000.02},
               {'card_number': '76452983', 'password': 'zxcvb', 'money': 230000.03}]


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
    recipient_list = ["iino-miko@outlook.com", ]
    send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)
    return JsonResponse({
        'code': 200,
        'message': '邮件发送成功!'
    })
    # return HttpResponse("Send email success")


def save_flight(flight):
    flight_arr.append(flight)


def print_flight():
    for flight in flight_arr:
        print(flight)


import requests


import random

messages = ["Hello!", "How are you?", "Good morning!", "Have a nice day!"]

def get_random_message(messages):
    return random.choice(messages)

random_message = get_random_message(messages)
print(random_message)

def get_random_message(messages):
    return random.choice(messages)




class RobotViews(View):
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        query = json_obj.get('query')


        response_dict = {
                "您好": "你好，我是百度机器人。",
                "你叫什么名字": "我是百度机器人。",
                "今天天气如何": "抱歉，我无法提供天气信息。",
                "如何购买机票": "点击购买机票按钮购买机票"
        }       # 添加更多的键值对，根据需要进行回复


        if query in response_dict:
            return JsonResponse({'msg' : response_dict[query]})
        else:
            return JsonResponse({'msg' : '对不起，我无法理解您的请求。'})



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
            subject = '注册成功邮件提示'
            message = '感谢您的注册，您已注册成功!'
            send_email_celery(request, email, subject, message)
            return JsonResponse({
                'code': 200,
                'message': '恭喜您，注册成功！'
            })
        except IntegrityError as e:
            return JsonResponse({'message': str(e)})


# 旅客登录功能
class LoginViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        user_priority = data.get('who')
        name = data.get('name')
        username = data.get('username')
        password = data.get('password')

        if user_priority == 'passenger':
            try:
                old_passenger = Passenger.objects.get(username=username)
            except Exception as e:
                return JsonResponse({
                    'code': 10201, 'error': '用户名或密码错误'
                })

            p_m = hashlib.md5()
            p_m.update(password.encode())
            if p_m.hexdigest() != old_passenger.password:
                return JsonResponse({
                    'code': 10202, 'error': '用户名或密码错误'
                })

            #   记录会话状态
            #   为旅客生成Token
            token = make_token(username)
            return JsonResponse({
                'message': '登录成功', 'username': username, 'data': {'token': token}, 'msg': old_passenger.message
            })

        elif user_priority == 'manager':
            try:
                old_manager = Manager.objects.get(username=username, name=name)
            except Exception as e:
                return JsonResponse({
                    'code': 10201, 'error': '用户名或密码错误'
                })

            if password != old_manager.password:
                return JsonResponse({
                    'code': 10202, 'error': '用户名或密码错误'
                })
            name = old_manager.name
        elif user_priority == 'staff':
            try:
                old_staff = Staff.objects.get(username=username, password=password)
            except Exception as e:
                return JsonResponse({
                    'code': 10201, 'error': '用户名或密码错误'
                })

            if password != old_staff.password:
                return JsonResponse({
                    'code': 10202, 'error': '用户名或密码错误'
                })
            name = old_staff.name
        # 记录会话状态
        # 为manager和staff生成token
        token = make_token(username)
        return JsonResponse({
            'message': '登录成功', 'username': username, 'name': name, 'data': {'token': token}
        })


# 更新用户信息
class UpdateInfoViews(View):
    @method_decorator(logging_check)
    def put(self, request):
        json_str = request.body
        data = json.loads(json_str)

        user = request.myuser

        phone_number = data.get('phone_number')
        email = data.get('email')
        password = data.get('password')
        print(phone_number, email, password)
        if phone_number:
            user.phone_number = phone_number
        if email:
            user.email = email
        if password:
            # 若是更新密码，仍需要先加密
            p_m = hashlib.md5()
            p_m.update(password.encode())
            user.password = p_m.hexdigest()

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
        if flight.status != 'addSucceeded':
            return JsonResponse({
                'code': 10309, 'error': '航班未导入'
            })
        flight.price = price
        flight.save()
        return JsonResponse({
            'code': 200, 'message': '调整航班价格成功'
        })


class payCarViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        parking_number = data.get('parking_number')
        try:
            parking = Parking.objects.get(parking_number=parking_number)
        except Exception as e:
            return JsonResponse({
                'code': 10401, 'error': '不存在该停车位,重新选择'
            })
        duration = datetime.datetime.now() - parking.start_time
        fee = duration * 10
        identification = data.get('identification')
        try:
            old_passenger = Passenger.objects.get(identification=identification)
        except Exception as e:
            return JsonResponse({
                'code': 10402, 'error': '不存在该旅客，是否已注册？'
            })
        try:

            return JsonResponse({'message': '请支付停车位',
                                 'parking_number': parking_number,
                                 'fee': fee, }
                                )

        except Exception as e:
            return JsonResponse({
                'message': str(e)
            })


# 旅客购买机票
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
        if old_flight.status != 'addSucceeded':
            return JsonResponse({
                'code': 10402, 'error': '航班未导入'
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
                                           arrival_datetime=arrival_datetime, flight_number_id=flight_number,
                                           destination=destination, origin=origin, status=status,
                                           airline_name=airline_name, terminal=terminal, gate=gate)
            ticket.save()
        except Exception as e:
            try:
                ticket = Ticket.objects.get(passenger = old_passenger)
            except Exception as e:
                return JsonResponse({
                    'code': 10405, 'error': '旅客只能买一张票！'
                })
            return JsonResponse({'message': '购票成功，请支付',
                                 'ticket_no': ticket.ticket_number_random,
                                 'passenger': old_passenger.identification,
                                 'departure_datetime': departure_datetime,
                                 'arrival_datetime': arrival_datetime,
                                 'destination': destination,
                                 'origin': origin,
                                 'price': old_flight.price,
                                 'runway': old_flight.runway.runway_number,
                                 'airline_name': airline_name.name,
                                 'terminal': terminal.terminal_number,
                                 'gate': gate.gate_number})




# 查询航班信息
class SearchFlightInfoViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        origin = data.get('origin')
        destination = data.get('destination')
        flight_list = Flight.objects.filter(origin=origin, destination=destination)  # 查询对应航班
        dict1 = {}
        for i in flight_list:
            if i.status != 'addSucceeded':
                continue
            if i.departure_datetime > datetime.datetime.now():  # 如果航班现在没有起飞，则传回该航班
                dict1[i.flight_number] = {'flight_number': i.flight_number, 'airline_name': i.airline_name.name,
                                          'origin': i.origin, 'destination': i.destination,
                                          'departure_datetime': i.departure_datetime,
                                          'arrival_datetime': i.arrival_datetime,
                                          'price': i.price, 'terminal': i.terminal.terminal_number,
                                          'gate': i.gate.gate_number, 'runway': i.runway.runway_number}

        return JsonResponse(dict1)


# 查询订票信息，并生成电子机票
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


# 旅客添加行李
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
            luggage = Luggage.objects.create(weight=weight, position=position,
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
class TrackLuggageViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        identification = data.get('identification')

        try:
            passenger = Passenger.objects.get(identification=identification)
        except Exception as e:
            return JsonResponse({
                'code': 10502, 'message': '未找到该旅客'
            })

        tickets = Ticket.objects.filter(passenger_id=identification)

        if not tickets:
            return JsonResponse({
                'code': 10503, 'message': '该旅客未买票'
            })

        thirty_minutes = datetime.timedelta(minutes=30)
        for ticket in tickets:
            if ticket.arrival_datetime + thirty_minutes <= datetime.datetime.now():
                return JsonResponse({
                    'code': 10504, 'message': '飞机落地已超过30min'
                })

        luggage_list = Luggage.objects.filter(passenger_id=identification)
        dict1 = {}
        for i in luggage_list:
            dict1[i.luggage_number] = {
                'luggage_number': i.luggage_number,
                'weight': i.weight,
                'status': i.status,
                'position': i.position,
                'passenger_id': i.passenger.identification
            }
        return JsonResponse(dict1)


# 查询当前可用的停车位
class SearchParkingViews(View):
    def get(self, request):
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
            return JsonResponse(dict1)


# 预约停车位
class ReserveParkingViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        parking_number = data.get('parking_number')
        username = data.get('username')
        try:
            passenger = Passenger.objects.get(username=username)
        except Exception as e:
            return JsonResponse({'code': 10603,'error': '旅客不存在'})
        passenger_id = passenger.identification

        try:
            parking = Parking.objects.get(parking_number=parking_number)
        except Exception as e:
            return JsonResponse({
                'code': 10602,
                'error': '未找到该停车位，请确认该停车位是否空闲'
            })
        if parking.status == '占用':
            return JsonResponse({
                'code': 10602,
                'error': '未找到该停车位，请确认该停车位是否空闲'
            })
        parking.status = '占用'
        parking.passenger_id = passenger_id
        parking.start_time = datetime.datetime.now()
        parking.save()

        return JsonResponse({
            'code': 200,
            'message': '车位预约成功',
        })


# 报修设备和设施(附带图片)
class RepairViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        dev_id = data.get('dev_id')
        dev_name = data.get('dev_name')
        # dev_image = request.FILES['devices']
        status = 'Waiting repair'
        try:
            dev = Device.objects.create(dev_id=dev_id, dev_name=dev_name, status=status)
        except Exception as e:
            return JsonResponse({
                'code': 10903,
                'error': 'failed create device!'
            })
        dev.save()
        return JsonResponse({
            'message': '添加成功'
        })


# 等待管理员审批
class ConfirmRepairViews(View):
    def get(self, request):
        dev_list = Device.objects.filter(status='Waiting repair')
        message = {}
        for i in dev_list:
            message[i.dev_id] = {'dev_id': i.dev_id, 'dev_name': i.dev_name}
        return JsonResponse(message)

    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        dev_id = data.get('dev_id')
        try:
            dev = Device.objects.get(dev_id=dev_id)
        except Exception as e:
            return JsonResponse({
                'code': 10701,
                'error': '不存在该设备的报修请求，请重新审批'
            })
        dev.status = 'Repairing'
        dev.save()
        return JsonResponse({
            'message': '审批成功'
        })


# 商家申请入驻
class MerchantInViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        shop_id = data.get('id')
        shop_name = data.get('name')
        shop_contact_number = data.get('contact_number')

        try:
            shop = Shop.objects.create(id=shop_id, name=shop_name, contact_number=shop_contact_number)
        except Exception as e:
            return JsonResponse({
                'code': 10701,
                'error': '商家入驻失败，请重新申请!'
            })

        shop.save()
        return JsonResponse({
            'code': 200,
            'message': '商家已经成功入驻，快来店里逛逛吧!'
        })


# 查询所有商家
class QueryMerchantsViews(View):
    def get(self, request):
        merchants = Shop.objects.all()
        if not merchants:
            return JsonResponse({
                'code': 10702,
                'error': '当前没有入驻的商家'
            })

        dict1 = {}

        for merchant in merchants:
            dict1[merchant.id] = {
                'id': merchant.id,
                'name': merchant.name,
                'contact_number': merchant.contact_number
            }

        return JsonResponse(dict1)


# 上传商品图片
def stores_image(request, store_id, shop_id):
    if request.methode != 'POST':
        return JsonResponse({
            'code': 10900,
            'error': 'Please use POST'
        })

    store_image = request.FILES.get('store')
    try:
        store = Store.objects.get(store_id=store_id,shop_id_id=shop_id)
    except Exception as e:
        return JsonResponse({
            'code': 10902,
            'error': 'failed upload!'
        })
    store.store_image = store_image
    return store_image


# 导入商品
class StoresInViews(View):
    def post(self, request):
        store_id = request.POST.get('store_id')
        store_name = request.POST.get('store_name')
        store_image = request.FILES['stores']
        shop_id = request.POST.get('shop_id')

        try:
            # store_image_data = store_image.read().decode('utf-8')
            store = Store.objects.create(store_id=store_id, store_name=store_name, shop_id_id=shop_id,
                                         store_image=store_image)
        except Exception as e:
            print(e)
            return JsonResponse({
                'code': 10703,
                'error': '商品导入失败'
            })

        store.save()

        return JsonResponse({
            'code': 200,
            'message': '商品导入成功'
        })


# 返回商店商品
class StoresInShopViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        shop_id = data.get('shop_id')
        try:
            shop = Shop.objects.get(id=shop_id)
        except Exception as e:
            return JsonResponse({
                'code': 10704,
                'error': '没有找到对应商店!'
            })

        stores = Store.objects.filter(shop_id_id=shop_id)
        if not stores:
            return JsonResponse({
                'code': 10705,
                'error': '当前商店空空如也!'
            })
        dict1 = {}
        for store in stores:
            image_filename = store.store_image.path  # 从数据库中获取相对地址的图片名称
            image_path = os.path.join(settings.MEDIA_ROOT, image_filename)

            with open(image_path, 'rb') as f:
                encoded_image = base64.b64encode(f.read()).decode('utf-8')

            dict1[store.store_id] = {
                'store_id': store.store_id,
                'store_name': store.store_name,
                'store_image': encoded_image,
                'shop_id': store.shop_id_id
            }

        return JsonResponse(dict1)


# 查询所有商品
class QueryStoresViews(View):
    def get(self, request):
        stores = Store.objects.all()
        if not stores:
            return JsonResponse({
                'code': 10705,
                'error': '当前还没有导入任何商品'
            })

        dict1 = {}

        for store in stores:
            dict1[store.id] = {
                'id': store.id,
                'store_id': store.store_id,
                'store_name': store.store_name,
                'shop_id': store.shop_id_id
            }

        return JsonResponse(dict1)


# 打印报表
class PrintReportViews(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        airline_name = data.get('airline_name')
        flight_all = []
        for flight in Flight.objects.all():
            if flight.status != 'addSucceeded':
                continue
            if flight.airline_name_id == airline_name:
                flight_all.append(flight)
        returns = {}
        for flight in flight_all:
            ticket_num = 0
            money = 0
            for ticket in Ticket.objects.all():
                if ticket.flight_number_id == flight.flight_number:
                    ticket_num = ticket_num + 1
                    money = money + flight.price
            returns[flight.flight_number] = {'flight_number': flight.flight_number,
                                             'airline': airline_name,
                                             'ticket_sold': ticket_num,
                                             'money': money}
        return JsonResponse(returns)


# 商店销售商品
class SaleStoreViews(View):
    # def get(self, request, shop_id):  # 返回商店所有商品信息

    def post(self, request):  # 购买商品
        json_str = request.body
        data = json.loads(json_str)
        passenger_name = data.get('passenger_name')
        store_name = data.get('store_name')
        shop_id = data.get('shop_id')
        store_id = data.get('store_id')

        # 取到要购买商品的旅客
        try:
            passenger = Passenger.objects.get(name=passenger_name)
        except Exception as e:
            return JsonResponse({
                'code': 10703,
                'error': '未找到该旅客'
            })

        passenger_identification = passenger.identification

        # 查找passenger所持有的票
        try:
            ticket = Ticket.objects.get(passenger_id=passenger_identification)
        except Exception as e:
            return JsonResponse({
                'code': 10704,
                'error': '该旅客还未买票，无法送货至指定登机口'
            })

        # 拿到航站楼号
        terminal_id = ticket.terminal.terminal_number
        # 拿到登机口号
        gate_id = ticket.gate.gate_number

        # 取到要购买的商品
        try:
            store = Store.objects.get(shop_id=shop_id, store_id=store_id, store_name=store_name)
        except Exception as e:
            return JsonResponse({
                'code': 10705,
                'error': '未找到到该商品'
            })

        result = {
            'code': 200,
            'message': '购买商品成功!',
            'store': {  # 返回商品信息
                'shop_id': store.shop_id,
                'store_id': store.store_id,
                'store_name': store.store_name,
                'store_image': store.store_image
            },
            'terminal_id': terminal_id,  # 返回旅客所在航站楼号
            'gate_id': gate_id  # 返回旅客所在登机口号
        }


# 查看航班时刻表（返回当前还未起飞的航班信息）
class SearchFlightTimeViews(View):
    def get(self, request):
        flights = Flight.objects.all()
        dict1 = {}
        for flight in flights:
            if flight.status != 'addSucceeded':
                continue
            if flight.departure_datetime > timezone.now():
                dict1[flight.flight_number] = {
                    'flight_number': flight.flight_number,
                    'flight.origin': flight.origin,
                    'flight.destination': flight.destination,
                    'departure_datetime': flight.departure_datetime,
                    'arrival_datetime': flight.arrival_datetime,
                    'price': flight.price,
                    'airline_name_id': flight.airline_name_id,
                    'gate_id': flight.gate_id,
                    'runway_id': flight.runway_id,
                    'terminal_id': flight.terminal_id
                }
        return JsonResponse(dict1)

    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        origin = data.get('origin')
        destination = data.get('destination')

        flights = Flight.objects.filter(origin=origin, destination=destination)

        if not flights:
            return JsonResponse({
                'code': 10803,
                'error': '您查询的地点之间还没有航班哦，换个试试吧'
            })

        dict1 = {}
        for flight in flights:
            if flight.departure_datetime > timezone.now():
                dict1[flight.flight_number] = {
                    'flight_number': flight.flight_number,
                    'departure_datetime': flight.departure_datetime,
                    'arrival_datetime': flight.arrival_datetime,
                    'price': flight.price,
                    'airline_name_id': flight.airline_name_id,
                    'gate_id': flight.gate_id,
                    'runway_id': flight.runway_id,
                    'terminal_id': flight.terminal_id
                }


# 查询所有可导入航班信息
def checkArray(request):
    if request.method != 'GET':
        return JsonResponse({
            'code': 10801,
            'error': 'Please use GET！'
        })

    if not flight_arr:
        return JsonResponse({
            'code': 10802,
            'message': '当前没有航班信息可以导入，请先添加航班信息'
        })

    dict1 = {}
    for flight in flight_arr:
        dict1[flight.flight_number] = {
            'flight_number': flight.flight_number,
            'flight.origin': flight.origin,
            'flight.destination': flight.destination,
            'departure_datetime': flight.departure_datetime,
            'arrival_datetime': flight.arrival_datetime,
            'price': flight.price,
            'status': flight.status,
            'airline_name_id': flight.airline_name_id,
            'gate_id': flight.gate_id,
            'runway_id': flight.runway_id,
            'terminal_id': flight.terminal_id
        }

    return JsonResponse(dict1)


# 通过可导入航班
def judgeFlight(request):
    if request.method != 'POST':
        return JsonResponse({
            'code': 10801,
            'error': 'Please use POST！'
        })

    json_str = request.body
    data = json.loads(json_str)
    op = data.get('op')
    flight_number = data.get('flight_number')

    try:
        if len(flight_arr) == 0:
            return JsonResponse({
                'code': 10802,
                'error': '未找到当前航班'
            })
        for flight in flight_arr:
            if flight.flight_number == flight_number:
                flight_arr.remove(flight)

    except Exception as e:
        return JsonResponse({
            'code': 10802,
            'error': '未找到当前航班'
        })
    flight = Flight.objects.get(flight_number=flight_number)
    if flight.status == 'addSucceeded':
        return JsonResponse({
            'code': 10804,
            'error': '已添加该航班'
        })
    if op == 1:  # 通过审批
        flight.status = 'addSucceeded'
        flight.save()
        return JsonResponse({
            'msg': 'OK'
        })
    elif op == 0:  # 拒绝审批
        flight.delete()
        return JsonResponse({
            'msg': 'NO'
        })
    else:
        return JsonResponse({
            'error': '10803'
        })


class PaymentStatusView(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        card_id = data.get('card_id')
        card_pwd = data.get('card_pwd')
        need_money = data.get('need_money')
        need_money = float(need_money)
        ticket_no = data.get('ticket_no')
        flag = 0
        for i in credit_card:
            if card_id == i['card_number']:
                flag = 1
                if card_pwd != i['password']:
                    return JsonResponse({
                        'code': 11001,
                        'error': '密码错误！'
                    })
                if need_money > i['money']:
                    return JsonResponse({
                        'code': 11002,
                        'error': '余额不足！'
                    })
                i['money'] = i['money'] - need_money
                print(i['money'])
        if flag == 0:
            return JsonResponse({
                'code': 11003,
                'error': '银行卡号不存在！'
            })

        try:
            ticket = Ticket.objects.get(ticket_number_random=ticket_no)
        except Exception as e:
            for i in credit_card:
                if card_id == i['card_number']:
                    i['money'] = i['money'] + need_money
            return JsonResponse({
                'code': 11004,
                'error': '机票不存在'
            })
        try:
            ticket.status = "已支付"
            ticket.save()
        except Exception as e:
            return JsonResponse({
                'code': 0, 'errmsg': 'ok'
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class PaymentStatus2View(View):
    def post(self, request):
        json_str = request.body
        data = json.loads(json_str)
        card_id = data.get('card_id')
        card_pwd = data.get('card_pwd')
        username = data.get('username')
        try:
            passenger = Passenger.objects.get(username=username)
        except Exception as e:
            return JsonResponse({'code': 10603,'error': '旅客不存在'})
        passenger_id = passenger.identification
        flag = 0
        try:
            parking = Parking.objects.get(passenger_id=passenger_id)
        except Exception as e:
            return JsonResponse({
                'code': 11004,
                'error': '支付车位不存在'
            })
        time_dif = datetime.datetime.now() - parking.start_time
        need_money = float(time_dif.total_seconds()/3600)*1000
        need_money = round(need_money,2)
        for i in credit_card:
            if card_id == i['card_number']:
                flag = 1
                if card_pwd != i['password']:
                    return JsonResponse({
                        'code': 11001,
                        'error': '密码错误！'
                    })
                if need_money > i['money']:
                    return JsonResponse({
                        'code': 11002,
                        'error': '余额不足！'
                    })
                i['money'] = i['money'] - need_money
                print(i['money'])
        if flag == 0:
            return JsonResponse({
                'code': 11003,
                'error': '银行卡号不存在！'
            })


        if parking.status == '空闲':
            for i in credit_card:
                if card_id == i['card_number']:
                    i['money'] = i['money'] + need_money
            return JsonResponse({
                'code': 11004,
                'error': '车位为空闲状态'
            })
        parking.status = "空闲"
        parking.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok','money': need_money})

