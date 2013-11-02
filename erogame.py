#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
多线程抓取网页
"""

import gzip
from urllib import request as urllib2

import threading

from pyquery import PyQuery as pq

threads = []
web_site_url = "http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/comment.php"

def work(url):
    """
    callback function
    """
    # 出现urllib2.HTTPError: HTTP Error 403: Forbidden错误是由于网站禁止爬虫，
    # 可以在请求加上头信息，伪装成浏览器访问伪装浏览器头
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    if not url:
        url = web_site_url
    req = urllib2.Request(url=url, headers = headers)
    feed_data = urllib2.urlopen(req).read()
    feed_data = gzip_decode_content(feed_data)
    data = pq(feed_data)
    get_next_page(data)
    if data :
        data("div.coment div").each(parse_html)


def parse_html(i, element):
    pq_element = pq(element)
    score = pq_element("span.red").text()

    if (i % 2 == 0):
        user_link = pq_element("p.footer2 a").attr("href")
        user_name = pq_element("p.footer2 > a").text()
        game_title = pq_element("p.comment2 span.futoji a").text()
        play_time = pq_element("p.play_time.footer2").text()
        if (play_time):
            date_str = pq_element("p.play_time.footer2 + p.footer2").text()
        else:
            date_str = pq_element("p.footer2").text()

    else:
        user_link = pq_element("p.footer1 a").attr("href")
        user_name = pq_element("p.footer1 > a").text()
        game_title = pq_element("p.comment1 span.futoji a").text()
        play_time = pq_element("p.play_time.footer1").text()
        if (play_time):
            date_str = pq_element("p.play_time.footer1 + p.footer1").text()
        else:
            date_str = pq_element("p.footer1").text()

    if (date_str) :
        date_str = date_str.split(" ")[0].strip()
    print("%s\t%s\t%s\t%s" % (score, game_title, date_str, user_name))

def get_next_page(data):
    if data :
        page_li = data("td:eq(1) h2 + p")
        if page_li :
            page_params = page_li.find("a").attr("href")
            next_page_url = web_site_url + page_params
            threading.Thread(target=work, args=(next_page_url, )).start()


def gzip_decode_content(doc=""):
    """
    根据URL返回内容，有些页面可能需要 gzip 解压缩
    """

    try:
        html = gzip.decompress(doc).decode("utf-8") #decode
    except:
        html=doc.decode("utf-8")
    return html


def main():
    work(())

if __name__ == "__main__":
    main()