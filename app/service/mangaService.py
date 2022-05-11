from django.db import transaction
import app.utils.kkmh as kkmh
from app.utils.serilizers import *
from app.utils.return_code import *
from django.core.cache import cache
import json


@transaction.atomic
def get_hot_manga_local():
    """获取热门漫画."""
    res = {
        "code": SUCCESS_CODE,
        "title": "热门漫画",
        "msg": "获取成功",
        # "data": MangaSerialize(Manga.objects.all(), many=True).data
    }

    # with open("app/static/hot_manga.json", "w", encoding="utf-8") as h:
    #     h.write(json.dumps(res, ensure_ascii=False))

    hot_manga = cache.get("hot_manga")
    if hot_manga is None:
        with open("app/static/hot_manga.json", encoding="utf-8") as h:
            hot_manga = json.load(h)["data"]
            cache.set("hot_manga", hot_manga)
            print("jinlaile1")
    res["data"] = MangaSerialize(hot_manga, many=True).data

    return res


@transaction.atomic
def get_home_manga():
    """获取漫画首页"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取成功",
    }

    categories = MangaCategory.objects.all()
    home_manga = []
    for category in categories:
        home_manga.append({
            "title": category.name,
            "data": MangaSerialize(Manga.objects.filter(category__name=category.name)[:12], many=True).data
        })

    cache.set("home_manga", home_manga)

    res["data"] = home_manga

    return res


@transaction.atomic
def get_manga_info(manga_id, manga_url):
    """根据传入url获取漫画信息"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取成功",

    }

    if manga_id is not None:
        manga = Manga.objects.filter(id=manga_id).first()
    else:
        manga = Manga.objects.filter(manga_url=manga_url).first()
    print(manga)
    # 如果本地数据库不存在该漫画信息，则调用工具类爬取信息并插入
    if manga is None:
        data = kkmh.get_manga_info(manga_url)
        title = data.get("title")
        image_url = data.get("image_url")
        status = data.get("status")
        detail = data.get("detail")
        # 检测是否存在该作者，不存在则插入
        author_name = data.get("author")
        author = MangaAuthor.objects.filter(name=author_name).first()
        if author is None:
            author = MangaAuthor.objects.create(name=author_name, url=data.get("author_url"))

        # 检测是否存在该类别，不存在则插入
        category_name = data.get("category")
        category = MangaCategory.objects.filter(name=category_name).first()
        if category is None:
            category = MangaCategory.objects.create(name=category_name, url=data.get("category_url"))

        # 检测是否存在该标签，不存在则插入
        tag_items = data.get("tags")
        tags = []
        for item in tag_items:
            tag_name = item.get("name")
            tag = MangaTag.objects.filter(name=tag_name).first()
            if tag is None:
                tag = MangaTag.objects.create(name=tag_name, url=item.get("url"))
            tags.append(tag.id)

        manga = Manga.objects.create(
            title=title,
            image_url=image_url,
            manga_url=manga_url,
            status=status,
            author=author,
            category=category,
            detail=detail
        )
        manga.tags.set(tags)
        manga.save()

    # 序列化对象信息并返回
    res["data"] = MangaSerialize(manga).data

    return res


@transaction.atomic
def add_manga_history(user_id, manga_id, last_read_chapter, last_read_url):
    """添加阅读记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "更新记录成功",
    }

    history = MangaHistory.objects.filter(user_id=user_id, manga_id=manga_id).first()
    # 若不存在阅读记录则添加 存在则更新浏览时间
    if history is None:
        history = MangaHistory.objects.create(user_id=user_id, manga_id=manga_id, last_read_chapter=last_read_chapter,
                                              last_read_url=last_read_url, is_read=1)
        res["msg"] = "添加记录成功"
    else:
        history.last_read_chapter = last_read_chapter
        history.last_read_url = last_read_url
        history.is_read = 1
        history.save()
    res["data"] = MangaHistorySerialize(history).data
    return res


@transaction.atomic
def get_chapter_list(manga_url):
    """获取章节列表"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取章节成功",

    }
    # 调用工具类获取所有章节
    lists = kkmh.get_chapter_lists(manga_url)
    res["data"] = lists
    return res


@transaction.atomic
def set_manga_collect(user_id, manga_id, collect):
    """设置是否加入书架"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "加入书架成功" if collect == "1" else "移出书架成功",
    }

    history = MangaHistory.objects.filter(user_id=user_id, manga_id=manga_id)
    # history.collect = collect
    history.update(collect=collect)

    res["data"] = MangaHistorySerialize(history.first()).data

    return res


@transaction.atomic
def get_chapter_images(chapter_url):
    """获取章节图片url列表"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取图片链接成功",
    }
    data = kkmh.get_chapter_images(chapter_url)
    res["data"] = data

    return res


@transaction.atomic
def manga_search(keywords, page):
    """根据关键字模糊查找漫画"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取搜索结果成功",
    }
    data = kkmh.search(keywords, page)

    res["data"] = data

    return res


@transaction.atomic
def get_last_read_chapter(user_id, manga_id):
    """获取用户对该漫画的浏览记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取该漫画阅读记录成功",
    }
    history = MangaHistory.objects.filter(user_id=user_id, manga_id=manga_id).first()

    if history is not None:
        res["data"] = MangaHistorySerialize(history).data
    else:
        res["code"] = FAIL_CODE
        res["msg"] = "没有浏览记录"
        res["data"] = MangaHistorySerialize(MangaHistory.objects.create(user_id=user_id, manga_id=manga_id)).data

    return res


@transaction.atomic
def get_all_manga_history(user_id):
    """获取用户的漫画历史记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取用户漫画历史记录成功",
    }
    history = MangaHistory.objects.filter(user_id=user_id).exclude(is_read=0).order_by("-last_read_time")

    res["data"] = MangaHistorySerialize(history, many=True).data

    return res


@transaction.atomic
def delete_manga_history(user_id, manga_id):
    """删除浏览记录"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "删除成功",
    }
    history = MangaHistory.objects.filter(user_id=user_id, manga_id=manga_id).all()
    print(history)

    history.update(is_read=0)

    res["data"] = get_all_manga_history(user_id)["data"]

    return res


@transaction.atomic
def get_manga_collections(user_id):
    """获取用户的书架"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "获取书架信息成功",
    }
    history = MangaHistory.objects.filter(user_id=user_id, collect=1).order_by("-last_read_time")

    res["data"] = MangaHistorySerialize(history, many=True).data

    return res


@transaction.atomic
def delete_manga_collections(delete_list):
    """删除书架中的书"""
    res = {
        "code": SUCCESS_CODE,
        "msg": "删除书架成功",
    }

    for index in delete_list:
        history = MangaHistory.objects.filter(id=index)
        history.update(collect=0)

    return res
