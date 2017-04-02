#!/usr/bin/env python
# encoding: utf-8

from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import roles
from fabric.colors import green
from fabric.colors import yellow


env.roledefs = {
    'remote': ['root@45.77.18.107']
}


@roles('remote')
def deploy(branch):
    '''部署'''
    print(green('开始部署'))
    # 创建运行空间, 更新代码
    print(yellow('-> 创建空间'))
    run('mkdir -p /opt/logs/dinglive')
    print(yellow('-> 同步代码'))
    with cd('/opt'):
        run('git clone https://github.com/simyy/dinglive.git')
    # 启动nginx
    print(yellow('-> 启动nginx'))
    run('mv /opt/dinglive/nginx.conf /etc/nginx/nginx.conf')
    run('nginx -s start')
    # 启动mysql
    print(yellow('-> 启动mysql'))
    run('service mysql start')
    print(yellow('-> 创建数据库表'))
    run('mysql -u root -p123 < /opt/dinglive/database.sql')
    # 启动supervisor
    print(yellow('-> 启动supervisord'))
    run('supervisord -c /opt/dinglive/supervisord.conf')
    print(green('完成部署'))


@roles('remote')
def reset_db():
    '''更新数据表'''
    print(green('开始更新mysql'))
    run('service mysql start')
    run('mysql -u root -p123 < /opt/dinglive/database.sql')
    print(green('完成更新mysql'))


@roles('remote')
def restart(cmd='all'):
    '''重启'''
    print(green('开始重启'))
    if cmd == 'all' or cmd == 'mysql':
        print(yellow('-> 重启mysql'))
        run('service mysql restart')
    if cmd == 'all' or cmd == 'web':
        print(yellow('-> 重启web'))
        run('supervisord -c /opt/dinglive/supervisord.conf')
        run('supervisorctl restart dinglive')
    if cmd == 'all' or cmd == 'nginx':
        print(yellow('-> 重启nginx'))
        run('mv /opt/dinglive/nginx.conf /etc/nginx/nginx.conf')
        run('nginx -s reload')
    print(green('完成重启'))


@roles('remote')
def update():
    '''更新'''
    # reload nginx
    print(green('开始更新'))
    print(yellow('-> 同步代码'))
    with cd('/opt/dinglive'):
        run('git pull')
    print(green('完成更新'))
