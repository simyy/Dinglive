#!/usr/bin/env python
# encoding: utf-8

import time
import json
import random
from datetime import datetime
from bs4 import BeautifulSoup

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


class DouyuCrawl(BaseCrawl):
    source_id = 3
    name = '斗鱼TV'
    def __init__(self):
        super(DouyuCrawl, self).__init__(method='get')

    def run(self, count=300):
        url = "http://www.douyu.com/directory/all?page={page}&isAjax=1"
        return super(DouyuCrawl, self).run(url, count=count)

    def _get_avatar_url(self, room_site):
        print 'get avatar url:%s' % room_site
        try:
            html = self._get(room_site)
            time.sleep(random.randrange(3))
            if not html:
                return None
            soup = BeautifulSoup(html)
            if soup.find('div', attrs={'class':'anchor-pic'}) is None:
                return soup.find('img', attrs={'class':'room_pic'}).attrs['src']
            return soup.find('div', attrs={'class':'anchor-pic'}).img.attrs['src']
        except Exception as e:
            print e
        return 'http://apic.douyucdn.cn/upload/avatar/default/01_middle.jpg'

    def parse(self, html):
        items = list()
        soup = BeautifulSoup(html)
        lis = soup.findAll('li')
        for li in lis:
            anchor = li.find('span', attrs={'class':'dy-name'}).text
            room_id = li.attrs['data-rid']
            room_name = li.find('a').attrs['title']
            room_site = "http://www.douyu.com/%s" % room_id
            audience_count = li.find('span', attrs={'class':'dy-num'}).text
            category_id = li.find('span', attrs={'class':'tag'}).text
            source_id = self.source_id
            if audience_count[-1] == u'万' or audience_count[-1] == '万':
                audience_count = float(audience_count[:-1]) * 10000
            avatar = None
            if room_id == '641634':
                avatar = "http://apic.douyucdn.cn/upload/avatar/face/201606/25/f96b638d35af3ee7c31129e80da97236_middle.jpg"
            items.append({
                'anchor': anchor,
                'avatar': avatar,
                'room_id': room_id,
                'room_name': room_name,
                'room_site': room_site,
                'update_time': datetime.now(),
                'is_online': 1,
                'fans_count': 0,
                'audience_count': audience_count,
                'category_id': category_id,
                'source_id': self.source_id,
            })
        return items


if __name__ == '__main__':
    DouyuCrawl().run(count=100)
