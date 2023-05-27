from apscheduler.schedulers.background import BackgroundScheduler
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore, register_job

from .models import Flight, Ticket

email_send = False


# @shared_task
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
    subject = '临近起飞通知'
    if ticket.airline_name_id == 'CZ':
        airline_name = '东方航空'
    elif ticket.airline_name_id == 'MU':
        airline_name = '南方航空'
    message = f'    尊敬的{ticket.passenger.name}乘客，感谢您选择我们的航空公司。我们提醒您，您的航班{ticket.flight.flight_number}将在两小时后起飞。为了确保您的旅行顺利进行，请您务必在起飞前两小时完成在线值机。通过在线值机，您可以选择座位、打印登机牌，并且节省排队的时间。请您访问我们的官方网站或使用我们的手机应用程序，点击值机选项，并按照提示完成值机流程。如果您需要任何帮助或有任何疑问，请随时联系我们的客户服务团队。再次感谢您选择我们的航空公司，祝您旅途愉快！最好的祝福，{airline_name}团队 '
    # message = f'Dear {ticket.passenger.name}, your flight {ticket.flight_number} is departing in 2 hours.'
    from_email = '949011578@qq.com'
    recipient_list = [ticket.passenger.email]
    print(ticket.passenger.email)
    # 发送邮件
    send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)
    print("Sending flight reminder email to", ticket.passenger.email)


# 起飞前2小时定时给需要登机的旅客发送邮件
# @shared_task
def check_flight_departure():
    # global email_send
    flights = Flight.objects.all()
    print(flights)
    for flight in flights:
        time_difference = flight.departure_datetime - timezone.now()
        hours_remaining = time_difference.total_seconds()  # // 3600
        print(flight.departure_datetime, timezone.now(), time_difference, hours_remaining, email_send)
        if 7191 <= hours_remaining <= 7209 and not email_send:
            # if hours_remaining == 2 and not email_send:
            tickets = Ticket.objects.filter(flight_number=flight.flight_number)
            for ticket in tickets:
                send_flight_reminder_email(ticket)
            # email_send = True
            # break
    return "Flight departure check completed"  # 添加返回值


try:
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)  # timezone是用来设置时区的
    scheduler.add_jobstore(DjangoJobStore(), "default")


    @register_job(scheduler, 'interval', seconds=5, id="text")  # 每隔5s执行一次
    def text():
        print("我是apscheduler定时任务")
        check_flight_departure()


    # register_events(scheduler)	之前版本的django-apschuler需要注册，现在不需要了
    scheduler.start()
    print("任务启动!")
except Exception as e:
    print("定时服务错误,已关闭:%s" % e)
    # 有错误就停止定时器
    scheduler.shutdown()
