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
            filter(TV.source_id==TVSrc.id, TV.category_id==TVCtg.id).\
            order_by(TV.audience_count.desc()).\
            all()[:10]
        self.render('index.html')


class RoomHandler(BaseHandler):
    def get(self):
        last_id = self.get_argument('last_id', default=None)
        session = self.backend.get_session()
        if last_id:
            self.rows = session.query(TV, TVCtg.name, TVSrc.pic).\
                filter(TV.id>last_id, TV.source_id==TVSrc.id, TV.category_id==TVCtg.id).\
                order_by(TV.audience_count.desc()).\
                all()[:10]
        else:
            self.rows = session.query(TV, TVCtg.name, TVSrc.pic).\
                filter(TV.source_id==TVSrc.id, TV.category_id==TVCtg.id).\
                order_by(TV.audience_count.desc()).\
                all()[:10]
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
