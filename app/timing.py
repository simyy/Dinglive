#!/usr/bin/env python
# encoding: utf-8

from core.base import WithBackend
from models.tables import TV, TVCtg

from sqlalchemy import func

from datetime import datetime
from datetime import timedelta


class Timing(WithBackend):
    def __init__(self):
        pass

    def off_line(self):
        session = self.backend.get_session()
        minutes_ago = datetime.now() - timedelta(minutes=21)
        session.query(TV).filter(TV.update_time < minutes_ago).\
                update({'is_online':0})
        session.commit()

    def calc_category_count(self):
        session = self.backend.get_session()
        rows = session.query(TVCtg.id).all()
        ctg_id_list = [x[0] for x in rows]
        print ctg_id_list
        rows = session.query(TV.category_id, func.count(TV.id).label('count')).\
            filter(TV.is_online==1).group_by(TV.category_id).all()
        for row in rows:
            session.query(TVCtg).filter(TVCtg.id==row[0]).update({TVCtg.count:row[1]}) 
            session.commit()
            ctg_id_list.remove(row[0])
        for ctg_id in ctg_id_list:
            session.query(TVCtg).filter(TVCtg.id==ctg_id).update({TVCtg.count:0})
            session.commit()

    def run(self):
        self.off_line()
        self.calc_category_count()


if __name__ == '__main__':
    print 'timing start:', datetime.now()
    Timing().run()
    print 'timing end:', datetime.now()

