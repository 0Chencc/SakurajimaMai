import requests
import requests_html
import random
import time
import send
from config import aAIds

starttime = time.gmtime()

api = {
    'user_info': 'https://www.acfun.cn/u/',
    'set_cookie': 'https://www.acfun.cn/'
}
version = random.randint(85, 95)
headers = {
    'Host': 'www.acfun.cn',
    'Sec-Ch-Ua': f'\\"Google Chrome\\";v=\\"{version}\\", \\" Not;A Brand\\";v=\\"99\\", \\"Chromium\\";v=\\"{version}\\"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '\\"macOS\\"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.4577.63 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
response = requests.get(api['set_cookie'], headers=headers)
cookies = requests.utils.dict_from_cookiejar(response.cookies)
up_video_list = []


def acfun_up_monitor(uid):
    session = requests_html.HTMLSession()
    user_info = api['user_info']+uid
    r = session.get(url=user_info, headers=headers, cookies=cookies).html
    play = r.xpath("//div[@id='ac-space-video-list']/a/@href")
    for i in range(len(play)):
        pushtime = r.xpath(f"//div[@id='ac-space-video-list']/a[@href='{play[i]}']/figure/figcaption/p/text()")[2]
        url = r.xpath("//div[@id='ac-space-video-list']/a/@href")[i]
        if is_new_video(pushtime) and (url in up_video_list) is False:
            name = r.xpath("//div[@class='top']/span[@class='name']/@data-username")[0]
            pic = r.xpath(
                f"//div[@id='ac-space-video-list']/a[@href='{play[i]}']/figure/img/@src")[0]
            title = r.xpath(f"//div[@id='ac-space-video-list']/a[@href='{play[i]}']/figure/figcaption/p/text()")[
                    0]
            video_info = {
                'url': f"https://www.acfun.cn{url}",
                'title': title,
                'name': name,
                'pushtime': pushtime,
                'pic': pic
            }
            up_ding_talk(video_info)
            up_video_list.append(url)
        else:
            break


def is_new_video(pushtime):
    pushtime = time.strptime(pushtime, "%Y/%m/%d")
    if pushtime > starttime:
        return True
    else:
        return False


def up_ding_talk(video_info):
    title = f"{video_info['name']} 发布了新视频"
    msg = f"**<{video_info['name']}>发布了新的视频**\n" \
          f"\n" \
          f"**《{video_info['title']}》**\n" \
          f"\n" \
          f"![pic]({video_info['pic']})\n" \
          f"\n" \
          f"视频地址：{video_info['url']}"
    send.sendmsg(title=title, msg=msg)


def start_monitor():
    count = 0
    if len(aAIds) == 0:
        count += 1
    if count == 1:
        print('没有关注的a站up主，程序退出')
        return
    while True:
        for i in aAIds:
            acfun_up_monitor(i)
        time.sleep(24*3600)