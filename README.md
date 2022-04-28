# translateAPI

利用翻译 API 给 GoldenDict 添加字典程序

程序`baidu2zh.py`按照外部参数的不同，可实现通用翻译、专业翻译两种功能，调用格式为：

- `python baidu2zh.py text` 先对文本`text`进行语种识别，源语言为中文，翻译为英文，其他源语言，均翻译为中文。
- `python baidu2zh.py text electronics` 对电子电气专业文本`text`进行中译英
