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
        url = "https://www.douyu.com/directory/all?page={page}&isAjax=1"
        return super(DouyuCrawl, self).run(url, count=count)

    def _get_avatar_url(self, room_site, default=True):
        if default:
            return 'http://apic.douyucdn.cn/upload/avatar/default/01_middle.jpg'

        # print 'get avatar url:%s' % room_site
        avatar = None
        try:
            html = self._get(room_site)
            time.sleep(random.randrange(3))
            if not html:
                return default
            soup = BeautifulSoup(html)
            if soup.find('div', attrs={'class': 'anchor-pic'}) is None:
                avatar = soup.find('img', attrs={'class': 'room_pic'})\
                    .attrs['src']
            else:
                avatar = soup.find('div', attrs={'class': 'anchor-pic'})\
                    .img.attrs['src']
            if avatar:
                return avatar
        except Exception as e:
            print e
        return default
        # return 'http://apic.douyucdn.cn/upload/avatar/default/01_middle.jpg'

    def parse(self, html):
        items = list()
        soup = BeautifulSoup(html)
        lis = soup.findAll('li')
        for li in lis:
            anchor = li.find('span', attrs={'class': 'dy-name'}).text
            room_id = li.attrs['data-rid']
            room_name = li.find('a').attrs['title']
            room_site = "http://www.douyu.com/%s" % room_id
            audience_count = li.find('span', attrs={'class': 'dy-num'}).text
            category_id = li.find('span', attrs={'class': 'tag'}).text
            if audience_count[-1] == u'万' or audience_count[-1] == '万':
                audience_count = float(audience_count[:-1]) * 10000
            avatar = None
            if audience_count > 100000:
                avatar = self._get_avatar_url(room_site, default=False)
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


class HuyaCrawl(BaseCrawl):
    source_id = 4
    name = '虎牙TV'

    def __init__(self):
        super(HuyaCrawl, self).__init__(method='get')

    def run(self, count=300):
        url = "http://www.huya.com/cache.php?m=Live&do=ajaxAllLiveByPage&page={page}&pageNum=1"
        return super(HuyaCrawl, self).run(url, count=count)

    def parse(self, html):
        json_doc = json.loads(html)
        if 'status' not in json_doc or json_doc['status'] != 200:
            return None
        if 'list' not in json_doc['data']:
            return None
        items = list()
        for item in json_doc['data']['list']:
            url = "http://www.huya.com/%s"
            tmp = {
                'anchor': item['nick'],
                'avatar': item['avatar180'],
                'room_id': item['privateHost'],
                'room_name': item['roomName'],
                'room_site': url % item['privateHost'],
                'update_time': datetime.now(),
                'is_online': 1,
                'fans_count': 0,
                'audience_count': item['totalCount'],
                'category_id': item['gameFullName'],
                'source_id': self.source_id,
            }
            items.append(tmp)
        return items


class LongzhuCrawl(BaseCrawl):
    source_id = 5
    name = '龙珠TV'

    def __init__(self):
        super(LongzhuCrawl, self).__init__(method='get')

    def run(self, count=300):
        url = "http://api.plu.cn/tga/streams?max-results=120&start-index={start_index}&sort-by=views"
        result = list()
        start_index = 0
        num = 0
        while num < count:
            tmp_url = url.format(start_index=start_index)
            start_index += 120
            res = self.load(tmp_url)
            print 'load\turl:%s' % tmp_url
            if not res or len(res) == 0:
                break
            num += len(res)
            print 'num:', num
            if res:
                result.extend(res)
            time.sleep(random.randrange(10))
        self.save(result)

    def parse(self, html):
        json_doc = json.loads(html)
        if 'data' not in json_doc:
            return None
        items = list()
        for item in json_doc['data']['items']:
            tmp = {
                'anchor': item['channel']['name'],
                'avatar': item['channel']['avatar'],
                'room_id': item['channel']['id'],
                'room_name': item['channel']['status'],
                'room_site': item['channel']['url'],
                'update_time': datetime.now(),
                'is_online': 1,
                'fans_count': item['channel']['followers'],
                'audience_count': item['viewers'],
                'category_id': item['game'][0]['Name'],
                'source_id': self.source_id,
            }
            items.append(tmp)
        return items


