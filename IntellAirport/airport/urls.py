from django.urls import path

from . import views
from .views import *

app_name = 'airport'

urlpatterns = [
    path('register/', RegisterViews.as_view()),
    path('login/', LoginViews.as_view())
]
