#!/usr/bin/env python
# encoding: utf-8

from core.base import BaseHandler
from core.base import TTemplate
from core.base import Response
from models.tables import TV
from models.tables import TVCtg
from models.tables import TVSrc

import tornado.web


class IndexHandler(BaseHandler):
    def get(self):
        session = self.backend.get_session()
        self.rows = session.query(TV, TVCtg.name, TVSrc.pic).\
            filter(TV.source_id==TVSrc.id, TV.category_id==TVCtg.id, TV.is_online==1).\
            order_by(TV.audience_count.desc()).\
            all()[:10]
        self.render('list.html')


class ListHandler(BaseHandler):
    def get(self, ctg_id):
        page = int(self.get_argument('page', default=0))
        session = self.backend.get_session()
        ctg_id = int(ctg_id)
        print page, ctg_id
        if ctg_id == 0:
            self.rows = session.query(TV, TVCtg.name, TVSrc.pic).\
                filter(TV.source_id==TVSrc.id, TV.category_id==TVCtg.id,
                    TV.is_online==1).\
                order_by(TV.audience_count.desc()).\
                all()[page*10:(page+1)*10]
        else:
            self.rows = session.query(TV, TVCtg.name, TVSrc.pic).\
                filter(TV.source_id==TVSrc.id, TV.category_id==TVCtg.id, 
                    TV.is_online==1, TV.category_id==ctg_id).\
                order_by(TV.audience_count.desc()).\
                all()[page*10:(page+1)*10]
        response = Response()
        if not self.rows:
            data = None
        else:
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
                    'source': row[2],
                }) 
            response.set_data(data)
        self.write(response.jsonize())

class Category(BaseHandler):
    def get(self):
        session = self.backend.get_session()
        self.rows = session.query(TVCtg).order_by(TVCtg.count.desc()).all()
        self.render('category.html')


class CtgList(BaseHandler):
    def get(self, ctg_id):
        print ctg_id
        session = self.backend.get_session()
        self.rows = session.query(TV, TVCtg.name, TVSrc.pic).\
            filter(TV.source_id==TVSrc.id, TV.category_id==TVCtg.id,
                TV.is_online==1, TV.category_id==ctg_id).\
            order_by(TV.audience_count.desc()).\
            all()[:10]
        self.render('list.html')

