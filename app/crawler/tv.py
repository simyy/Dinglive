#!/usr/bin/env python
# encoding: utf-8

import json
import random
from datetime import datetime

from base import BaseCrawl


class ZhanqiCrawl(BaseCrawl):
    source_id = 1
    name = '战旗TV'
    def __init__(self):
        super(ZhanqiCrawl, self).__init__(method='get')

    def run(self, count=300):
        url = "http://www.zhanqi.tv/api/static/live.hots/{size}-{page}.json"
        return super(ZhanqiCrawl, self).run(url, count=count)

    def parse(self, html):
        json_doc = json.loads(html)
        if 'code' not in json_doc or json_doc['code'] != 0:
            return None
        if 'rooms' not in json_doc['data']:
            return None
        items = list()
        for item in json_doc['data']['rooms']:
            url = "http://www.zhanqi.tv%s"
            tmp = {
                'anchor': item['nickname'],
                'avatar': item['avatar'] + '-big',
                'room_id': item['id'],
                'room_name': item['title'],
                'room_site': url % item['url'],
                'update_time': datetime.now(),
                'is_online': 1,
                'fans_count': 0,
                'audience_count': item['online'],
                'category_id': item['gameName'],
                'source_id': self.source_id,
            }
            items.append(tmp)
        return items


class PandaCrawl(BaseCrawl):
    source_id = 2
    name = '熊猫TV'
    def __init__(self):
        super(PandaCrawl, self).__init__(method='get')

    def run(self, count=300):
        url = "http://www.panda.tv/live_lists?status=2&order=person_num&pageno={page}&pagenum={size}"
        return super(PandaCrawl, self).run(url, count=count)

    def parse(self, html):
        json_doc = json.loads(html)
        if 'errno' not in json_doc or json_doc['errno'] != 0:
            return None
        if 'data' not in json_doc or 'items' not in json_doc['data']:
            return None
        items = list()
        for item in json_doc['data']['items']:
            url = "http://www.panda.tv/%s" % item['id']
            tmp = {
                'anchor': item['userinfo']['nickName'],
                'avatar': item['userinfo']['avatar'],
                'room_id': item['id'],
                'room_name': item['name'],
                'room_site': url,
                'update_time': datetime.now(),
                'is_online': 1,
                'fans_count': 0,
                'audience_count': item['person_num'],
                'category_id': item['classification']['cname'],
                'source_id': self.source_id,
            }
            items.append(tmp)
        return items


if __name__ == '__main__':
    ZhanqiCrawl().run(maxCount=100)
