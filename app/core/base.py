#!/usr/bin/enc python
# encoding: utf-8

from conf import DB_PWD, DB_USER, DB_HOST, DB_NAME

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    @property
    def backend(self):
        return Backend.instance()

class WithBackend(object):
    @property
    def backend(self):
        return Backend.instance()


class Backend(object):
    def __init__(self):
        engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
            (DB_USER, DB_PWD, DB_HOST, DB_NAME),
            encoding='utf-8', echo=False,
            pool_size=100, pool_recycle=10)
        self._session = sessionmaker(bind=engine, 
                autocommit=False, autoflush=False)

    @classmethod
    def instance(cls):
        """Singleton db object"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def get_session(self):
        return self._session()
