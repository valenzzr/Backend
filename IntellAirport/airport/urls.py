from django.urls import path

from . import views
from .views import *

app_name = 'airport'

urlpatterns = [

    # 用户系统：
    # 127.0.0.1:8000/api/register 用户注册
    path('register/', RegisterViews.as_view()),
    # 127.0.0.1:8000/api/login 用户登录
    path('login/', LoginViews.as_view()),
    # 127.0.0.1:8000/api/updateInfo 修改个人信息
    path('updateInfo/', UpdateInfoViews.as_view()),
    # 127.0.0.1:8000/api/uploadAvatar 上传头像
    path('uploadAvatar/', views.UploadImage),

    # 航班信息：
    # 127.0.0.1:8000/api/addFlight/ 添加航班信息
    path('addFlight/', AddFlightViews.as_view()),
    # 127.0.0.1:8000/api/deleteFlight/ 删除航班信息
    path('deleteFlight/', DeleteFlightViews.as_view()),
    # 127.0.0.1:8000/api/updatePrice/ 更新航班价格
    path('updatePrice/', UpdateFlightPriceViews.as_view()),
    # 127.0.0.1:8000/api/searchFlightInfo/ 查询航班信息
    path('searchFlightInfo/', SearchFlightInfoViews.as_view()),

    # 旅客信息
    # 127.0.0.1：8000/api/buyTicket/ 旅客购买机票
    path('buyticket/', BuyTicketsViews.as_view()),
    # 127.0.0.1:8000/api/searchTicket/ 查询订票信息并生成电子机票
    path('searchTicket/', SearchTicketViews.as_view()),
    # 127.0.0.1:8000/api/addLuggage/ 添加行李
    path('addLuggage/', AddLuggageViews.as_view()),
    # 127.0.0.1:8000/api/trackLuggage/ 旅客追踪自己的行李
    path('trackLuggage/', TrackLuggageViews.as_view()),

    # 报修功能

    # 表单管理

    # 商家入驻
    # 127.0.0.1:8000/api/merchantIn/ 商家申请入驻
    path('merchantIn/', MerchantInViews.as_view()),
    # 127.0.0.1:8000/api/storesIn/ 导入商品
    path('storesIn/', StoresInViews.as_view()),
    # 127.0.0.1:8000/api/saleStore/ 商店销售商品
    path('saleStore/', SaleStoreViews.as_view()),

    # 停车管理
    # 127.0.0.1:8000/api/searchParking 查询当前可用停车位
    path('searchParking/', SearchParkingViews.as_view()),
    # 127.0.0.1:8000/api/reserveParking 预约停车位
    path('reserveParking/', ReserveParkingViews.as_view()),

]
