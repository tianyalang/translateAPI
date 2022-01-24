import baidu2zh as x

s1 = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph, he is a chinese.'
s2 = '我是中国人'
s3 = 'हमारे देश के छोटे-छोटे बच्चों ने, बेटे-बेटियों ने हर युग में इतिहास लिखा है'

print(x.read_config())
print(x.trans(s1))
print(x.trans(s3, 'en'))