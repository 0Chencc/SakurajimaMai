from config import WEBHOOK
from sign import getDingSign
import urllib3
import json
import requests


def sendmsg(title,msg):
    headers = {
        'Content-Type': 'application/json',
    }
    params = getDingSign()
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": msg
        },
        "at": {
            "atMobiles": [
                ""
            ],
            "atUserIds": [
                ""
            ],
            "isAtAll": False
        }
    }
    data = json.dumps(message)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.post(url=WEBHOOK, headers=headers, params=params, data=data, verify=False)
    if response.json()['errcode'] == 0:
        print('已完成钉钉消息推送')
    else:
        print('发送失败：错误代码'+response.json()['errcode']+'错误信息：'+response.json()['msg'])