# lpl赛事订阅：这里是中国人的赛事订阅，要看lck的到韩国人的项目看 -- 来自华为13promax远峰蓝
# 如果其他赛区有需要我会增加的，需要请提交issue。这个功能发布于凌晨4：40。所以不写那么多赛区了。
import json

import requests
api = {
    'set_cookies':'https://m.wanplus.cn/',
    'e_sport_data':'https://m.wanplus.cn/ajax/schedule/list',
}

response = requests.get(url=api['set_cookies'])
cookies = requests.utils.dict_from_cookiejar(response.cookies)

response = requests.get(url=api['e_sport_data'], cookies=cookies)
print(response.text)