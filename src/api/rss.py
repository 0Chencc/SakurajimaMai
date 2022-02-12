import sys
import feedparser
import time
import datetime
from dateutil import parser
import send
from config import shanghai

start_time = datetime.datetime.now().astimezone(shanghai)
new_post_list = []


def is_new(date):
    # 通过datetime.timetuple()转化为元组，再使用time.mktime转成时间戳来进行判断。
    # push_time = time.mktime(parser.parse(date).timetuple())
    # return push_time >= start_time
    # 通过datetime直接判断
    return parser.parse(date) >= start_time
    # a = parser.parse(date)
    # if a.date() > start_time.date():
    #     return True
    # elif a.date() == start_time.date():
    #     return a.hour >= start_time.hour and a.minute >= start_time.minute
    # else:
    #     return False


def monitor(url):
    rss = feedparser.parse(url)
    for i in rss['entries']:
        text = f"{i['title']} {i['link']}"
        date = f"{i['published']}"
        if is_new(date) and text not in new_post_list:
            send.sendmsg('订阅的rss更新了', text)
            new_post_list.append(text)


def monitor_start():
    try:
        rss_path = f'{sys.path[0]}/rss.txt'
        rss_resource = open(rss_path, 'r')
    except:
        print("没有rss.txt文件，rss订阅已退出")
        return
    rss_list = rss_resource.readlines()
    print(rss_list)
    if rss_list is None or len(rss_list) == 0:
        print("没有订阅的rss链接，rss订阅已退出")
        return
    while True:
        for i in rss_list:
            monitor(i)
        time.sleep(60*30)