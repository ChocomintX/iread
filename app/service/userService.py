import json

import requests
from django.http import HttpResponse, response, JsonResponse
from app.models import User
from django.db.models import Q
from django.db import transaction
import app.utils.kkmh as kkmh
from app.utils.return_code import SUCCESS_CODE, ERROR_CODE
from app.utils.serilizers import *


def test(request):
    resp = dict()
    resp["images"] = kkmh.get_chapter_images("https://www.ykmh.com/manhua/DrSTONEshijiyuan/51454.html")
    return JsonResponse(resp)


def testchapter(request):
    resp = dict()
    # resp["images"] = kkmh.get_chapter_lists("http://www.ykmh.com/manhua/ReModelinggaizaorenzhizhan/")
    # resp["info"] = kkmh.get_manga_info("http://www.ykmh.com/manhua/ReModelinggaizaorenzhizhan/")
    resp["search"] = kkmh.search("女", 2)
    return JsonResponse(resp)


@transaction.atomic
def login(username, password):
    """验证登录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "登陆成功！"
    }

    user = User.objects.filter(Q(username=username) | Q(phone_number=username) | Q(email=username)).first()

    if user is None:
        res["code"] = ERROR_CODE
        res["msg"] = "用户不存在"
    elif user.password != password:
        res["code"] = ERROR_CODE
        res["msg"] = "密码错误"
    elif user.active_status == 0:
        res["code"] = ERROR_CODE
        res["msg"] = "用户未激活"
    else:
        res["data"] = UserSerialize(user).data
    return res


@transaction.atomic
def register(data):
    """用户注册"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "注册成功"
    }
    username = data.get("username")
    password = data.get("password")
    nickname = data.get("nickName")
    email = data.get("email")

    user = User.objects.filter(
        Q(username=username) | Q(phone_number=username) | Q(email=username) | Q(email=email)).first()
    if user is not None:
        res["code"] = ERROR_CODE
        res["msg"] = "用户名或邮箱已被注册"
    else:
        new_user = User(username=username, password=password, nickname=nickname, email=email,active_status=1)
        new_user.save()
        res["data"]=UserSerialize(new_user).data
    return res


@transaction.atomic
def update(data):
    """更新用户"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "更新成功"
    }
    username = data.get("username")
    password = data.get("password")
    nickname = data.get("nickname")
    email = data.get("email")
    phone_number = data.get("phone_number")
    active_status = data.get("active_status")

    user = User.objects.filter(username=username).first()
    user.username = username if username is not None else user.username
    user.password = password if password is not None else user.password
    user.nickname = nickname if nickname is not None else user.nickname
    user.email = email if email is not None else user.email
    user.phone_number = phone_number if phone_number is not None else user.phone_number
    user.active_status = active_status if active_status is not None else user.active_status

    user.save()
    return res


# @transaction.atomic
# def bind_phone(username, phone_number):
#     res = {
#         "code": "1",
#         "msg": "绑定成功"
#     }
#
#     user = User.objects.filter(username=username).first()
#     user.phone_number = phone_number
#     user.save()
#     return res
#
#
# @transaction.atomic
# def bind_email(username, email):
#     res = {
#         "code": "1",
#         "msg": "绑定成功"
#     }
#
#     user = User.objects.filter(username=username).first()
#     user.email = email
#     user.save()
#     return res


@transaction.atomic
def change_password(username, old_password, new_password):
    res = {
        "code": SUCCESS_CODE,
        "msg": "修改成功"
    }

    user = User.objects.filter(username=username).first()
    if user.password != old_password:
        res["code"] = ERROR_CODE
        res["msg"] = "旧密码错误"
    else:
        user.password = new_password
        user.save()
    return res


@transaction.atomic
def add_manga(username, manga):
    return
