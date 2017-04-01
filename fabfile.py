#!/usr/bin/env python
# encoding: utf-8

from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import roles
from fabric.colors import green
from fabric.colors import yellow

import time


env.roledefs = {
    'remote': ['root@45.77.18.107']
}


@roles('remote')
def deploy(branch):
    '''部署'''
    print(green('开始部署'))
    # 创建运行空间, 更新代码
    print(yellow('1.创建空间'))
    run('mkdir -p /opt/logs/dinglive')
    print(yellow('2.同步代码'))
    with cd('/opt'):
        run('git clone https://github.com/simyy/dinglive.git')
        run('git checkout %s' % branch)
    # 启动nginx
    print(yellow('3.启动nginx'))
    run('nginx -s stop')
    time.sleep(2)
    run('nginx -c /opt/dinglive/nginx.conf')
    # 启动mysql
    print(yellow('4.启动mysql'))
    run('')
    # 启动supervisor
    print(yellow('5.启动supervisord'))
    run('supervisord -c /opt/dinglive/supervisord.conf')
    print(green('完成部署'))


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
