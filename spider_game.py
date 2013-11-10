#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
A multiprocessing Spider
http://www.pythonclub.org/python-network-application/observer-spider
http://blog.csdn.net/xihuanqiqi/article/details/11579853
"""

import urllib.request
from pyquery import PyQuery

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
    data = PyQuery(feed_data)
    if data :
        parse_pov_table(data("table#att_pov_table"))
    return id

def parse_pov_table(table):
    pq_element = PyQuery(table)
    #row = 1
    #th_query = 'th:eq(%d)' % row
    #td_query = 'td:eq(%d)' % row
    #http://pythonhosted.org/pyquery/api.html#pyquery.pyquery.PyQuery.items
    for row in table.items('tr'):
        if row('th').text() == '傾向':
            tuples = row('td').text().split(' , ')
            #links = row('td a:eq(1)').attr('href')
            #print(links)
            for (offset, tuple) in enumerate(tuples):
            #for tuple in tuples:
                str = tuple.strip().split(' ')
                zokusei = str[0]
                if len(str) > 1:
                    number = int(re.split('(\d+)', str[1])[1])
                else:
                    number = 1
                pov_id = int(row("td a:eq(%d)" % offset).attr('href').split('#pov')[1])
                print(zokusei + "(%d): %d" % (pov_id, number))

def gzip_decode_content(doc = ""):
    try:
        html = gzip.decompress(doc).decode("utf-8") #decode
    except:
        html = doc.decode("utf-8")
    return html

def main():
    get_game_info(7062, url)
    pool = multiprocessing.Pool(processes=4)
    result = []
    #for i in range(7062, 7063):
        #result.append(pool.apply_async(get_game_info, (i, url, )))
    #pool.close()
    #pool.join()
    #for res in result:
        #print(res.get())

if __name__ == "__main__":
    main()