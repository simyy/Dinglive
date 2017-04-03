#!/usr/bin/env python
# encoding: utf-8

from core.base import WithBackend
from models.tables import TV, TVCtg
from common.utils import yellow
from common.utils import current

from sqlalchemy import func
from datetime import datetime
from datetime import timedelta
import conf
import sys


class Clear(WithBackend):
    def __init__(self):
        pass

    def off_line(self, minutes):
        session = self.backend.get_session()
        minutes_ago = datetime.now() - timedelta(minutes=minutes)
        session.query(TV)\
            .filter(TV.update_time < minutes_ago)\
            .update({'is_online': 0})
        session.commit()

    def calc_category_count(self):
        session = self.backend.get_session()
        rows = session.query(TVCtg.id).all()
        ctg_id_list = [x[0] for x in rows]
        rows = session.query(
                TV.category_id, func.count(TV.id).label('count'))\
            .filter(TV.is_online == 1)\
            .group_by(TV.category_id).all()
        for row in rows:
            session.query(TVCtg)\
                .filter(TVCtg.id == row[0])\
                .update({TVCtg.count: row[1]})
            session.commit()
            ctg_id_list.remove(row[0])
        for ctg_id in ctg_id_list:
            session.query(TVCtg)\
                .filter(TVCtg.id == ctg_id)\
                .update({TVCtg.count: 0})
            session.commit()

    def run(self, env):
        print yellow('-> 开始清洗和统计 %s' % current())
        period = conf.SPIDER_PERIOD.get(env)
        minutes = period / 60
        if minutes <= 1:
            minutes = 30
        self.off_line(minutes)
        self.calc_category_count()
        print yellow('-> 完成清洗和统计 %s' % current())


if __name__ == '__main__':
    env = sys.argv[1] if len(sys.argv) > 1 else conf.TEST
    Clear().run(env)
