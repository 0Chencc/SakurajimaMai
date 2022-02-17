import requests
from src.api import send
import time
from src.config import WB_UIDS, shanghai
import datetime
from dateutil import parser
api = {
    'userinfo': 'https://m.weibo.cn/api/container/getIndex',
}
start_time = datetime.datetime.now().astimezone(shanghai)
weiboIds = []


def weibo_monitor(uid):
    user_info_api = api['userinfo']
    params = {
        'type': 'uid',
        'value': uid
    }
    userinfo = requests.get(url=user_info_api, params=params).json()
    username = userinfo['data']['userInfo']['screen_name']
    for i in userinfo['data']['tabsInfo']['tabs']:
        if i['tab_type'] == 'weibo':
            params['containerid'] = i['containerid']
    weiboinfo = requests.get(url=user_info_api, params=params).json()
    for i in weiboinfo['data']['cards']:
        if i['card_type'] == 9:
            if (i['mblog']['id'] in weiboIds) is False:
                # createtime = time.strptime(i['mblog']['created_at'], '%a %b %d %X %z %Y')
                create_time = parser.parse(i['mblog']['created_at'])
                if is_new_weibo(create_time):
                    title = f'<{username}>发布了一条微博'
                    create_time = create_time.__format__("%Y-%m-%d %X")
                    text = i['mblog']['text']
                    msg = f"**{title}**\n" \
                          f"\n" \
                          f"> 于{create_time}\n" \
                          f"\n" \
                          f"{text}\n"
                    if 'pics' in i['mblog']:
                        for j in i['mblog']['pics']:
                            purl = j['large']['url']
                            mkpic = f"![{purl}]({purl})\n"
                            msg = msg + mkpic
                    send.sendmsg(title=title, msg=msg)
                weiboIds.append(i['mblog']['id'])


def is_new_weibo(ctime):
    if ctime > start_time:
        return True
    else:
        return False


def start_monitor():
    if len(WB_UIDS) == 0:
        print('没有关注的博主，微博监控退出')
        return
    print("微博博主动态推送已启动")
    while True:
        for i in WB_UIDS:
            try:
                weibo_monitor(i)
            except:
                continue
        time.sleep(5)