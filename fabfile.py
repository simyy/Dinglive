#!/usr/bin/env python
# encoding: utf-8

from fabric.api import env
from fabric.api import run
from fabric.api import roles


env.roledefs = {
    'remote_server': ['root@45.77.18.107']
}


@roles('remote_server')
def restart():
    run('')
