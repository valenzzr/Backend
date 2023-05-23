from django.urls import path

from . import views
from .views import *

app_name = 'airport'

urlpatterns = [
    path('register/', RegisterViews.as_view()),
    path('login/', LoginViews.as_view()),
    path('addflight/', AddFlightViews.as_view()),
    path('buyticket/', BuyTicketsViews.as_view()),
    path('searchinformation/', SearchInformationViews.as_view()),
    path('searchticket/', SearchTicketViews.as_view()),
]
