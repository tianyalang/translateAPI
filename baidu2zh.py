import requests
import random
import sys
import os
import io
import json
from hashlib import md5
from PIL import ImageGrab


def get_file_md5(file_name):
    with open(file_name, 'rb') as f:
        data = f.read()
        return md5(data).hexdigest()


def getSign(cfg, strings, salt, domain=''):
    """生成签名"""
    s = cfg['id'] + strings + str(salt) + domain + cfg['key']
    return md5(s.encode('utf-8')).hexdigest()


def read_config():
    """打开当前文件路径下，同级的 json 配置文件"""
    with open(sys.path[0] + '/config.json') as j:
        return json.load(j)['baiduAPI']  # dic


def sendRequest(type, text='', src='', dst='', domain=''):
    """语种识别、通用翻译、专业翻译三种功能的统一请求命令"""
    cfg = read_config()
    salt = random.randint(32768, 65536)

    if type == 'language':  # 支持识别中、英、日、韩、泰、越南、俄
        url = 'https://fanyi-api.baidu.com/api/trans/vip/language'
        sign = getSign(cfg, text, salt)
        data = {'appid': cfg['id'], 'q': text, 'salt': salt, 'sign': sign}

    elif type == 'translate':
        url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        sign = getSign(cfg, text, salt)
        data = {
            'appid': cfg['id'],
            'q': text,
            'from': src,
            'to': dst,
            'salt': salt,
            'sign': sign,
            'action': 1
        }

    elif type == 'fieldtranslate':
        url = 'https://fanyi-api.baidu.com/api/trans/vip/fieldtranslate'
        sign = getSign(cfg, text, salt, domain)
        data = {
            'appid': cfg['id'],
            'q': text,
            'from': src,
            'to': dst,
            'salt': salt,
            'sign': sign,
            'domain': domain
        }

    elif type == 'picture':
        img = ImageGrab.grabclipboard()
        img_path = './temp/ocr.png'
        img.save(img_path)
        url = 'https://fanyi-api.baidu.com/api/trans/sdk/picture'
        sign = getSign(cfg, get_file_md5(img_path), salt, 'APICUIDmac')
        data = {
            'from': 'en',
            'to': 'zh',
            'appid': cfg['id'],
            'salt': salt,
            'sign': sign,
            'cuid': 'APICUID',
            'mac': 'mac',
            'version': 3
        }
        image = {'image': (os.path.basename(img_path), open(img_path,'rb'), "multipart/form-data")}
        response = requests.post(url, params=data, files=image)
        return response.json()['data']['content']

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, params=data, headers=headers)
    return r.json()
    #TODO 不知道如何在 goldenDict 中激活该程序
    

def display(result):
    """GoldenDic 中以 html 语言显示"""
    # 没有这句，goldendict中文输出乱码
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if 'error_code' in result:
        print('Error Code from API: ' + result['error_code'])  # 报错信息
    else:
        ans = result['trans_result']
        print('原文 (' + result['from'] + ')')
        print("<p style='color:red'>&nbsp&nbsp&nbsp&nbsp" + ans[0]['src'] +
              "</p><hr/>")  # 行首两空格, 结尾分隔线
        print('译文 (' + result['to'] + ')')
        print("<p style='color:blue'>&nbsp&nbsp&nbsp&nbsp" + ans[0]['dst'] +
              "</p>")


if __name__ == '__main__':
    args = sys.argv  # 外部调用.py时, 输入参数列表，第0个参数是函数文件名本身

    if len(args) == 2:  # 外部输入1个参数时，用通用翻译
        test = sendRequest('language', args[1])
        src = test['data']['src'] if test['error_msg'] == 'success' else 'auto'
        dst = 'en' if src == 'zh' else 'zh'
        display(sendRequest('translate', args[1], src, dst))

    elif len(args) == 3 and args[-1] == 'electronics':  # 2个参数，专业翻译
        display(
            sendRequest('fieldtranslate', args[1], 'zh', 'en', 'electronics'))
