#!/usr/bin/enc python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado import template, web
from conf import DB_PWD, DB_USER, DB_HOST, DB_NAME
from core import decorator

import jinja2
import threading


SUCCESS = 0

ERROR_PARAM = 3001
ERROR_SERV = 3002


class Response(object):
    def __init__(self, code=0, msg='OK'):
        self.code = code
        self.msg = msg
        self.data = None

    def set_data(self, data):
        if data and not isinstance(data, dict) and not isinstance(data, list):
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


class SuccessResponse(Response):
    def __init__(self, data):
        super(SuccessResponse, self).__init__(code=SUCCESS, msg='OK')
        self.set_data(data)


class ErrorResponse(Response):
    def __init__(self, code, msg):
        super(ErrorResponse, self).__init__(code=code, msg=msg)
