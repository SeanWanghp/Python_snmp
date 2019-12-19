# !-*-coding:utf-8-*-
# data@:2018-09-20
# C:\Python27\Doc python
__author__ = 'Sean Wang'
import requests
import bs4
from requests.auth import HTTPBasicAuth


def login_wiki():
    """login wiki page and capture detail content
    bs4 basic function:  https://www.cnblogs.com/lizm166/p/8143231.html"""
    wiki_page = ["http://wiki.calix.local/display/~sewang/VB+script+for+simulation+ONT+with+services",
                 "http://wiki.calix.local/display/DVT/TestCenter+Chassis+info+in+CDC+lab",
                 "http://wiki.calix.local/display/DVT/IXIA+Chasiss+information+in+Nanjing+Lab",
                 ]
    page = wiki_page[2]

    def SaveFile(content, filename):
        with open(filename, 'a') as fs:
            try:
                fs.write(str(content) + '\r')
            except Exception as e:
                print(e)
        fs.close()

    # login web page
    response = requests.get(page, auth=HTTPBasicAuth('sewang', 'p@ssword88'))
    # 方法二 r = requests.get('http://120.27.34.24:9001', auth=('user', '123'))
    if response.status_code is 200:
        # 使用BeautifulSoup解析代码,并锁定页码指定标签内容
        content = bs4.BeautifulSoup(response.content.decode("utf-8"), "lxml")
        if 'ONT' in page:
            element = content.find_all(id='main-content')
            print(element)
            div = content.find(name='div', id='main-content')
            ps = div.find_all(name='p', recursive=False, limit=10)  # limit可以限制字数少于多少的不显示
        elif 'TestCenter' or 'IXIA' in page:
            element = content.find_all(id='main-content')
            # div = content.find_all('div', class_='table-wrap')

            if 'TestCenter' in page:
                for div in content.find_all('table'):
                    print('table: {}'.format(div))
                    ps = div.find_all('td', )
                    print('ps: {}'.format(ps))
            elif 'IXIA' in page:
                # div = content.find_all('div', class_='table-wrap')
                for div in content.find_all('div', class_='table-wrap'):
                    try:
                        print('th: {}'.format(div))
                        ps = div.find_all('p', )
                        print('p: {}'.format(ps))
                    except Exception as e:
                        pass
        for p in ps:
            ptext = p.get_text()
            print("pText:", ptext)
            SaveFile(ptext.strip().encode('utf-8'), 'wiki.txt')
    else:
        print('loging failed at code {}'.format(response.status_code))


def login_jira():
    """login jira own new bug page and capture ticket content"""
    wiki_page = ["http://jira.calix.local/issues/?filter=12234",
                 ]
    page = wiki_page[0]

    # login web page
    response = requests.get(page, auth=HTTPBasicAuth('sewang', 'p@ssword88'))
    # 方法二 r = requests.get('http://120.27.34.24:9001', auth=('user', '123'))
    if response.status_code is 200:
        # 使用BeautifulSoup解析代码,并锁定页码指定标签内容
        content = bs4.BeautifulSoup(response.content.decode("utf-8"), "lxml")
        element = content.find_all(class_='navigator-container')
        # print(element)
        for div in content.find_all('tbody'):
            # print('div: {}'.format(div))
            try:
                # print('table: {}'.format(div))
                ps = div.find_all('td', )
                # print('td: {}'.format(ps))
            except Exception as e:
                pass
        for p in ps:
            ptext = p.get_text()
            print("thText:", ptext)
    else:
        print('loging failed at code {}'.format(response.status_code))


if __name__ == '__main__':
    # login_wiki()
    login_jira()
