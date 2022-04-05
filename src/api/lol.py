# lpl赛事订阅：这里是中国人的赛事订阅，要看lck的到韩国人的项目看 -- 来自华为13promax远峰蓝
# 如果其他赛区有需要我会增加的，需要请提交issue。这个功能发布于凌晨2:03。所以不写那么多赛区了。
from datetime import *
import json
from api import send
from dateutil import parser
import time
from config import shanghai
import requests

# start_time = datetime.datetime.now().astimezone(shanghai)

api = {
    'set_cookies': 'https://wanplus.cn/',
    'e_sport_data': 'https://wanplus.cn/ajax/schedule/list',
}


def get_cookies():
    response = requests.get(url=api['set_cookies'], verify=False)
    return requests.utils.dict_from_cookiejar(response.cookies)


def near_time(now_time, start_time):
    return 0 <= (start_time - now_time) <= 1800


def e_sport_info_monitor():
    cookies = get_cookies()
    headers = {
        'Host': 'wanplus.cn',
        'Content-Length': '51',
        'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'X-Csrf-Token': '1068275517',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Origin': 'https://wanplus.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://wanplus.cn/lol/schedule',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
    }
    now_time = int(time.time())
    data = {
        "_gtk": 1068275517,
        "game": 2,
        "time": now_time,
        "eids": [1078]
    }
    response = requests.post(url=api['e_sport_data'], cookies=cookies, data=data, headers=headers, verify=False)
    week_games_info = response.json()
    if week_games_info['msg'] == 'success':
        schedule_list = week_games_info['data']['scheduleList']
        for i in schedule_list:
            day_games_info = schedule_list[i]
            game_list = day_games_info['list']
            if game_list:
                for j in game_list:
                    game_start_time = j['relation']+' '+j['starttime']
                    game_start_time = int(datetime.timestamp(datetime.strptime(game_start_time, '%Y%m%d %H:%M')
                                                             .astimezone(shanghai)))
                    if near_time(now_time=now_time, start_time=game_start_time):
                        msg = f"![banner]({j['poster']})\n\n" \
                              f"{j['ename']}{j['groupname']}" \
                              f"——{j['oneseedname']} 对战 {j['twoseedname']}\n\n" \
                              f"即将开始\n\n" \
                              f"请留意比赛开始时间：{j['starttime']}\n\n" \
                              f"赛事直播地址：\n\n" \
                              f"虎牙：https://www.huya.com/lpl\n\n" \
                              f"B站：https://live.bilibili.com/6"
                        send.sendmsg(title=f"{j['oneseedname']} 对战 {j['twoseedname']}即将开始", msg=msg)
    else:
        print('获取订阅失败，可能是api问题')


def monitor_start():
    while True:
        e_sport_info_monitor()
        time.sleep(30*60)


monitor_start()
