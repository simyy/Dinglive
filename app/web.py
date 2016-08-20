#!/usr/bin/env python
# encoding: utf-8

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.options import define, options

from handlers.hello import HelloHandler
from handlers import tv
from core.base import JinjaLoader
from core.base import BaseHandler


define('port', default=4000, help="server port", type=int)

handlers = [
    (r'/hello', HelloHandler),
    (r'/', tv.IndexHandler),
    (r'/tv/ctg/([0-9]+)/list', tv.ListHandler),
    (r'/ctg', tv.Category),
    (r'/ctg/([0-9]+)', tv.CtgList),
    (r'/search/(.+)', tv.SearchIndex),
]


class My404Handler(BaseHandler):
    def prepare(self):
        self.set_status(404)
        self.render("404.html")


tornado.web.ErrorHandler = My404Handler


def main():
    app = tornado.web.Application(
            handlers, template_loader=JinjaLoader(
                os.path.join(os.path.dirname(__file__), 'templates/')),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            default_handler_class=My404Handler,
            debug=False)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
