import os
from datetime import *
import pytz
shanghai = pytz.timezone('Asia/Shanghai')
SECRET = os.getenv('SECRET')
WEBHOOK = os.getenv('WEBHOOK')

WB_UIDS = os.getenv('WB_UIDS').split(',')if os.getenv('WB_UIDS') is not None else ''
bUPIds = os.getenv('BUPIDS').split(',')if os.getenv('BUPIDS') is not None else ''
bAIds = os.getenv('BAIDS').split(',')if os.getenv('BAIDS') is not None else ''
aAIds = os.getenv('AUPIDS').split(',')if os.getenv('AUPIDS') is not None else ''

breakfast = os.getenv('BREAKFAST')
if breakfast is not None and breakfast != '':
    breakfast = (
        datetime.strptime(breakfast, '%H') if len(breakfast) == 2 else datetime.strptime(
            breakfast, '%H%M'))

lunch = os.getenv('LUNCH')
if lunch is not None and lunch != '':
    lunch = (
        datetime.strptime(lunch, '%H') if len(lunch) == 2 else datetime.strptime(
            lunch, '%H%M'))

dinner = os.getenv('DINNER')
if dinner is not None and dinner != '':
    dinner = (
        datetime.strptime(dinner, '%H') if len(dinner) == 2 else datetime.strptime(
            dinner, '%H%M'))