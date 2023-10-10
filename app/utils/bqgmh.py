# 数据来源：笔趣阁
import random
import time
from threading import Thread

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.biqug.org"
# 模式识别，0为请求桌面页面，1为请求移动端页面
MODE = 1
mobile_headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) " +
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}
desktop_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


def get_chapter_images(chapter_url):
    """
    根据章节获取图片列表
    :param chapter_url:
    :return: list<string>
    """

    # 获取原始文本
    r = requests.get(BASE_URL + chapter_url, headers=mobile_headers)
    r.encoding = "UTF-8"
    soup = BeautifulSoup(r.text, "html.parser")

    # 获取图片元素列表
    chapter_images = []
    images = soup.find(class_="comic-list").find_all("img")
    for image in images:
        chapter_images.append(image.get("src"))

    # 去除尾部广告二维码图片
    # chapter_images.pop()
    return chapter_images


def get_chapter_lists(manga_url):
    """
    获取漫画章节列表
    :param manga_url:
    :return:[
        {
            "title": 列表名（此处只有一个）
            "chapter_list": [
                {
                    "name": 章节名,
                    "url": 章节链接
                },...复数个
            ]
        }
    ]
    """

    # 获取原始文本
    r = requests.get(BASE_URL + manga_url, headers=mobile_headers)
    # r.encoding = "UTF-8"
    # 提取章节容器元素
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup)
    chapter_html = soup.find(class_="catalog-list").find_all("a")

    # 适应接口形状
    # 循环获取所有章节列表，存入chapter_lists并返回
    res = {"title": "连载列表"}
    chapter_list = []
    for chapter in chapter_html:
        chapter_list.append({
            "name": chapter.text,
            "url": chapter["href"].replace("https://www.biqug.org", "")
        })
    chapter_list.reverse()
    res["chapter_list"] = chapter_list

    chapter_lists = [res]

    return chapter_lists


def get_manga_info(manga_url):
    """
    获取漫画信息
    :return:{
        "image_url": 封面图片,
        "title": 标题,
        "author": 作者,
        "author_url": 作者主页,
        "status": 连载状态,
        "category": 漫画类别,
        "category_url": 类别主页,
        "tags": [{
            name: 标签名,
            url: 标签链接
        }],
        "detail": 漫画介绍
    }
    """

    manga_info = dict()
    if MODE == 0:
        # 获取原始文本
        r = requests.get(BASE_URL + manga_url, headers=desktop_headers)
        r.encoding = "UTF-8"
        soup = BeautifulSoup(r.text, "html.parser")
        info_group = soup.find(class_="de-info__box")

        manga_info["image_url"] = info_group.find(class_="de-info__cover").find("img").get("src")
        manga_info["title"] = info_group.find(class_="comic-title").text

        # 作者
        manga_info["author"] = info_group.find(class_="name").text
        manga_info["author_url"] = info_group.find(class_="name").find("a").get("href")

        # 状态
        manga_info["status"] = soup.find(class_="de-chapter__title").find("span").text

        # 类别
        manga_info["category"] = "少年漫画"
        manga_info["category_url"] = "base_url"

        # 标签
        tags = []
        for t in info_group.find(class_="comic-status").find("span").find_all("a"):
            tags.append({
                "name": t.text,
                "url": t.get("href")
            })

        manga_info["tags"] = tags

        # 简介
        manga_info["detail"] = info_group.find(class_="intro-total").text.replace("\"", "")
    elif MODE == 1:
        # 获取原始文本
        r = requests.get(BASE_URL + manga_url, headers=mobile_headers)
        r.encoding = "UTF-8"
        soup = BeautifulSoup(r.text, "html.parser")
        info_group = soup.find(class_="comic-info-box")

        manga_info["image_url"] = re.search(r"\('(.+?)'\)", str(info_group)).group(1)
        manga_info["title"] = info_group.find(class_="comic-name").text

        # 作者
        manga_info["author"] = info_group.find(class_="au-name").text.split("：")[1].strip().replace("\n", "")
        manga_info["author_url"] = ""

        # 状态
        manga_info["status"] = soup.find(class_="comic-update-info").text

        # 类别
        manga_info["category"] = random.choice(["少女漫画", "少年漫画", "少儿漫画", "青年漫画", "儿童漫画"])
        manga_info["category_url"] = ""

        # 标签
        tags = []
        html_tags = info_group.find(class_="comic-tags").text.split("\n")
        if len(html_tags) == 4:
            for t in html_tags[2].strip().split(" "):
                tags.append({
                    "name": t,
                    "url": ""
                })

        manga_info["tags"] = tags

        # 简介
        manga_info["detail"] = soup.find(class_="comic-intro").text.replace("\"", "")
    return manga_info


def search(keywords, page):
    """
    搜索漫画
    :param keywords: 关键词
    :param page: 页数
    :return:[
        {
            "title": 漫画标题,
            "manga_url": 漫画链接,
            "image_url": 封面图片链接,
            "author": 作者,
            "last_chapter": 最后更新章节,
        }
    ]
    """

    # search_url=BASE_URL + "/search/{}/{}".format(keywords, page)
    search_url = BASE_URL + "/index.php/search?key={}".format(keywords)

    # 获取原始文本
    r = requests.get(search_url, headers=mobile_headers)
    # r.encoding = "UTF-8"
    # 提取搜索结果容器元素
    soup = BeautifulSoup(r.text, "html.parser")
    search_list = soup.select(".comic-list-item")

    search_result = []
    # 若为空则直接返回
    if search_list is None:
        return search_result

    # 遍历搜索结果，存入search_result后返回
    for item in search_list:
        search_result.append({
            "title": item.find(class_="comic-name").text,
            "manga_url": item.find("a").get("href"),
            "image_url": item.find("img").get("src"),
            "author": "未知",
            "last_chapter": "未知",
        })

    return search_result


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


@async_call
def download():
    """
    下载信息到数据库

    :return:
    """
    import app.service.mangaService_bqg as mangaService
    page = 15

    while True:
        url = BASE_URL + "/index.php/category/page/{0}".format(page)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        manga_list = soup.find(class_="cate-comic-list").find_all(class_="common-comic-item")

        index = 0
        for manga_info in manga_list:
            url = manga_info.find("a").get("href")
            mangaService.get_manga_info(None, url)
            index += 1
            print("缓存第{0}页第{1}部漫画信息".format(page, index))

        if index < 30:
            break

        page += 1


if __name__ == '__main__':
    # download()

    # chapter_lists = get_chapter_lists("/index.php/comic/moshiweiwang")
    # print(chapter_lists)
    # print(get_chapter_images("/index.php/chapter-284292.html"))

    # print(get_manga_info("/index.php/comic/moshiweiwang"))

    # print(chapter_lists[0])
    # chapter = chapter_lists[0]["chapter_list"][0]
    # print(get_chapter_images(chapter.get("url")))
    #
    print(search("斗破", 1))

    # start = time.time()
    #
    # r1 = requests.get("https://www.biqug.org/index.php/comic/wuliandianfeng", headers=mobile_headers)
    # t1 = time.time()
    # print(r1.status_code, t1 - start)
    #
    # r2 = requests.get("https://www.biqug.org/index.php/comic/wuliandianfeng", headers=desktop_headers)
    #
    # t2 = time.time()
    # print(r2.status_code, t2 - t1)
