# -*- coding: utf-8 -*-

# This code shows an example of ocr translation from Simplified-Chinese to English.
# This code runs on Python 2.7.x and Python 3.x.
# ```
#   python ocr_translate.py <image>
# ```
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/26` for complete api document

import requests
import random
import json
import os
import sys
from hashlib import md5
from PIL import ImageGrab

img = ImageGrab.grabclipboard()
img_path = './temp/ocr.png'
img.save(img_path)

# if len(sys.argv) != 2:
#     print("usage: python {} <image>".format(sys.argv[0]))
#     exit(-1)

# file_name = sys.argv[1]
file_name = img_path
url = 'http://api.fanyi.baidu.com/api/trans/sdk/picture'

from_lang = 'en'
to_lang = 'zh'

# Set your own appid/appkey.
appid = '20211103000990246'
appkey = 'ue4nR6w1IZKI4JmkOeBR'

# cuid & mac
cuid = 'APICUID'
mac = 'mac'


# Generate salt and sign
def get_md5(string, encoding='utf-8'):
    return md5(string.encode(encoding)).hexdigest()


def get_file_md5(file_name):
    with open(file_name, 'rb') as f:
        data = f.read()
        return md5(data).hexdigest()


salt = random.randint(32768, 65536)
sign = get_md5(appid + get_file_md5(file_name) + str(salt) + cuid + mac +
               appkey)

# Build request
payload = {
    'from': from_lang,
    'to': to_lang,
    'appid': appid,
    'salt': salt,
    'sign': sign,
    'cuid': cuid,
    'mac': mac
}
image = {
    'image': (os.path.basename(file_name), open(file_name,
                                                'rb'), "multipart/form-data")
}

# Send request
response = requests.post(url, params=payload, files=image)
result = response.json()['data']['content']

# Show response
# print(json.dumps(result, indent=4, ensure_ascii=False))
for part in result:
    print(part['src'])
    print(part['dst'])