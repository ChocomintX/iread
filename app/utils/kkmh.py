from threading import Thread

import requests
from bs4 import BeautifulSoup
import re

base_url = "http://www.ykmh.com"


def get_chapter_images(chapter_url):
    """根据章节获取图片列表"""

    # 获取原始文本
    r = requests.get(chapter_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    })
    r.encoding = "UTF-8"
    # soup = BeautifulSoup(r.text, "html.parser")
    # script = soup.find("script").text
    # print(script)

    # 正则提取，并转换为list
    chapter_images = re.search("(?<=chapterImages = \\[).*?(?=])", r.text).group()
    if chapter_images:
        # 去除斜杠与双引号
        chapter_images = chapter_images.replace('"', "").replace("\\", "")
        # 切割为list
        chapter_images = chapter_images.split(",")
    for i in range(len(chapter_images)):
        chapter_images[i] = "http://js.tingliu.cc" + chapter_images[i]
    return chapter_images


def get_chapter_lists(manga_url):
    """获取漫画所有章节"""

    # 获取原始文本
    r = requests.get(manga_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    })
    r.encoding = "UTF-8"
    # 提取章节容器元素
    soup = BeautifulSoup(r.text, "html.parser")
    zj_list = soup.find_all("div", attrs={'class': 'zj_list'})

    # 循环获取所有章节列表，存入chapter_lists并返回
    chapter_lists = []
    for l in zj_list:
        item = dict()
        # 列表标题
        item["title"] = l.find("h2").text

        chapter_list = []
        # 处理章节标签
        for chapter in l.find_all("li"):
            chapter_list.append({
                "name": chapter.find("span", attrs={"class": "list_con_zj"}).text.strip(),
                "url": base_url + chapter.find("a").get("href")
            })

        # 列表内容
        item["chapter_list"] = chapter_list
        chapter_lists.append(item)

    return chapter_lists


def get_manga_info(manga_url):
    """获取漫画的信息"""

    # 获取原始文本
    r = requests.get(manga_url)
    r.encoding = "UTF-8"
    soup = BeautifulSoup(r.text, "html.parser")
    info_group = soup.find("div", attrs={"class": "wrap_intro_l_comic"})

    manga_info = dict()
    manga_info["image_url"] = info_group.find("div", attrs={"class": "comic_i_img"}).find("img").get("src")
    manga_info["title"] = info_group.find("h1").text

    # 作者、分类等信息
    infos = info_group.find("ul", attrs={"class": "comic_deCon_liO"}).findAll("li")

    # 作者
    manga_info["author"] = infos[0].find("a").text
    manga_info["author_url"] = base_url + infos[0].find("a").get("href")

    # 状态
    manga_info["status"] = infos[1].find("a").text

    # 类别
    manga_info["category"] = infos[2].find("a").text
    manga_info["category_url"] = base_url + infos[2].find("a").get("href")

    # 类型
    tags = []
    for t in infos[3].findAll("a"):
        tags.append({
            "name": t.text,
            "url": base_url + t.get("href")
        })

    manga_info["tags"] = tags

    # 简介
    d = info_group.findAll("p", attrs={"class": "comic_deCon_d"})
    manga_info["detail"] = d[len(d) - 1].text.replace("[-折叠]", "").replace("[+展开] ", "").replace("\n<<隐藏",
                                                                                                     "").strip()

    return manga_info


def search(keywords, page):
    """搜索漫画"""

    # 获取原始文本
    r = requests.get(base_url + "/search/?keywords={}&page={}".format(keywords, page))
    r.encoding = "UTF-8"
    # 提取搜索结果容器元素
    soup = BeautifulSoup(r.text, "html.parser")
    search_list = soup.find("ul", attrs={"class": "list_con_li"})

    search_result = list()
    if search_list is None:
        return search_result

    search_list = search_list.find_all("li")
    # 遍历搜索结果，存入search_result后返回
    for item in search_list:
        search_result.append({
            "title": item.find("a").get("title"),
            "manga_url": item.find("a").get("href"),
            "image_url": item.find("a").find("img").get("src"),
            "author": item.findAll("p")[1].text.strip(),
            "last_chapter": item.findAll("p")[2].text.strip(),
        })

    return search_result


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


@async_call
def download():
    """下载信息到数据库"""
    import app.service.mangaService as ms
    # 获取原始文本
    page = 1
    while True:
        r = requests.get("http://www.ykmh.com/list/click/?page={0}".format(page))
        r.encoding = "UTF-8"
        # 提取搜索结果容器元素
        soup = BeautifulSoup(r.text, "html.parser")
        manga_list = soup.find(attrs={"class": "list-view"}).find_all(attrs={"class": "comic_img"})

        index = 0
        for manga in manga_list:
            print(manga.get("href"))
            ms.get_manga_info(None, manga.get("href"))
            index += 1
            print("缓存第{0}页第{1}部漫画信息".format(page, index))
        if index < 36:
            break
        page += 1


if __name__ == '__main__':
    imgs = get_chapter_images("http://www.ykmh.com/manhua/yiquanchaoren/132026.html")
    print(imgs)
    # print(imgs, "\n", len(imgs))
    # chapters = get_chapter_lists("https://www.ykmh.com/manhua/jinjidejuren/")
    # print(chapters)
    # info = get_manga_info("http://www.ykmh.com/manhua/yiquanchaoren/")
    # print(info)
    # download()
