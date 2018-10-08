#!-*-coding:utf-8-*-
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-09-20
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word


import requests, bs4
from requests.auth import HTTPBasicAuth

'''
login wiki page and capture detail content
'''
wiki_page = "http://wiki.calix.local/display/~sewang/VB+script+for+simulation+ONT+with+services"


def SaveFile(content, filename):
    with open(filename, 'a') as fs:
        fs.write(content+"\n")
        fs.close()

#方法一
response = requests.get(wiki_page, auth=HTTPBasicAuth('sewang', 'pppppppppp'))
#方法二<br>r = requests.get('http://120.27.34.24:9001', auth=('user', '123'))
#查看响应状态码
status_code = response.status_code

#使用BeautifulSoup解析代码,并锁定页码指定标签内容
content = bs4.BeautifulSoup(response.content.decode("utf-8"), "lxml")
element = content.find_all(id='main-content')

print(status_code)
print(element)

div = content.find(name='div', id='main-content')
ps = div.find_all(name='p', recursive=False, limit = 10000) #only direct children, limit 可以限制字数少于多少的不显示
for p in ps:
    pText = p.get_text()
    print "pText:", pText
    SaveFile(pText.encode('utf-8').strip(), 'wiki.txt')