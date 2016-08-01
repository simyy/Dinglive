#!/usr/bin/env python
# encoding: utf-8

import requests


class BaseCrawl(object):
    def __init__(self, url, method='get'):
        self.url = url
        self.method = method

    def run(self, kwargs=None):
        if self.method == 'get':
            r = self._get(self.url, kwargs=kwargs)
        else:
            r = self._post(self.url, kwargs=kwargs)
        if r:
            return self.parse(r)
        return None

    def parse(self, html):
        pass

    def _get(self, url, kwargs=None):
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        return None

    def _post(self, url, kwargs=None):
        r = requests.post(url, kwargs)
        if r.status_code == 200:
            return r.text
        return None
