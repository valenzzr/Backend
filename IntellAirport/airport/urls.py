from django.urls import path
from django.urls import re_path as url
from . import views
from .views import *

from django.contrib import admin

app_name = 'airport'

urlpatterns = [
    # 用户系统：
    # 127.0.0.1:8000/api/register/ 用户注册
    path('register/', RegisterViews.as_view()),
    # 127.0.0.1:8000/api/login/ 用户登录
    path('login/', LoginViews.as_view()),
    # 127.0.0.1:8000/api/updateInfo/ 修改个人信息
    path('updateInfo/', UpdateInfoViews.as_view()),
    # 127.0.0.1:8000/api/uploadAvatar/ 上传头像
    path('uploadAvatar/', views.UploadImage),

    # 航班信息：
    # 127.0.0.1:8000/api/addFlight/ 添加航班信息
    path('addFlight/', AddFlightViews.as_view()),
    # 127.0.0.1:8000/api/deleteFlight/ 删除航班信息
    path('deleteFlight/', DeleteFlightViews.as_view()),
    # 127.0.0.1:8000/api/updatePrice/ 更新航班价格
    path('updatePrice/', UpdateFlightPriceViews.as_view()),

    # 旅客信息
    # 127.0.0.1:8000/api/buyTicket/ 购买机票
    path('buyTicket/', BuyTicketsViews.as_view()),
    # 127.0.0.1:8000/api/searchInformation/ 查询航班信息
    path('searchInformation/', SearchFlightInfoViews.as_view()),
    # 127.0.0.1:8000/api/searchTicket 查询订票信息，并生成电子机票
    path('searchTicket/', SearchTicketViews.as_view()),
    # 127.0.0.1:8000/api/addLuggage/ 添加行李
    path('addLuggage/', AddLuggageViews.as_view()),
    # 127.0.0.1:8000/api/trackLuggage/ 旅客追踪自己的行李
    path('trackLuggage/', TrackLuggageViews.as_view()),

    # 报修功能
    # 127.0.0.1:8000/api/repair/ 报修设备并附带图片
    path('repair/', RepairViews.as_view()),
    # 127.0.0.1:8000/api/confirmRepair/ 等待管理员确认保修，get方法获取需要管员确认的报修，POST返回确认的报修方式
    path('confirmRepair/', ConfirmRepairViews.as_view()),


    # 127.0.0.1:8000/api/searchFlightTime/ 查看航班时刻表（返回当前还未起飞的航班信息）
    path('searchFlightTime/', SearchFlightTimeViews.as_view()),
    # 127.0.0.1:8000/api/checkArray/ 查看当前可审批的航班
    path('checkArray/', views.checkArray),
    # 127.0.0.1:8000/api/judgeFlight/ 审批航班
    path('judgeFlight/', views.judgeFlight),
    # 127.0.0.1:8000/api/importFlightInfo/ 批量导入航班信息
    # path('importFlightInfo/', views.import_flight_info),

    # 商家入驻
    # 127.0.0.1:8000/api/merchantIn/ 商家申请入驻
    path('merchantIn/', MerchantInViews.as_view()),
    # 127.0.0.1：8000/api/queryMerchants/ 查询商家信息
    path('queryMerchants/', QueryMerchantsViews.as_view()),
    # 127.0.0.1:8000/api/storesIn/ 导入商品
    path('storesIn/', StoresInViews.as_view()),
    # 127.0.0.1:8000/api/queryStores/ 查询商品信息
    path('queryStores/', QueryStoresViews.as_view()),
    # 127.0.0.1:8000/api/saleStore/ 商店销售商品
    path('saleStore/', SaleStoreViews.as_view()),
    # 127.0.0.1:8000/api/storesInShop/ 商店显示商品
    path('storesInShop/', StoresInShopViews.as_view()),
    # 127.0.0.1:8000/api/PayCar/ 支付车位
    path('payCar/', payCarViews.as_view()),

    # 停车管理
    # 127.0.0.1:8000/api/searchParking/ 查询当前可用停车位
    path('searchParking/', SearchParkingViews.as_view()),
    # 127.0.0.1:8000/api/reserveParking/ 预约停车位
    path('reserveParking/', ReserveParkingViews.as_view()),

    # 表单管理
    # 127.0.0.1:8000/api/printReport/
    path('printReport/', PrintReportViews.as_view()),

    # 客服功能
    # 127.0.0.1:8000/api/robot/
    path('robot/', RobotViews.as_view()),

    path('pay/', PaymentStatusView.as_view()),
    path('pay2/', PaymentStatus2View.as_view()),
]
