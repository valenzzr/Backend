from celery import Celery
import os

from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IntellAirport.settings')

app = Celery('IntellAirport')

app.conf.update(
    broker_url='redis://127.0.0.1:6379/1'
)

app.conf.timezone = 'Asia/Shanghai'      # app.conf是整个celery的配置信息
# 是否使用UTC时间
app.conf.enable_utc = False

app.conf.beat_schedule = {
    'check_flight_departure': {
        'task': 'airport.tasks.check_flight_departure',
        'schedule': 10,
    },
}

app.autodiscover_tasks(settings.INSTALLED_APPS)
