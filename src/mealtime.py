import datetime
import pytz
import send
import time
from config import breakfast, lunch, dinner
shanghai = pytz.timezone('Asia/Shanghai')
meals = {
    'breakfast': breakfast,
    'lunch': lunch,
    'dinner': dinner,
}


def meal_remind(key):
    meal = {
        'breakfast': '早饭',
        'lunch': '午饭',
        'dinner': '晚饭',
    }
    info = f'麻衣学姐来提醒你记得按时吃{meal[key]}哦～'
    send.sendmsg(title=info, msg=info)


def remind_start():
    count = 0
    for i in meals.values():
        if i is None or i == '':
            count += 1
    if count == 3:
        print('三餐都没有设定时间，提醒吃饭退出')
        return
    while True:
        now = datetime.datetime.now().astimezone(shanghai)
        hour = now.hour
        minute = now.minute
        for key, value in meals.items():
            if value is not None and value != '':
                if value.hour == hour and value.minute == minute:
                    meal_remind(key)
        time.sleep(60)