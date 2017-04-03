#!/usr/bin/env python
# encoding: utf-8

from termcolor import colored

import datetime


def green(a):
    return colored(a, 'green')


def yellow(a):
    return colored(a, 'yellow')


def blue(a):
    return colored(a, 'blue')


def red(a):
    return colored(a, 'red')


def save_pic(pic_name, url):
    return ''


def current():
    return datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
