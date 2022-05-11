from datetime import datetime, timezone

from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from app.models import *
from iread.settings import TIME_ZONE


class TimestampField(serializers.Field):
    """
    This serializer field transform a datetime str to a timestamp float.
    """

    def to_representation(self, value):
        return value.timestamp()

    def to_internal_value(self, data):
        timestamp = float(data)
        no_tz = datetime.utcfromtimestamp(timestamp)
        return no_tz.astimezone(timezone(TIME_ZONE))


class UserSerialize(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MangaAuthorSerialize(ModelSerializer):
    class Meta:
        model = MangaAuthor
        fields = "__all__"


class MangaCategorySerialize(ModelSerializer):
    class Meta:
        model = MangaCategory
        fields = "__all__"


class MangaTagSerialize(ModelSerializer):
    class Meta:
        model = MangaTag
        fields = "__all__"


class MangaSerialize(ModelSerializer):
    author = MangaAuthorSerialize()
    category = MangaCategorySerialize()
    tags = MangaTagSerialize(many=True)

    class Meta:
        model = Manga
        fields = "__all__"


class MangaHistorySerialize(ModelSerializer):
    manga = MangaSerialize()
    # last_read_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    last_read_time = TimestampField()

    class Meta:
        model = MangaHistory
        fields = "__all__"


class BookAuthorSerialize(ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = "__all__"


class BookSerialize(ModelSerializer):
    author = BookAuthorSerialize()
    update_time = TimestampField()

    class Meta:
        model = Book
        fields = "__all__"


class BookHistorySerialize(ModelSerializer):
    book = BookSerialize()
    last_read_time = TimestampField()

    class Meta:
        model = BookHistory
        fields = "__all__"
