#!/usr/bin/env python
# encoding: utf-8

from core.base import BaseHandler
from core.response import SuccessResponse
from models.tables import TV
from models.tables import TVCtg
from models.tables import TVSrc
from itertools import groupby
import copy


indexSize = 25
pageSize = 10
online = 1


cates = [
    {"class": "", "img": '<img src="/static/img/Home.png"/>', "href": u"/", "text": u"全部"},
    {"class": "", "img": '<img src="/static/img/L_Letter.png"/>', "href": u"/cate/英雄联盟", "text": u"英雄联盟"},
    {"class": "", "img": '<img src="/static/img/D_Letter.png"/>', "href": u"/cate/DOTA", "text": "DOTA"},
    {"class": "", "img": '<img src="/static/img/W_Letter.png"/>', "href": u"/cate/王者荣耀", "text": u"王者荣耀"},
    {"class": "", "img": '<img src="/static/img/S_Letter.png"/>', "href": u"/cate/守望先锋", "text": u"守望先锋"},
    {"class": "", "img": '<img src="/static/img/L_Letter.png"/>', "href": u"/cate/炉石传说", "text": u"炉石传说"},
    {"class": "", "img": '<img src="/static/img/C_Letter.png"/>', "href": u"/cate/穿越火线", "text": u"穿越火线"},
    {"class": "", "img": '<img src="/static/img/P_Letter.png"/>', "href": u"/cate/跑跑卡丁车", "text": u"跑跑卡丁车"},
    {"class": "", "img": '<img src="/static/img/Y_Letter.png"/>', "href": u"/cate/娱乐天地", "text": u"娱乐天地"},
    {"class": "", "img": '<img src="/static/img/Y_Letter.png"/>', "href": u"/cate/游戏放映室", "text": u"游戏放映室"},
    {"class": "", "img": '<img src="/static/img/H_Letter.png"/>', "href": u"/cate/户外直播", "text": u"户外直播"}]


class Index(BaseHandler):
    def get(self):
        session = self.backend.get_session()
        self.rows = session.query(TV, TVCtg.name, TVSrc.pic)\
            .filter(TV.source_id == TVSrc.id, TV.category_id == TVCtg.id,
                    TV.is_online == 1)\
            .order_by(TV.audience_count.desc())\
            .all()[:indexSize]
        self.cates = copy.deepcopy(cates)
        for item in self.cates:
            if item["text"] == u"全部":
                item["class"] = "active"
                break
        self.render('list.html')


class ListAjax(BaseHandler):
    def get(self, cate):
        page = int(self.get_argument('page', default=0))
        searchStr = self.get_argument('searchStr', default=None)
        self.rows = self.list(cate, searchStr, page)
        data = list()
        for row in self.rows:
            data.append({
                'id': row[0].id,
                'room_name': row[0].room_name[:25],
                'room_site': row[0].room_site,
                'anchor': row[0].anchor,
                'avatar': row[0].avatar,
                'fans_count': row[0].fans_count,
                'audience_count': row[0].audience_count,
                'category': row[1],
                'source': row[2]})
        self.write(SuccessResponse(data).jsonize())

    def list(self, cate='all', searchStr=None, page=1, pageSize=pageSize):
        session = self.backend.get_session()
        query = session.query(TV, TVCtg.name, TVSrc.pic)\
            .filter(TV.source_id == TVSrc.id, TV.category_id == TVCtg.id,
                    TV.is_online == 1)
        if cate != 'all':
            query = query.filter(TVCtg.name == cate)
        if searchStr:
            ctgs = session.query(TVCtg)\
                .filter(TVCtg.name.like('%' + searchStr + '%'))
            if ctgs:
                ctg_ids = [x.id for x in ctgs]
                query = query.filter(TV.category_id.in_(ctg_ids))
            else:
                query = query.filter(TV.anchor.like('%' + searchStr + '%'))
        query = query.order_by(TV.audience_count.desc())
        return query[page*10: (page+1)*pageSize]


class Cate(BaseHandler):
    def get(self):
        session = self.backend.get_session()
        self.rows = session.query(TVCtg).filter(TVCtg.count > 0)\
            .order_by(TVCtg.count.desc()).all()
        self.cates = dict()
        for row in self.rows:
            if row.cate not in self.cates:
                self.cates[row.cate] = list()
            self.cates[row.cate].append(row)

        for k in self.cates:
            self.cates[k] = sorted(self.cates[k], key=lambda x: x.sort)
        self.keys = [
            u"热门游戏", u"娱乐直播", u"综合直播",
            u"单机游戏", u"网络游戏", u"移动游戏"]
        self.render('cate.html')


class CateIndex(BaseHandler):
    def get(self, cate):
        session = self.backend.get_session()
        self.rows = session.query(TV, TVCtg.name, TVSrc.pic)\
            .filter(TV.source_id == TVSrc.id, TV.category_id == TVCtg.id,
                    TV.is_online == 1, TVCtg.name == cate)\
            .order_by(TV.audience_count.desc())\
            .all()[:25]
        self.cates = copy.deepcopy(cates)
        for item in self.cates:
            if item["text"] == cate:
                item["class"] = "active"
        self.render('list.html')


class QualityIndex(BaseHandler):
    def get(self):
        self.render('quality.html')


class RoomIndex(BaseHandler):
    def get(self):
        self.src = self.get_argument('src')
        self.render('room.html')


class SearchIndex(BaseHandler):
    def get(self, searchStr):
        session = self.backend.get_session()
        query = session.query(TV, TVCtg.name, TVSrc.pic)\
            .filter(TV.source_id == TVSrc.id, TV.category_id == TVCtg.id,
                    TV.is_online == online)
        ctgs = session.query(TVCtg)\
            .filter(TVCtg.name.like('%' + searchStr + '%'))\
            .all()
        if ctgs:
            ctg_ids = [x.id for x in ctgs]
            query = query.filter(TV.category_id.in_(ctg_ids))
        else:
            query = query.filter(TV.anchor.like('%' + searchStr + '%'))

        self.rows = query.order_by(TV.audience_count.desc())[:indexSize]
        self.cates = copy.deepcopy(cates)
        self.render('list.html')
