#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.options import define, options

from handlers import tv
from core.base import JinjaLoader
from core.base import BaseHandler


define('port', default=4000, help="server port", type=int)

handlers = [
    (r'/', tv.Index),
    (r'/tv/cate/(.+)/list', tv.ListAjax),
    (r'/cate', tv.Cate),
    (r'/quality', tv.QualityIndex),
    (r'/cate/(.+)', tv.CateIndex),
    (r'/room/', tv.RoomIndex),
    (r'/search/(.+)', tv.SearchIndex),
]


class My404Handler(BaseHandler):
    def prepare(self):
        self.set_status(404)
        self.render("404.html")


tornado.web.ErrorHandler = My404Handler


def main(debug):
    app = tornado.web.Application(
            handlers, template_loader=JinjaLoader(
                os.path.join(os.path.dirname(__file__), 'templates/')),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            default_handler_class=My404Handler,
            debug=debug)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    debug = False
    if len(sys.argv) == 2:
        if sys.argv[1] == 'debug':
            debug = True
    main(debug)
