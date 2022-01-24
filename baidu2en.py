import sys
import baidu2zh

if __name__ == '__main__':
    content = sys.argv[1]  # 外部调用.py时, 第一个输入变量
    baidu2zh.display(baidu2zh.trans(content, 'en'))
