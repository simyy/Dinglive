#!/usr/bin/env python
# encoding: utf-8

from core.base import WithBackend
from models.tables import TV

from datetime import datetime
from datetime import timedelta


class Timing(WithBackend):
    def __init__(self):
        pass

    def run(self):
        session = self.backend.get_session()
        minutes_ago = datetime.now() - timedelta(minutes=12)
        session.query(TV).filter(TV.update_time < minutes_ago).\
                update({'is_online':0})
        session.commit()


if __name__ == '__main__':
    Timing().run()

