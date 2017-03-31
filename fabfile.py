#!/usr/bin/env python
# encoding: utf-8

from fabric.api import env
from fabric.api import run
from fabric.api import roles


env.roledefs = {
    'remote': ['root@45.77.18.107']
}


@roles('remote')
def init():
    '''环境初始化'''
    pass


@roles('remote')
def deploy():
    '''部署'''
    pass


@roles('remote')
def close():
    '''关闭'''
    pass


@roles('remote')
def restart():
    '''重启'''
    # reload nginx
    run('nginx -s /opt/dinglive/nginx.conf')
    run('systemctl restart mysqld')
    run('supervisord -c /opt/dinglive/supervisord.conf')
