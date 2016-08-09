#!/usr/bin/enc python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado import template, web
from conf import DB_PWD, DB_USER, DB_HOST, DB_NAME
from core import decorator

import json
import jinja2
import threading


class Response(object):
    def __init__(self, code=0, msg='OK'):
        self.code = code
        self.msg = msg
        self.data = None

    def set_data(self, data):
        if data and not isinstance(data, dict) and \
            not isinstance(data, list):
            raise Exception("Response data must be a dict")
        self.data = data

    @decorator.jsonize
    def jsonize(self):
        result = {
            'code': self.code,
            'msg': self.msg,
            'data': self.data,
        }
        return result


class BaseHandler(web.RequestHandler):
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


class TTemplate(object):
    def __init__(self, template_instance):
        self.template_instance = template_instance

    def generate(self, **kwargs):
        return self.template_instance.render(**kwargs)


class JinjaLoader(template.BaseLoader):
    def __init__(self, root_directory, **kwargs):
        self.jinja_env = \
        jinja2.Environment(loader=jinja2.FileSystemLoader(root_directory), **kwargs)
        self.templates = {}
        self.lock = threading.RLock()

    def resolve_path(self, name, parent_path=None):
        return name

    def _create_template(self, name):
        template_instance = TTemplate(self.jinja_env.get_template(name))
        return template_instance
