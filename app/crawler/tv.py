#!/usr/bin/env python
# encoding: utf-8

import json
import random

from base import TVRoom
from base import BaseCrawl


class ZhanqiCrawl(BaseCrawl):
    src = 0
    name = '战旗TV'
    def __init__(self):
        super(ZhanqiCrawl, self).__init__(method='get')

    def run(self, maxCount=300):
        url = "http://www.zhanqi.tv/api/static/live.hots/{size}-{page}.json"
        return super(ZhanqiCrawl, self).run(url)

    def parse(self, html):
        json_doc = json.loads(html)
        if 'code' not in json_doc or json_doc['code'] != 0:
            return None
        if 'rooms' not in json_doc['data']:
            return None
        rooms = list()
        for item in json_doc['data']['rooms']:
            ganmeId = 0
            room = TVRoom(item["code"], item['title'], item['nickname'],
                item['avatar'], item['gender'], item['url'], item['spic'],
                item['online'], ganmeId, self.src)
            rooms.append(room)
        return rooms 


class PandaCrawl(BaseCrawl):
    src = 1
    name = '熊猫TV'
    def __init__(self):
        super(PandaCrawl, self).__init__(method='get')

    def run(self, maxCount=300):
        url = "http://www.panda.tv/live_lists?status=2&order=person_num&pageno={page}&pagenum={size}"
        return super(PandaCrawl, self).run(url)


if __name__ == '__main__':
    #ZhanqiCrawl().run()
    PandaCrawl().run()
