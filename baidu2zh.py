import requests
import random
import sys
import io
import json
from hashlib import md5


def make_md5(s):
    return md5(s.encode('utf-8')).hexdigest()


def read_config():
    # 打开当前文件路径下，同级的 json 配置文件
    with open(sys.path[0] + '/config.json') as j:
        return json.load(j)['baiduAPI']  # dic


def trans(query):
    """自动判断语种，并译为汉语"""

    cfg = read_config()
    salt = random.randint(32768, 65536)
    sign = make_md5(cfg['id'] + query + str(salt) + cfg['key'])  # 生成签名

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': cfg['id'], 'q': query, 'from': 'auto', 'to': 'zh', 'salt': salt, 'sign': sign, 'action': 1}  # 源语言自动确定

    # Send request
    r = requests.post(cfg['url'], params=payload, headers=headers)
    return r.json()


def display(result):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 没有这句，goldendict中文输出乱码
    if 'error_code' in result:
        print('Error Code from API: ' + result['error_code'])  # 报错信息
    else:
        ans = result['trans_result']
        print('原文(' + result['from'] + ')')
        print("<p style='color:red'>&nbsp&nbsp&nbsp&nbsp" + ans[0]['src'] + "</p><hr/>")  # 行首两空格, 结尾分隔线
        print('译文(' + result['to'] + ')')
        print("<p style='color:blue'>&nbsp&nbsp&nbsp&nbsp" + ans[0]['dst'] + "</p>")


if __name__ == '__main__':
    # content = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph, he is a chinese.'
    content = sys.argv[1]  # 外部调用.py时, 第一个输入变量
    display(trans(content))
    
