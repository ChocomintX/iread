from django.http import HttpResponse, response, JsonResponse
import app.service.userService as userService
from app.utils.return_code import SUCCESS_CODE, ERROR_CODE
from django_redis import get_redis_connection
from django.core.cache import cache
import app.utils.kkmh as kkmh
import app.utils.bookSpider as bookSpider


# 用户操作的所有接口

def test(request):
    # 从连接池中拿到连接
    # conn = get_redis_connection()
    # name = str(conn.get('age'), encoding='utf-8')

    # kkmh.download()
    bookSpider.download()

    return HttpResponse("ok")


def login(request):
    try:
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        # 登陆成功则将信息加入session
        res = userService.login(username, password)
        if res.get("code") == 0:
            # cookie = request.session.session_key
            # res["cookie"] = cookie
            # request.session[cookie] = res.get("data")
            res.get("data").pop("password")
        return JsonResponse(res)
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def register(request):
    try:
        return JsonResponse(userService.register(request.POST))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def active(request):
    try:
        return HttpResponse(userService.active(request.GET))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def update(request):
    try:
        return JsonResponse(userService.update(request.POST))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def bind_phone(request):
    try:
        data = request.POST
        username = data.get("username")
        phone_number = data.get("phone_number")
        return JsonResponse(userService.update({
            "username": username,
            "phone_number": phone_number
        }))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def bind_email(request):
    try:
        data = request.POST
        username = data.get("username")
        email = data.get("email")
        return JsonResponse(userService.update({
            "username": username,
            "email": email
        }))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def change_password(request):
    try:
        data = request.POST
        username = data.get("username")
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        return JsonResponse(userService.change_password(username, old_password, new_password))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })
