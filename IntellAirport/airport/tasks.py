from django.core.mail import send_mail
from django.http import JsonResponse
from IntellAirport.celery import app
from django.utils import timezone
from .models import Flight


@app.task
def send_email_celery(request, email, subject, message):
    # # 邮件主题
    # subject = "ACF activate"
    # # 邮件内容
    # message = "Hello"
    # 发件人
    from_email = "949011578@qq.com"
    # 收件人，可以是多个，以列表的形式存储
    # recipient_list = ["152xxxx7756@sina.cn", "iino-miko@outlook.com", ]
    recipient_list = [email]
    send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)
    return JsonResponse({
        'code': 200,
        'message': '邮件发送成功!'
    })


def send_flight_reminder_email(flight):
    # 构建邮件内容
    subject = 'Flight Reminder'
    message = f'Dear {flight.passenger.name}, your flight {flight.flight_number} is departing in 2 hours.'
    from_email = 'your_email@example.com'
    to_email = flight.passenger.email

    # 发送邮件
    send_mail(subject, message, from_email, [to_email])


@app.task
def check_flight_departure():
    flights = Flight.objects.all()
    for flight in flights:
        time_difference = flight.departure_datetime - timezone.now()
        hours_remaining = time_difference.total_seconds() // 3600
        if hours_remaining == 2:
            send_flight_reminder_email(flight)

