# -*- coding: UTF-8 -*-

import os
import re
import sys

import requests
from bs4 import BeautifulSoup


def get_writer_list():
    writer_list = []
    # index page
    index = 'http://zuopinj.com/writer/'
    req = requests.get(url = index)
    req.encoding = 'utf8'
    html = req.text
    bf1 = BeautifulSoup(html, features = "lxml")
    # get items for A-Z
    items = bf1.find_all('div', attrs={ "class": 'item' })
    for item in items:
        bf2 = BeautifulSoup(str(item), features = "lxml")
        # get all writers
        writers = bf2.find_all('li')
        for writer in writers:
            # get writers detail info
            bf3 = BeautifulSoup(str(writer), features = "lxml")
            try:
                author = re.findall(r"http://(.*).zuopinj.com/", bf3.li.a['href'])[0]
                type = 0
            except:
                author = re.findall(r"http://zuopinj.com/.*/(.*)/", bf3.li.a['href'])[0]
                type = 1
            finally:
                writer_list.append({
                    "type" : type,
                    "url" : bf3.li.a['href'],
                    "author" : author,
                    "title" : bf3.li.a['title'],
                    "name" : re.findall(r"(.*)作品", bf3.li.a['title'])[0],
                    "summary" : bf3.li.get_text(separator=" ", strip=True),
                })
    return writer_list

def get_book_list(url):
    # get all books url of a writer
    book_list = []

    # type 1
    req = requests.get(url = url)
    req.encoding = 'utf8'
    html = req.text
    bf1 = BeautifulSoup(html, features = "lxml")
    books = bf1.find_all('div', attrs={ "class": 'bk' })
    for book in books:
        bf2 = BeautifulSoup(str(book), features = "lxml")
        url = bf2.a['href']
        title = bf2.h3.get_text(separator=" ", strip=True)
        book_list.append({
            "url" : url,
            "title" : title,
        })

    # type 2
    if len(book_list) == 0:
        next_page = url
        while next_page != "":
            req = requests.get(url = next_page)
            req.encoding = 'utf8'
            html = req.text
            bf1 = BeautifulSoup(html, features = "lxml")
            tab_on = bf1.find('div', attrs={ "class": 'tab-detail on' })
            bf2 = BeautifulSoup(str(tab_on), features = "lxml")
            # get next page url
            zp_pages = bf2.find('div', attrs={ "class": 'zp_pages' })
            bf = BeautifulSoup(str(zp_pages), features = "lxml")
            pages = bf.find('a', attrs={ "id": 'lg_nextpage' })
            try:
                bf = BeautifulSoup(str(pages), features = "lxml")
                next_page = bf.a['href']
            except:
                next_page = ""
            finally:
                books = bf2.find_all('div', attrs={ "class": 'zp-book-item' })
                for book in books:
                    bf3 = BeautifulSoup(str(book), features = "lxml")
                    url = bf3.a['href']
                    title = bf3.h2.string
                    book_list.append({
                        "url" : url,
                        "title" : title,
                    })
    
    # type 3
    if len(book_list) == 0:
        req = requests.get(url = url)
        req.encoding = 'utf8'
        html = req.text
        bf1 = BeautifulSoup(html, features = "lxml")
        books = bf1.find_all('div', attrs={ "class": 'bookbar' })
        for book in books:
            bf2 = BeautifulSoup(str(book), features = "lxml")
            url = bf2.a['href']
            title = re.findall(r"《(.*)》全集在线阅读", bf2.h3.a.string)[0]
            book_list.append({
                "url" : url,
                "title" : title,
            })
    return book_list

def get_download_url(url):
    try:
        # first step
        req = requests.get(url = url)
        req.encoding = 'utf8'
        html = req.text
        bf1 = BeautifulSoup(html, features = "lxml")
        if bf1.find('div', attrs={ "class": 'btn-group' }) != None:
            btn_group = bf1.find('div', attrs={ "class": 'btn-group' })
            bf2 = BeautifulSoup(str(btn_group), features = "lxml")
            buttons = bf2.find_all('a')
            bf3 = BeautifulSoup(str(buttons[2]), features = "lxml")
            download_page = bf3.a['href']
        else:
            down = bf1.find('div', attrs={ "class": 'down' })
            bf2 = BeautifulSoup(str(down), features = "lxml")
            download_page = bf2.a['href']

        # second step
        req = requests.get(url = download_page)
        req.encoding = 'utf8'
        html = req.text
        bf1 = BeautifulSoup(html, features = "lxml")
        info = bf1.find('div', attrs={ "class": 'xzxx' })
        bf2 = BeautifulSoup(str(info), features = "lxml")
        buttons = bf2.find_all('p')
        bf3 = BeautifulSoup(str(buttons[4]), features = "lxml")
        download_url = bf3.a['href']
        return download_url
    except:
        return ""

if __name__ == "__main__":
    # set cookie
    headers = {
        "Cookie" : '__cfduid=d8e3c4012936e04db5a42fd7f3f0a11701617636299; atsrsmlusername=jiangmeng; atsrsmluserid=601404; atsrsmlgroupid=1; atsrsmlrnd=HTjaavuXyJgvn2KeijMu; atsrsmlauth=17fbf84dbc204ae3b4b88fb340acc563',
    }

    # test cases
    # book_list = get_book_list('http://dongyeguiwu.zuopinj.com/')
    # book_list = get_book_list('http://zuopinj.com/kb/lilinqi/')
    # print(book_list)
    # url = get_download_url('http://xushengzhi.zuopinj.com/5580/')
    # print(url)

    # get writers
    writer_list = get_writer_list()
    print("一共有 %d 个作家。" % len(writer_list))
    for writer in writer_list:
        dir = os.path.join(os.getcwd(), "docs", "zuopinj", writer["author"])
        if not os.path.exists(dir):
            os.mkdir(dir)
        # get books of each writer
        book_list = get_book_list(writer["url"])
        if len(book_list) == 0:
            print(writer)
        for book in book_list:
            save_path = os.path.join(dir, book["title"] + ".txt")
            if not os.path.exists(save_path):
                # download each book (.txt)
                download_url = get_download_url(book["url"])
                if download_url != "":
                    try:
                        r = requests.get(download_url, headers=headers)
                        with open(save_path, "wb") as file:
                            file.write(r.content)
                        print(book["title"])
                    except:
                        print(book["title"], download_url)
                else:
                    print(book["title"] + "【下载失败】")
