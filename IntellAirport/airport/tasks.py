from celery import shared_task
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from .models import Flight, Ticket

email_send = False


@shared_task
def test_add(x, y):
    return x + y


@shared_task
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


def send_flight_reminder_email(ticket):
    # 构建邮件内容
    subject = 'Flight Reminder'
    message = f'Dear {ticket.passenger.name}, your flight {ticket.flight_number} is departing in 2 hours.'
    from_email = '949011578@qq.com'
    recipient_list = [ticket.passenger.email]
    print(ticket.passenger.email)
    # 发送邮件
    send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)
    print("Sending flight reminder email to", ticket.passenger.email)


@shared_task
def check_flight_departure():
    global email_send
    flights = Flight.objects.all()
    print(flights)
    for flight in flights:
        time_difference = flight.departure_datetime - timezone.now()
        hours_remaining = time_difference.total_seconds()  # // 3600
        print(flight.departure_datetime, timezone.now(), time_difference, hours_remaining, email_send)
        if 7190 <= hours_remaining <= 7210 and not email_send:
            # if hours_remaining == 2 and not email_send:
            tickets = Ticket.objects.filter(flight_number=flight.flight_number)
            for ticket in tickets:
                send_flight_reminder_email(ticket)
            email_send = True
            break
    return "Flight departure check completed"  # 添加返回值
