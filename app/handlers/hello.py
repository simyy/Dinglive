#!/usr/bin/env python
# encoding: utf-8

from common.base import BaseHandler
from models.tables import Student

import tornado.web


class HelloHandler(BaseHandler):
    def get(self):
        #session = self.backend.get_session()
        #student = Student(name='jack', age=99)
        #session.add(student)
        #session.commit()
        self.write("hello")
