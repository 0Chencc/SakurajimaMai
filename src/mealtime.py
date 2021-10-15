import time
import send
from config import breakfast, lunch, dinner

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
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min
        for key, value in meals.items():
            if value is not None and value != '':
                if value.tm_hour == hour and value.tm_min == minute:
                    meal_remind(key)
        time.sleep(60)