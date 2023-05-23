from django.urls import path

from . import views
from .views import *

app_name = 'airport'

urlpatterns = [
    # 127.0.0.1:8000/api/register 用户注册
    path('register/', RegisterViews.as_view()),
    # 127.0.0.1:8000/api/login 用户登录
    path('login/', LoginViews.as_view()),
    # 127.0.0.1:8000/api/addFlight 添加航班信息
    path('addFlight/', AddFlightViews.as_view()),
    # 127.0.0.1:8000/api/deleteFlight 删除航班信息
    path('deleteFlight/', DeleteFlightViews.as_view()),
    # 127.0.0.1:8000/api/updatePrice 更新航班价格
    path('updatePrice/', UpdateFlightPriceViews.as_view()),

    path('buyticket/', BuyTicketsViews.as_view()),
    path('searchinformation/', SearchInformationViews.as_view()),
    path('searchticket/', SearchTicketViews.as_view()),
    # 127.0.0.1:8000/api/addLuggage 添加行李
    path('addLuggage/',AddLuggageViews.as_view()),
]
