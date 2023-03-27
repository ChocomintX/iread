import json

from django.db import models
from django.db.models import Q
from django.forms.models import model_to_dict


# Create your models here.

class User(models.Model):
    """用户表"""

    class Meta:
        db_table = "user"
        constraints = [models.CheckConstraint(check=Q(active_status=0) | Q(active_status=1), name="action_check")]

    username = models.CharField(verbose_name="用户名", max_length=100)
    password = models.CharField(verbose_name="密码", max_length=100)
    nickname = models.CharField(verbose_name="昵称", max_length=100)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    phone_number = models.CharField(verbose_name="手机号", max_length=15, null=True)
    email = models.CharField(verbose_name="邮箱", max_length=50)
    collect_choices = (
        (0, "未激活用户"),
        (1, "已激活用户")
    )
    active_status = models.SmallIntegerField(verbose_name="账号激活状态", choices=collect_choices, default=0)


# class MangaHistory(models.Model):
#     """漫画浏览历史表"""
#
#     class Meta:
#         db_table = "history_manga"
#
#     name = models.CharField(verbose_name="漫画名", max_length=30)
#     image_url = models.CharField(verbose_name="最后阅读章节的链接", max_length=500)
#     manga_url = models.CharField(verbose_name="漫画信息链接", max_length=500)
#     last_read_chapter = models.CharField(verbose_name="最后阅读章节", max_length=100)
#     last_read_time = models.DateTimeField(verbose_name="最后阅读时间")
#     last_read_url = models.CharField(verbose_name="最后阅读章节的链接", max_length=500)
#
#     collect_choices = (
#         (0, "未加入书架"),
#         (1, "已加入书架")
#     )
#     collect = models.SmallIntegerField(verbose_name="是否收藏", choices=collect_choices)
#     user = models.ForeignKey(verbose_name="用户id", to=User, to_field="id", on_delete=models.CASCADE)

class MangaAuthor(models.Model):
    """漫画作者表"""

    class Meta:
        db_table = "manga_author"

    name = models.CharField(verbose_name="作者名", max_length=100)
    url = models.CharField(verbose_name="作者主页链接", max_length=500)


class MangaCategory(models.Model):
    """漫画类别表"""

    class Meta:
        db_table = "manga_category"

    name = models.CharField(verbose_name="类别名", max_length=100)
    url = models.CharField(verbose_name="类别链接", max_length=500)


class MangaTag(models.Model):
    """漫画标签表"""

    class Meta:
        db_table = "manga_tag"

    name = models.CharField(verbose_name="标签名", max_length=100)
    url = models.CharField(verbose_name="标签链接", max_length=500)


# class MangaType(models.Model):
#     """漫画类型表"""
#
#     class Meta:
#         db_table = "manga_type"
#
#     name = models.CharField(verbose_name="类型名", max_length=100)
#     url = models.CharField(verbose_name="类型链接", max_length=500)

class Manga(models.Model):
    """漫画表"""

    class Meta:
        db_table = "manga_info"

    # def __str__(self):
    #     return json.dumps(model_to_dict(self))

    title = models.CharField(verbose_name="漫画名", max_length=200)
    image_url = models.CharField(verbose_name="最后阅读章节的链接", max_length=500)
    manga_url = models.CharField(verbose_name="漫画主页链接", max_length=500)
    status = models.CharField(verbose_name="状态", max_length=200)
    detail = models.CharField(verbose_name="简介", max_length=1000)

    author = models.ForeignKey(verbose_name="作者id", to=MangaAuthor, to_field="id", on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name="类别id", to=MangaCategory, to_field="id", on_delete=models.CASCADE)
    tags = models.ManyToManyField(verbose_name="标签", to=MangaTag, through="MangaInfoTag")


class MangaInfoTag(models.Model):
    """漫画标签联系表"""

    class Meta:
        db_table = "manga_info_tag"

    manga = models.ForeignKey(verbose_name="漫画id", to=Manga, to_field="id", on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name="标签id", to=MangaTag, to_field="id", on_delete=models.CASCADE)


class MangaHistory(models.Model):
    """漫画浏览历史表"""

    class Meta:
        db_table = "manga_history"

    last_read_chapter = models.CharField(verbose_name="最后阅读章节", max_length=100, null=True)
    last_read_time = models.DateTimeField(verbose_name="最后阅读时间", auto_now=True)
    last_read_url = models.CharField(verbose_name="最后阅读章节的链接", max_length=500, null=True)

    is_read_choices = (
        (0, "未阅读"),
        (1, "已阅读"),
        (2, "已删除")
    )
    is_read = models.SmallIntegerField(verbose_name="是否浏览", default=0)

    collect_choices = (
        (0, "未加入书架"),
        (1, "已加入书架")
    )
    collect = models.SmallIntegerField(verbose_name="是否收藏", choices=collect_choices, default=0)

    manga = models.ForeignKey(verbose_name="漫画id", to=Manga, to_field="id", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户id", to=User, to_field="id", on_delete=models.CASCADE)


class BookAuthor(models.Model):
    """小说作者表"""

    class Meta:
        db_table = "book_author"

    name = models.CharField(verbose_name="作者名", max_length=100)


class Book(models.Model):
    """小说信息表"""

    class Meta:
        db_table = "book_info"

    name = models.CharField(verbose_name="小说名", max_length=30)
    image_url = models.CharField(verbose_name="封面图片链接", max_length=500)
    book_url = models.CharField(verbose_name="小说主页链接", max_length=500)

    new_chapter_name = models.CharField(verbose_name="最新章节名", max_length=100)
    new_chapter_url = models.CharField(verbose_name="最新章节链接", max_length=500)
    update_time = models.DateTimeField(verbose_name="最近更新时间")

    status = models.CharField(verbose_name="连载状态", max_length=20)
    detail = models.CharField(verbose_name="简介", max_length=1000)

    author = models.ForeignKey(verbose_name="作者id", to=BookAuthor, to_field="id", on_delete=models.CASCADE)
    # category = models.ForeignKey(verbose_name="类别id", to=MangaCategory, to_field="id", on_delete=models.CASCADE)
    # tags = models.ManyToManyField(verbose_name="标签", to=MangaTag, through="MangaInfoTag")


class BookHistory(models.Model):
    """小说浏览历史表"""

    class Meta:
        db_table = "book_history"

    last_read_chapter = models.CharField(verbose_name="最后阅读章节", max_length=100, null=True)
    last_read_time = models.DateTimeField(verbose_name="最后阅读时间", auto_now=True)
    last_read_url = models.CharField(verbose_name="最后阅读章节的链接", max_length=500, null=True)

    is_read_choices = (
        (0, "未阅读"),
        (1, "已阅读"),
        (2, "已删除")
    )
    is_read = models.SmallIntegerField(verbose_name="是否浏览", default=0)

    collect_choices = (
        (0, "未加入书架"),
        (1, "已加入书架")
    )
    collect = models.SmallIntegerField(verbose_name="是否收藏", choices=collect_choices, default=0)

    book = models.ForeignKey(verbose_name="小说id", to=Book, to_field="id", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户id", to=User, to_field="id", on_delete=models.CASCADE)