class QuanminCrawl(BaseCrawl):
    source_id = 6
    name = '全民直播'

    def __init__(self):
        super(QuanminCrawl, self).__init__(method='get')

    def run(self, count=300):
        url = "http://www.quanmin.tv/json/play/{list_page}.json"
        result = list()
        page = 0
        num = 0
        while num < count:
            if page == 0:
                list_page = 'list'
            else:
                list_page = 'list_%d' % page
            page += 1
            tmp_url = url.format(list_page=list_page)
            res = self.load(tmp_url)
            print 'load\turl:%s' % tmp_url
            if not res or len(res) == 0:
                break
            num += len(res)
            print 'num:', num
            if res:
                result.extend(res)
            time.sleep(random.randrange(10))
        self.save(result)

    def parse(self, html):
        json_doc = json.loads(html)
        if 'data' not in json_doc:
            return None
        items = list()
        for item in json_doc['data']:
            tmp = {
                'anchor': item['nick'],
                'avatar': item['avatar'],
                'room_id': item['uid'],
                'room_name': item['title'],
                'room_site': "http://www.quanmin.tv/v/%s" % item['uid'],
                'update_time': datetime.now(),
                'is_online': 1,
                'fans_count': item['follow'],
                'audience_count': item['view'],
                'category_id': item['category_name'],
                'source_id': self.source_id,
            }
            items.append(tmp)
        return items


class HuomaoCrawl(BaseCrawl):
    source_id = 7
    name = '火猫直播'

    def __init__(self):
        super(HuomaoCrawl, self).__init__(method='get')

    def _get_avatar_url(self, room_site, default=True):
        return "http://www.huomao.com/static/web/images/default_headimg/default_head_normal.jpg"

    def parse(self, html):
        json_doc = json.loads(html)
        if 'data' not in json_doc:
            return None
        items = list()
        for item in json_doc['data']['channelList']:
            audience_count = item['views']
            if audience_count[-1] == u'万' or audience_count[-1] == '万':
                audience_count = float(audience_count[:-1]) * 10000
            elif "," in audience_count:
                audience_count = int(audience_count.replace(",", ""))
            else:
                audience_count = int(audience_count)
            tmp = {
                'anchor': item['nickname'],
                'avatar': self._get_avatar_url(audience_count),
                'room_id': item['room_number'],
                'room_name': item['channel'],
                'room_site': "http://www.huomao.com/%s" % item['room_number'],
                'update_time': datetime.now(),
                'is_online': 1,
                'fans_count': 0,
                'audience_count': audience_count,
                'category_id': item['gameCname'],
                'source_id': self.source_id,
            }
            items.append(tmp)
        return items

    def run(self, count=300):
        url = "http://www.huomao.com/channels/channel.json?page={page}&page_size=120&game_url_rule=all"
        return super(HuomaoCrawl, self).run(url, count=count)


crawlers = {
    'zq': ZhanqiCrawl(),
    'lz': LongzhuCrawl(),
    'pd': PandaCrawl(),
    'qm': QuanminCrawl(),
    'hy': HuyaCrawl(),
    'dy': DouyuCrawl(),
    'hm': HuomaoCrawl(),
}


if __name__ == '__main__':
    # ZhanqiCrawl().run(count=100)
    # PandaCrawl().run(count=100)
    # DouyuCrawl().run(count=100)
    # HuyaCrawl().run(count=100)
    # LongzhuCrawl().run(count=100)
    # QuanminCrawl().run(count=100)
    HuomaoCrawl().run(count=100)
