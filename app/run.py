#!/usr/bin/env python
# encoding: utf-8

from handlers.hello import HelloHandler
from crawler.tv import PandaCrawl

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.options import define, options

import urllib
import json
import datetime
import time


define('port', default=8000, help="server port", type=int)


handlers = [
    ('/', HelloHandler),
]


def main():
    app = tornado.web.Application(handlers) 
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    #main()
    PandaCrawl().run()
