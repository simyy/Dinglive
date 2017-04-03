#!/usr/bin/env python
# encoding: utf-8

# ENV
TEST = 'test'
PROD = 'prod'

# mysql
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_USER = 'root'
DB_PWD = '123'
DB_NAME = 'dinglive'

# crond
SPIDER_PERIOD = {'prod': 30 * 60, 'test': 10}
SPIDER_COUNT = {'prod': 500, 'test': 50}
