import json

from django.http import HttpResponse, response, JsonResponse
import app.service.mangaService_bqg as mangaService
from app.utils.return_code import SUCCESS_CODE, ERROR_CODE


# 漫画操作的所有接口

def get_hot_manga(request):
    try:
        return JsonResponse(mangaService.get_hot_manga_local())
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_home_manga(request):
    try:
        return JsonResponse(mangaService.get_home_manga())
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_manga_info(request):
    try:
        data = request.POST
        manga_id = data.get("manga_id")
        manga_url = data.get("manga_url")
        return JsonResponse(mangaService.get_manga_info(manga_id, manga_url))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def add_manga_history(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        manga_id = data.get("manga_id")
        last_read_chapter = data.get("last_read_chapter")
        last_read_url = data.get("last_read_url")
        return JsonResponse(mangaService.add_manga_history(user_id, manga_id, last_read_chapter, last_read_url))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_manga_chapter_list(request):
    try:
        data = request.POST
        manga_url = data.get("manga_url")
        return JsonResponse(mangaService.get_chapter_list(manga_url))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def set_manga_collect(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        manga_id = data.get("manga_id")
        collect = data.get("collect")
        return JsonResponse(mangaService.set_manga_collect(user_id, manga_id, collect))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_manga_chapter_images(request):
    try:
        data = request.POST
        chapter_url = data.get("chapter_url")
        return JsonResponse(mangaService.get_chapter_images(chapter_url))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_last_read_chapter(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        manga_id = data.get("manga_id")
        return JsonResponse(mangaService.get_last_read_chapter(user_id, manga_id))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_manga_history(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        return JsonResponse(mangaService.get_all_manga_history(user_id))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def delete_manga_history(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        manga_id = data.get("manga_id")
        return JsonResponse(mangaService.delete_manga_history(user_id, manga_id))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_manga_collections(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        manga_id = data.get("manga_id")
        return JsonResponse(mangaService.get_manga_collections(user_id))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def delete_manga_collections(request):
    try:
        data = request.POST
        delete_list = json.loads(data.get("delete_list"))
        return JsonResponse(mangaService.delete_manga_collections(delete_list))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_manga_search(request):
    try:
        data = request.POST
        keywords = data.get("keywords")
        page = data.get("page")
        return JsonResponse(mangaService.manga_search(keywords, page))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })
