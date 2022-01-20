import requests
import send
from config import bUPIds, bAIds,shanghai
import time
import datetime
api = {
    'userinfo': 'http://api.bilibili.com/x/space/acc/info',
    'videos_info': 'https://api.bilibili.com/x/space/arc/search',
    'video_play': 'https://www.bilibili.com/video/',
    'anime_info': 'https://api.bilibili.com/pgc/view/web/season',
}
starttime = time.mktime(time.localtime())

up_video_list = []
anime_list = []


def bilibili_monitor(upid):
    params = {
        'mid': upid
    }
    response = requests.get(api['videos_info'], params=params)
    videos = response.json()['data']['list']['vlist']
    for i in videos:
        bv = i['bvid']
        if i['created'] >= starttime and (bv in up_video_list) is False:
            ding_talk(i, upid)
            up_video_list.append(bv)
        else:
            break


def anime_monitor(apid):
    params = {
        'season_id': apid
    }
    response = requests.get(api['anime_info'], params=params)
    eps = response.json()['result']['episodes']
    eps.reverse()
    for i in eps:
        if i['pub_time'] >= starttime and (apid in anime_list) is False:
            print((i in anime_list) is False)
            anime_ding_talk(i, apid)
            anime_list.append(apid)
        else:
            break


def anime_ding_talk(ep, apid):
    params = {
        'season_id': apid
    }
    play_link = ep['short_link']
    title = ep['long_title']
    name = requests.get(api['anime_info'], params=params).json()['result']['title']
    pic = f"![pic]({ep['cover']})"
    msg = f"**《{name}》更新啦**\n" \
          f"\n" \
          f">新的一集《{title}》\n" \
          f"\n" \
          f"{pic}\n" \
          f"\n" \
          f"播放地址：{play_link}"
    send.sendmsg(title=f'{name}更新啦', msg=msg)


def ding_talk(video, upid):
    params = {
        'mid': upid
    }
    bv = video['bvid']
    video_title = video['title']
    pic = f"![pic]({video['pic']})"
    name = requests.get(api['userinfo'], params=params).json()['data']['name']
    play = api['video_play'] + bv
    title = f"{name} 发布了新的视频"
    msg = f"**<{name}> 发布了新的视频**\n" \
          f"\n" \
          f"**《{video_title}》**\n" \
          f"\n" \
          f"{pic}\n" \
          f"\n" \
          f"播放地址：{play}"
    send.sendmsg(title=title, msg=msg)


def start_monitor():
    count = 0
    if len(bUPIds) == 0:
        count += 1
    if len(bAIds) == 0:
        count += 1
    if count == 2:
        print('没有追番且没有关注的up主，b站监控已退出')
        return
    while True:
        for upid in bUPIds:
            try:
                bilibili_monitor(upid)
            except:
                continue
        for aid in bAIds:
            try:
                anime_monitor(aid)
            except:
                continue
        time.sleep(600)