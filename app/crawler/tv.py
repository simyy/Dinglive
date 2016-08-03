#!/usr/bin/env python
# encoding: utf-8

import json
import random

from base import TVRoom
from base import BaseCrawl


class ZhanqiCrawl(BaseCrawl):
    src_id = 0
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
            ctg_id = 0
            room = TVRoom(
                item["code"],
                item['title'],
                item['nickname'],
                item['avatar'] + '-big',
                item['gender'],
                item['url'],
                item['spic'],
                item['online'],
                ctg_id,
                self.src_id)
            rooms.append(room)
        return rooms 


class PandaCrawl(BaseCrawl):
    src_id = 1
    name = '熊猫TV'
    def __init__(self):
        super(PandaCrawl, self).__init__(method='get')

    def run(self, maxCount=300):
        url = "http://www.panda.tv/live_lists?status=2&order=person_num&pageno={page}&pagenum={size}"
        return super(PandaCrawl, self).run(url)

    def parse(self, html):
        json_doc = json.loads(html)
        if 'errno' not in json_doc or json_doc['errno'] != 0:
            return None
        if 'data' not in json_doc or 'items' not in json_doc['data']:
            return None
        rooms = list()
        for item in json_doc['data']['items']:
            ctg_id = 0
            url = "http://www.panda.tv/%s" % item['id']
            room = TVRoom(
                item['id'],
                item['name'],
                item['userinfo']['nickName'],
                item['userinfo']['avatar'],
                -1,
                url,
                item['pictures']['img'],
                item['person_num'],
                ctg_id,
                self.src_id)
            rooms.append(room)
        return rooms


if __name__ == '__main__':
    print ZhanqiCrawl().run(maxCount=100)
    print PandaCrawl().run()
