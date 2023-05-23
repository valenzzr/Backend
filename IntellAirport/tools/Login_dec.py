import jwt
from django.http import JsonResponse
from django.conf import settings
from airport.models import Passenger


def logging_check(func):
    def wrap(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({
                'code': 403, 'error': '用户未登录'
            })

        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            print('jwt decode error is %s' % e)
            return JsonResponse({
                'code': 403, 'error': '请登录'
            })

        username = res['username']
        user = Passenger.objects.get(username=username)
        request.nowuser = user
        return func(request, *args, **kwargs)

    return wrap
