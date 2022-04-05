import time
import threading
import os
from api import acfun, bilibili, rss, weibo, mealtime, lol

threads = [threading.Thread(target=weibo.start_monitor), threading.Thread(target=bilibili.start_monitor),
           threading.Thread(target=mealtime.remind_start), threading.Thread(target=acfun.start_monitor),
           threading.Thread(target=rss.monitor_start), threading.Thread(target=lol.monitor_start)]


# 由于需要挂在github，所以需要设定好程序每次运行的周期，如果程序是在服务器运行，可以忽略该项
def cycle():
    try:
        count = 0
        times = 60 * 4
        while True:
            if count <= times:
                count += 1
            else:
                break
            time.sleep(60)
    finally:
        # send.sendmsg('结束提醒', '机器人已循环一个周期')
        os._exit(0)


threads.append(threading.Thread(target=cycle))

if __name__ == '__main__':
    for i in threads:
        i.start()
