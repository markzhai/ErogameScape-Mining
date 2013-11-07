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
import re
#import reposity

url = "http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/game.php?game="

def get_game_info(id, url):
    """
    get game information by given id
    """
    # 在请求加上浏览器头信息，伪装成浏览器访问
    headers = {'User-Agent':      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
               'Accept-Encoding': 'gzip'}
    url = '%s%s' % (url, id)
    req = urllib.request.Request(url = url, headers = headers)
    feed_data = urllib.request.urlopen(req).read()
    feed_data = gzip_decode_content(feed_data)
    feed_data = feed_data[39:]  #remove <?xml version="1.0" encoding="utf-8" ?>
    #print(feed_data)
    #fp = open("spider-game.html", "wb")
    #fp.write(bytes(feed_data, 'UTF-8'))
    #fp.close()
    data = pq(feed_data)
    if data :
        parse_html(data("table#att_pov_table"))
    return id

def parse_html(element):
    pq_element = pq(element)

    row = 1
    th_query = 'th:eq(%d)' % row
    td_query = 'td:eq(%d)' % row

    attribute = pq_element(th_query).text()
    contents = pq_element(td_query).text()
    while attribute:
        if attribute == '傾向':
            print(contents)
            elements = re.split(',', contents)
            for item in elements:
                str = item.strip().split(' ')
                zokusei = str[0]
                if len(str) > 1:
                    number = int(re.split('(\d+)', str[1])[1])
                else:
                    number = 1
                print(zokusei + ": %d" % number)
        row += 1
        th_query = 'th:eq(%d)' % row
        td_query = 'td:eq(%d)' % row
        attribute = pq_element(th_query).text()
        contents = pq_element(td_query).text()

def gzip_decode_content(doc=""):
    try:
        html = gzip.decompress(doc).decode("utf-8") #decode
    except:
        html = doc.decode("utf-8")
    return html

def main():
    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in range(7062, 7063):
        result.append(pool.apply_async(get_game_info, (i, url, )))
    pool.close()
    pool.join()
    #for res in result:
        #print(res.get())

if __name__ == "__main__":
    main()