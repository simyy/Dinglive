#!/usr/bin/env python
# encoding: utf-8

from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import roles


env.roledefs = {
    'remote': ['root@45.77.18.107']
}


@roles('remote')
def deploy(branch):
    '''部署'''
    # 创建运行空间, 更新代码
    run('mkdir -p /opt/logs/dinglive')
    with cd('/opt'):
        run('git clone https://github.com/simyy/dinglive.git')
        run('git checkout %s' % branch)
    # 安装nginx、mysql
    # 安装python依赖环境


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
