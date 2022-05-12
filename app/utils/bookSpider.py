from threading import Thread
from time import sleep
from urllib.parse import unquote, quote
import requests
from bs4 import BeautifulSoup
import app.service.bookService as bs

# 数据源网址，此处选择笔趣阁
base_url = "https://www.qbiqu.com"


def get_home_books():
    """
    获取网站首页的推荐列表
    返回的数据结构为
    [
        {
            "title": 分类标题,
            "top_book": { # 置顶图书
                "name": 书名,
                "image_url": 图片,
                "book_url": 链接,
                "detail": 简介
            },
            "book_list": [ # 该分类图书列表
                {
                    "name": 书名,
                    "author": 作者,
                    "book_url": 链接
                },
            ]
        }
    ]
    """
    result = []

    r = requests.get(base_url)
    r.encoding = "GBK"

    soup = BeautifulSoup(r.text, "html.parser")
    novelslist = soup.find_all("div", {"class": "novelslist"})

    for group in novelslist:
        contents = group.find_all(attrs={"class": "content"})
        for content in contents:
            book_list = []
            for book in content.find_all("li"):
                book_list.append({
                    "name": book.text.split("/")[0],
                    "author": book.text.split("/")[1],
                    "book_url": book.find("a").get("href")
                })

            result.append({
                "title": content.find("h2").text,
                "top_book": {
                    "name": content.find("a").text,
                    "image_url": content.find("img").get("src"),
                    "book_url": content.find("a").get("href"),
                    "detail": content.find("dd").text
                },
                "book_list": book_list
            })
    return result


def get_book_info(book_url):
    """
    爬取小说信息

    :param book_url: 小说链接
    :return:{
        "name": 小说名,
        "author": 作者,
        "update_time": 最后更新时间,
        "new_chapter_name": 最后更新章节,
        "new_chapter_url": 最新章节链接,
        "image_url": 封面图片链接,
        "status": 连载状态
    }
    """
    r = requests.get(book_url)
    r.encoding = "GBK"

    soup = BeautifulSoup(r.text, "html.parser")
    info = soup.find(id="info")
    img = soup.find(id="fmimg")
    result = {
        "name": info.find("h1").text,
        "author": info.find_all("p")[0].text.split("：")[1],
        "update_time": info.find_all("p")[2].text.split("：")[1],
        "new_chapter_name": info.find_all("a")[3].get("title"),
        "new_chapter_url": book_url + info.find_all("a")[3].get("href"),
        "image_url": base_url + img.find().get("src"),
        "detail": soup.find(id="intro").find("p").text,
        "status": "连载中" if img.find_all()[1].get("class") == "a" else "已完结"
    }
    return result


def get_book_chapter(book_url):
    """
    爬取小说章节列表

    :param book_url: 小说链接
    :return:
    [
        {
            "chapter_name": 章节名,
            "chapter_url": 章节链接
        }
    ]
    """
    r = requests.get(book_url)
    r.encoding = "GBK"

    soup = BeautifulSoup(r.text, "html.parser")

    html_list = soup.find(id="list").find_all("a")

    for i in range(9):
        html_list.pop(0)

    chapter_list = []
    for item in html_list:
        chapter_list.append({
            "name": item.text,
            "url": base_url + item.get("href")
        })

    return chapter_list


def get_chapter_content(chapter_url):
    """
    爬取小说章节内容

    :param chapter_url: 章节链接
    :return: content 章节内容
    """
    r = requests.get(chapter_url)
    r.encoding = "GBK"

    soup = BeautifulSoup(r.text, "html.parser")

    # print(r.text)
    content = str(soup.find("div", id="content")).replace("<div id=\"content\">", "").replace("</div>", "")

    return str(content)


def search(keywords, page):
    """
    模糊搜索小说

    :param keywords: 关键字
    :param page: 页数
    :return:
    """
    r = requests.get("https://www.qbiqu.com/modules/article/search.php?searchkey={0}&page={1}".format(
        quote(keywords, encoding="GBK"), page))
    r.encoding = "GBK"
    print(keywords, page)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup)
    books = soup.find_all(id="nr")
    for book in books:
        bs.get_book_info(None, book.find("a").get("href"))


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


@async_call
def download_search(keywords):
    """
    缓存搜索到的小说

    :param keywords:
    :return:
    """
    page = 1
    flag = True
    while flag:
        r = requests.get("https://www.qbiqu.com/modules/article/search.php?searchkey={0}&page={1}".format(
            quote(keywords, encoding="GBK"), page))
        r.encoding = "GBK"
        soup = BeautifulSoup(r.text, "html.parser")

        flag = soup.find(attrs={"class": "next"}) is not None
        page += 1
        print(flag,page)
        books = soup.find_all(id="nr")
        for book in books:
            bs.get_book_info(None, book.find("a").get("href"))


@async_call
def download():
    """下载信息到数据库"""

    # 获取原始文本
    r = requests.get("https://www.qbiqu.com/xiaoshuodaquan/", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    })
    r.encoding = "GBK"
    # 提取搜索结果容器元素
    soup = BeautifulSoup(r.text, "html.parser")
    book_list = soup.find(attrs={"id": "main"}).find_all("a")
    print(book_list)
    index = 1
    sleep(6)
    for book in book_list:
        print("当前缓存小说{0},链接:{1}  进度:{2}/{3}".format(book.text, book.get("href"), index, len(book_list)))
        index += 1
        try:
            bs.get_book_info(None, book_url=book.get("href"))
        except:
            print("错误:", book)
            continue
    # print(error_list,len(error_list))


if __name__ == '__main__':
    search("大主宰", 1)
