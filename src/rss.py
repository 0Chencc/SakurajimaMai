import json

import feedparser
import pytz
import time
import datetime
from dateutil import parser
import send
shanghai = pytz.timezone('Asia/Shanghai')
start_time = datetime.datetime.now().astimezone(shanghai)
rss_resource = open('../rss.txt', 'r')


def is_new(date):
    a = parser.parse(date).astimezone(shanghai)
    if a.date() > start_time.date():
        return True
    elif a.date() == start_time.date():
        return a.hour >= start_time.hour and a.minute >= start_time.minute
    else:
        return False


def monitor(url):
    rss = feedparser.parse(url)
    for i in rss['entries']:
        text = f"{i['title']} {i['link']}"
        date = f"{i['published']}"
        if is_new(date):
            send.sendmsg('订阅的rss更新了', text)


def monitor_start():
    rss_list = rss_resource.readlines()
    print(rss_list)
    if rss_list is None or len(rss_list) == 0:
        return
    while True:
        for i in rss_list:
            monitor(i)
        time.sleep(60*30)


monitor_start()