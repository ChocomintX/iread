import json

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, JsonResponse
from app.utils.return_code import *

NOT_REQUIRED_LOGIN_PATH = ["/user/login/", "/user/register/"]


class LoginMiddleware(MiddlewareMixin):
    """验证登录中间件"""

    def process_request(self, request):
        print(request.POST)

        # print(request.body)
        return
        if request.path_info in NOT_REQUIRED_LOGIN_PATH:
            return
        print(request.POST)
        cookie = request.POST.get("cookie")
        info = request.session.get(cookie)
        print(cookie, info, request.session)
        if info is None:
            return JsonResponse({
                "code": TIMEOUT_CODE,
                "msg": "登录已过期！"
            })

    def process_response(self, request, response):
        print("exit")
        return response
