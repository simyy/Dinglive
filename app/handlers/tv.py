#!/usr/bin/env python
# encoding: utf-8

from core.base import BaseHandler
from core.response import SuccessResponse
from models.tables import TV
from models.tables import TVCtg
from models.tables import TVSrc


indexSize = 25
pageSize = 10
allCtg = 0
online = 1


class Index(BaseHandler):
    def get(self):
        session = self.backend.get_session()
        self.rows = session.query(TV, TVCtg.name, TVSrc.pic)\
            .filter(TV.source_id == TVSrc.id, TV.category_id == TVCtg.id, TV.is_online == 1)\
            .order_by(TV.audience_count.desc())\
            .all()[:indexSize]
        self.render('list.html')


class List(BaseHandler):
    def get(self, ctg_id):
        page = int(self.get_argument('page', default=0))
        searchStr = self.get_argument('searchStr', default=None)
        ctg_id = int(ctg_id)
        self.rows = self.list(ctg_id, searchStr, page)
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
        response = SuccessResponse()
        response.set_data(data)
        self.write(response.jsonize())

    def list(self, ctg_id=allCtg, searchStr=None, page=1, pageSize=pageSize):
        session = self.backend.get_session()
        query = session.query(TV, TVCtg.name, TVSrc.pic)\
                .filter(TV.source_id == TVSrc.id, TV.category_id == TVCtg.id, TV.is_online == 1)
        if ctg_id != allCtg:
            query = query.filter(TV.category_id == ctg_id)
        if searchStr:
            ctgs = session.query(TVCtg).filter(TVCtg.name.like('%' + searchStr + '%'))
            if ctgs:
                ctg_ids = [x.id for x in ctgs]
                query = query.filter(TV.category_id.in_(ctg_ids))
            else:
                query = query.filter(TV.anchor.like('%' + searchStr + '%'))
        query = query.order_by(TV.audience_count.desc())
        return query[page * 10 : (page + 1) * pageSize]


class Category(BaseHandler):
    def get(self):
        session = self.backend.get_session()
        self.rows = session.query(TVCtg).order_by(TVCtg.count.desc()).all()
        self.render('category.html')


class CategoryIndex(BaseHandler):
    def get(self, ctg_id):
        session = self.backend.get_session()
        self.rows = session.query(TV, TVCtg.name, TVSrc.pic)\
            .filter(TV.source_id == TVSrc.id, TV.category_id == TVCtg.id, TV.is_online == 1, TV.category_id == ctg_id)\
            .order_by(TV.audience_count.desc())\
            .all()[:25]
        self.render('list.html')


class SearchIndex(BaseHandler):
    def get(self, searchStr):
        session = self.backend.get_session()
        query = session.query(TV, TVCtg.name, TVSrc.pic)\
            .filter(TV.source_id == TVSrc.id, TV.category_id == TVCtg.id, TV.is_online == online)
        ctgs = session.query(TVCtg).filter(TVCtg.name.like('%' + searchStr + '%')).all()
        if ctgs:
            ctg_ids = [x.id for x in ctgs]
            query = query.filter(TV.category_id.in_(ctg_ids))
        else:
            query = query.filter(TV.anchor.like('%' + searchStr + '%'))

        self.rows = query.order_by(TV.audience_count.desc())[:indexSize]
        self.render('list.html')
