# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: P♂boy
@License: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@Contact: 17647361832@163.com
@Software: Pycharm
@File: spider100.py
@Time: 2019/1/25 22:12
@Desc:
"""
import json
from multiprocessing import Pool
import requests
import re
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text

    except RequestException:
        return None
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?title="(.*?)"'
                         '.*?<img data-src="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>', re.S)
    items  = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'title': item[1],
            'image': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
        }
    # print(items)
    # print('---')

def write_in_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
def main(offset):
    url = 'https://maoyan.com/board/4?offset=%d'%(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_in_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [offset * 10 for offset in range(10)])