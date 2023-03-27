import json

from django.http import HttpResponse, response, JsonResponse
import app.service.bookService as bookService
from app.utils.return_code import SUCCESS_CODE, ERROR_CODE


# 小说操作的所有接口

def get_home_book(request):
    try:
        print(bookService.get_home_books())
        return JsonResponse(bookService.get_home_books())
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_book_info(request):
    try:
        data = request.POST
        book_id = data.get("book_id")
        book_url = data.get("book_url")
        return JsonResponse(bookService.get_book_info(book_id, book_url))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_book_chapter(request):
    try:
        data = request.POST
        book_url = data.get("book_url")
        return JsonResponse(bookService.get_book_chapter(book_url))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def add_book_history(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        last_read_chapter = data.get("last_read_chapter")
        last_read_url = data.get("last_read_url")
        return JsonResponse(bookService.add_book_history(user_id, book_id, last_read_chapter, last_read_url))
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
        book_id = data.get("book_id")
        return JsonResponse(bookService.get_last_read_chapter(user_id, book_id))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def set_book_collect(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        collect = data.get("collect")
        return JsonResponse(bookService.set_book_collect(user_id, book_id, collect))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_chapter_content(request):
    try:
        data = request.POST
        chapter_url = data.get("chapter_url")
        return JsonResponse(bookService.get_chapter_content(chapter_url))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def add_book_history(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        last_read_chapter = data.get("last_read_chapter")
        last_read_url = data.get("last_read_url")
        return JsonResponse(bookService.add_book_history(user_id, book_id, last_read_chapter, last_read_url))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_book_collections(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        return JsonResponse(bookService.get_book_collections(user_id))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def delete_book_collections(request):
    try:
        data = request.POST
        delete_list = json.loads(data.get("delete_list"))
        return JsonResponse(bookService.delete_book_collections(delete_list))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_book_history(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        return JsonResponse(bookService.get_all_book_history(user_id))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def delete_book_history(request):
    try:
        data = request.POST
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        return JsonResponse(bookService.delete_book_history(user_id, book_id))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })


def get_book_search(request):
    try:
        data = request.POST
        keywords = data.get("keywords")
        page = data.get("page")
        return JsonResponse(bookService.book_search(keywords, page))
    except Exception as e:
        return JsonResponse({
            "code": ERROR_CODE,
            "msg": "请求失败！",
            "error_msg": str(e)
        })