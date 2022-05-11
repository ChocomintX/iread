"""iread URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.service import userService
from app.views import userApi, mangaApi, bookApi
from app.utils import bookSpider

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', userApi.test),
    path('chapter/', userService.testchapter),

    # 用户接口
    path('user/', include([
        path('login/', userApi.login),
        path('register/', userApi.register),
        path('update/', userApi.update),
        path('bindPhone/', userApi.bind_phone),
        path('bindEmail/', userApi.bind_email),
        path('changePassword/', userApi.change_password),
    ])),

    # 漫画操作接口
    path('manga/', include([
        path('getHotManga/', mangaApi.get_hot_manga),
        path('getHomeManga/', mangaApi.get_home_manga),
        path('getMangaInfo/', mangaApi.get_manga_info),
        path('getMangaChapterList/', mangaApi.get_manga_chapter_list),
        path('getMangaChapterImages/', mangaApi.get_manga_chapter_images),
        path('getLastReadChapter/', mangaApi.get_last_read_chapter),
        path('getMangaHistory/', mangaApi.get_manga_history),
        path('getMangaCollections/', mangaApi.get_manga_collections),
        path('getMangaSearch/', mangaApi.get_manga_search),
        path('addMangaHistory/', mangaApi.add_manga_history),
        path('setMangaCollect/', mangaApi.set_manga_collect),
        path('deleteMangaHistory/', mangaApi.delete_manga_history),
        path('deleteMangaCollections/', mangaApi.delete_manga_collections)

    ])),

    # 小说操作接口
    path('book/', include([
        path('getHomeBook/', bookApi.get_home_book),
        path('getBookInfo/', bookApi.get_book_info),
        path('getBookChapter/', bookApi.get_book_chapter),
        path('getLastReadChapter/', bookApi.get_last_read_chapter),
        path('getChapterContent/', bookApi.get_chapter_content),
        path('getBookCollections/', bookApi.get_book_collections),
        path('getBookHistory/', bookApi.get_book_history),
        path('setBookCollect/', bookApi.set_book_collect),
        path('addBookHistory/', bookApi.add_book_history),
        path('deleteBookCollections/', bookApi.delete_book_collections),
        path('deleteBookHistory/', bookApi.delete_book_history),
    ]))
]
