#!/usr/bin/env python
# encoding: utf-8

'''
定是脚本，用于爬取网站信息
默认情况，为线上爬取规则
可选参数：
@prod 正式环境
@test 测试环境
'''

from spider.tv import crawlers
from conf import SPIDER_PERIOD
from conf import SPIDER_COUNT
from conf import TEST
from conf import PROD
from clear import Clear
from common.utils import green
from common.utils import current

from apscheduler.schedulers.background import BlockingScheduler
import sys


# enviroment
ENV = set([TEST, PROD])


class Crond(object):
    '''定时任务'''
    scheduler = BlockingScheduler()

    def __init__(self, env=TEST):
        self.env = env

    def add_job(self, seconds, task, args):
        Crond.scheduler.add_job(task, 'interval', seconds=seconds, args=args)

    def start(self):
        Crond.scheduler.start()


def task(env):
    print green('-> 开始抓取 %s' % current())
    count = SPIDER_COUNT.get(env)
    for key, crawler in crawlers.items():
        try:
            crawler.run(count)
        except Exception as e:
            print "crawl error", key, e
    Clear().run(env)
    print green('-> 完成抓取 %s' % current())


def run(env):
    crond = Crond(env)
    crond.add_job(2, task, (env,))
    crond.start()


if __name__ == '__main__':
    env = sys.argv[1] if len(sys.argv) > 1 else TEST
    print green('当前执行环境: %s' % env)
    run(env)
