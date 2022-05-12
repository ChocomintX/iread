from threading import Timer

from django.db import transaction
import app.utils.bookSpider as bookspider
from app.utils.serilizers import *
from app.utils.return_code import *
from django.db.models import Q
from django.core.cache import cache
import json


# 小说相关操作服务层

def get_home_books():
    """获取首页的小说列表"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取成功",
    }
    home_books = cache.get("home_books")
    if home_books is None:
        home_books = bookspider.get_home_books()
        cache.set("home_books", home_books)

    res["data"] = home_books
    return res


@transaction.atomic
def get_book_info(book_id, book_url):
    """获取小说详细信息"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取成功",
    }
    book = Book.objects.filter(Q(id=book_id) | Q(book_url=book_url)).first()
    if book is None:
        data = bookspider.get_book_info(book_url)

        # 检测是否存在该小说作者，不存在则插入
        author_name = data.get("author")
        author = BookAuthor.objects.filter(name=author_name).first()
        if author is None:
            author = BookAuthor.objects.create(name=author_name)

        book = Book.objects.create(
            name=data.get("name"),
            author=author,
            image_url=data.get("image_url"),
            book_url=book_url,
            update_time=data.get("update_time"),
            new_chapter_name=data.get("new_chapter_name"),
            new_chapter_url=data.get("new_chapter_url"),
            detail=data.get("detail"),
            status=data.get("status")
        )
        print("添加新小说:", data.get("name"))

    book = Book.objects.filter(Q(id=book_id) | Q(book_url=book_url)).first()
    res["data"] = BookSerialize(book).data

    return res


def get_book_chapter(book_url):
    """获取小说章节列表"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取成功",
        "data": bookspider.get_book_chapter(book_url)
    }

    return res


@transaction.atomic
def add_book_history(user_id, book_id, last_read_chapter, last_read_url):
    """添加阅读记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "更新记录成功",
    }

    history = BookHistory.objects.filter(user_id=user_id, book_id=book_id).first()
    # 若不存在阅读记录则添加 存在则更新浏览时间
    if history is None:
        history = BookHistory.objects.create(user_id=user_id, book_id=book_id, last_read_chapter=last_read_chapter,
                                             last_read_url=last_read_url, is_read=1)
        res["msg"] = "添加记录成功"
    else:
        history.last_read_chapter = last_read_chapter
        history.last_read_url = last_read_url
        history.is_read = 1
        history.save()
    res["data"] = BookHistorySerialize(history).data
    return res


@transaction.atomic
def get_last_read_chapter(user_id, book_id):
    """获取用户对该小说的浏览记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取该小说阅读记录成功",
    }
    history = BookHistory.objects.filter(user_id=user_id, book_id=book_id).first()

    if history is not None:
        res["data"] = BookHistorySerialize(history).data
    else:
        res["code"] = FAIL_CODE
        res["msg"] = "没有浏览记录"
        res["data"] = BookHistorySerialize(BookHistory.objects.create(user_id=user_id, book_id=book_id)).data

    return res


@transaction.atomic
def get_chapter_content(chapter_url):
    """获取该章节的文本内容"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取章节内容成功",
        "data": bookspider.get_chapter_content(chapter_url)
    }

    return res


def set_book_collect(user_id, book_id, collect):
    """设置是否加入书架"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "加入书架成功" if collect == "1" else "移出书架成功",
    }

    history = BookHistory.objects.filter(user_id=user_id, book_id=book_id)
    # if history.first() is None:

    history.update(collect=collect)

    res["data"] = BookHistorySerialize(history.first()).data

    return res


@transaction.atomic
def add_book_history(user_id, book_id, last_read_chapter, last_read_url):
    """添加阅读记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "更新记录成功",
    }

    history = BookHistory.objects.filter(user_id=user_id, book_id=book_id).first()
    # 若不存在阅读记录则添加 存在则更新浏览时间
    if history is None:
        history = BookHistory.objects.create(user_id=user_id, book_id=book_id, last_read_chapter=last_read_chapter,
                                             last_read_url=last_read_url, is_read=1)
        res["msg"] = "添加记录成功"
    else:
        history.last_read_chapter = last_read_chapter
        history.last_read_url = last_read_url
        history.is_read = 1
        history.save()
    res["data"] = BookHistorySerialize(history).data
    return res


@transaction.atomic
def get_book_collections(user_id):
    """获取用户的书架"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取书架信息成功",
    }
    history = BookHistory.objects.filter(user_id=user_id, collect=1).order_by("-last_read_time")

    res["data"] = BookHistorySerialize(history, many=True).data

    return res


@transaction.atomic
def delete_book_collections(delete_list):
    """删除书架中的书"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "删除书架成功",
    }

    for index in delete_list:
        history = BookHistory.objects.filter(id=index)
        history.update(collect=0)

    return res


@transaction.atomic
def get_all_book_history(user_id):
    """获取用户的小说历史记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取用户小说历史记录成功",
    }
    history = BookHistory.objects.filter(user_id=user_id).exclude(is_read=0).order_by("-last_read_time")

    res["data"] = BookHistorySerialize(history, many=True).data

    return res


@transaction.atomic
def delete_book_history(user_id, book_id):
    """删除浏览记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "删除成功",
    }
    history = BookHistory.objects.filter(user_id=user_id, book_id=book_id).all()
    print(history)

    history.update(is_read=0)

    res["data"] = get_all_book_history(user_id)["data"]

    return res


@transaction.atomic
def book_search(keywords, page):
    """根据关键字模糊查找漫画"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取搜索结果成功",
    }
    bookspider.download_search(keywords)
    data = Book.objects.filter(Q(name__contains=keywords) | Q(author__name__contains=keywords)).all()

    res["data"] = BookSerialize(data, many=True).data

    return res
