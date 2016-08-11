#!/usr/bin/env python
# encoding: utf-8

import os
import json
import time
import urllib
import datetime

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.options import define, options

from handlers.hello import HelloHandler
from handlers import tv
from core.base import JinjaLoader


define('port', default=4000, help="server port", type=int)

handlers = [
    (r'/hello', HelloHandler),
    (r'/', tv.IndexHandler),
    (r'/tv/ctg/([0-9]+)/list', tv.ListHandler),
    (r'/ctg', tv.Category),
    (r'/ctg/([0-9]+)', tv.CtgList),
]


def main():
    app = tornado.web.Application(handlers, 
        template_loader=JinjaLoader(os.path.join(os.path.dirname(__file__), 'templates/')),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True) 
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
