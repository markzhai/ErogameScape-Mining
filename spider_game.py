#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
多线程抓取网页
http://www.pythonclub.org/python-network-application/observer-spider
http://blog.csdn.net/xihuanqiqi/article/details/11579853
"""

import urllib.request
from pyquery import PyQuery as pq

import multiprocessing
import gzip
#import reposity

url = "http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/game.php?game="

def get_game_info(id, url):
    """
    get game information by given id
    """
    # 出现urllib2.HTTPError: HTTP Error 403: Forbidden错误是由于网站禁止爬虫，
    # 可以在请求加上头信息，伪装成浏x览器访问伪装浏览器头
    headers = {'User-Agent':      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
               'Accept-Encoding': 'gzip'}
    url = '%s%s' % (url, id)
    req = urllib.request.Request(url = url, headers = headers)
    feed_data = urllib.request.urlopen(req).read()
    feed_data = gzip_decode_content(feed_data)
    feed_data = feed_data[39:]  #remove <?xml version="1.0" encoding="utf-8" ?>
    print(feed_data)
    #fp = open("spider-game.html", "wb")
    #fp.write(bytes(feed_data, 'UTF-8'))
    #fp.close()
    data = pq(feed_data)
    if data :
        parse_html(data("table#att_pov_table"))
    return "done " + id

def parse_html(element):
    pq_element = pq(element)
    score = pq_element("td").text()
    print(score)

def gzip_decode_content(doc=""):
    """
    根据URL返回内容，有些页面可能需要 gzip 解压缩
    """
    try:
        html = gzip.decompress(doc).decode("utf-8") #decode
    except:
        html = doc.decode("utf-8")
    return html

def main():
    get_game_info(7062, url)
    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in range(7062, 7064):
        result.append(pool.apply_async(get_game_info, (i, url, )))
    pool.close()
    pool.join()
    for res in result:
        print(res.get())
    print("Sub-process(es) done.")

if __name__ == "__main__":
    main()