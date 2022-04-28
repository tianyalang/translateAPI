import baidu2zh as x
# import baidu2zhfeild as y




# s1 = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph, he is a chinese.'
# s2 = '电机建模是电机设计和性能分析的基础。开关磁阻电机由于通常工作于磁饱和状态，加之绕组电流非正弦，使得建立统一的电机非线性数学模型十分困难。本文以子域法为基础，结合等效电流法和保角变换法，实现了开关磁阻电机的高精度非线性快速解析建模，为开关磁阻电机的设计分析和先进控制算法应用提供理论基础。'
# s3 = 'हमारे देश के छोटे-छोटे बच्चों ने, बेटे-बेटियों ने हर युग में इतिहास लिखा है'
# s4 = 'とうほく'

# print(x.read_config())
# print(x.sendRequest('language', s4))
# print(x.trans(s1, 'en', 'zh'))
# print(x.sendRequest('fieldtranslate', s2, 'zh', 'en', 'electronics'))
print(x.sendRequest('picture'))
# print(x.trans(s4, 'jp', 'en'))
