#!/usr/bin/env python
# encoding: utf-8

from functools import wraps

import json


def jsonize(func):
    @wraps(func)
    def deco(*args, **kwargs):
        r = func(*args, **kwargs)
        if isinstance(r, dict):
            return json.dumps(r)
        return r
    return deco
