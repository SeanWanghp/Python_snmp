# !-*-coding:utf-8-*-
# data@:2018-09-20
# C:\Python37
__author__ = 'Sean Wang'
import requests
import bs4
import os
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


def download_mp3():
    # 下载MP3文件到本地
    def DownloadFile(mp3_url, save_url, file_name):
        try:
            if mp3_url is None or save_url is None or file_name is None:
                print('参数错误')
                return None
            # 文件夹不存在，则创建文件夹
            folder = os.path.exists(save_url)
            if not folder:
                os.makedirs(save_url)
            # 读取MP3资源
            res = requests.get(mp3_url, stream=True)
            # 获取文件地址
            file_path = os.path.join(save_url, file_name)
            print('开始写入文件：', file_path)
            # 打开本地文件夹路径file_path，以二进制流方式写入，保存到本地
            with open(file_path, 'wb') as fd:
                for chunk in res.iter_content():
                    fd.write(chunk)
            print(file_name + ' 成功下载！')
        except Exception as e:
            print("程序错误")

    if __name__ == "__main__":
        """MP3源地址url, find out the mp3 soure method as following:
        play we-> 'Network' + F5(refresh) -> search 'mp3' or check out the file as media or file with bigsize,
        check out the file address and verify it with web
        """

        url = ['http://96.ierge.cn/13/197/395449.mp3?v=0524',
               'http://96.ierge.cn/12/180/361661.mp3?v=0524',
               'http://win.web.ra03.sycdn.kuwo.cn/756440f2b6a14f22c0e94b90e33de049/5dfc23e3/resource/a1/48/21/11/1639143032.aac',
               'http://win.web.ra03.sycdn.kuwo.cn/378f1a32146919298e89d82324f1e3c4/5dfc2696/resource/a2/48/49/75/1226258725.aac'
               'http://58.216.6.154/amobile.music.tc.qq.com/C400000z1MeK42lTZT.m4a?guid=8232151651&vkey=3BC26B8B24A1F860996A628565CEAE07F302A70BC08D67946B1D3E462BE2A68011500DC23C05F2FB4868B03F46098E36E52600F83C81EDAE&uin=4554&fromtag=66',
               'http://58.216.6.159/amobile.music.tc.qq.com/C40000189mAI2BxJrT.m4a?guid=8232151651&vkey=F05EF2A830F02D12C13186FE9332C99AABF55FACCC3E32DB37CA7159AA6B534128ABF08AD360AAA0E5DF054AC44FA6193D0591D5593483F1&uin=4554&fromtag=66',
               'https://res.wx.qq.com/voice/getvoice?mediaid=MzU1Njc2MzY3M18yMjQ3NDg0MTkx',
               ]
        # MP3保存文件夹
        save_url = 'F:/BaiduMusic/'
        # MP3文件名
        for ur, i in zip(url, range(1, len(url) + 1)):
            file_name = '{}.mp3'.format(i)
            DownloadFile(ur, save_url, file_name)


if __name__ == '__main__':
    # login_wiki()
    # login_jira()
    download_mp3()
