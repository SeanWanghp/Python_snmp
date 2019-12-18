# coding=utf-8
# Date ：2019/11/25 9:13
__author__ = 'Maojun'
import re
import urllib.request
import gzip
import requests
from time import sleep


class Urlopenlib:
    def __init__(self):
        """https://space.bilibili.com/66821193?spm_id_from=333.999.b_62696c692d6865616465722d6d.20"""
        self.response = None
        pass

    def __del__(self):
        if self.response:
            self.response.close()
        else:
            pass

    def getHtml(self, url):
        """response.info()  web respond head content and check the code mode 'utf-8' or 'gbk'"""
        print(url)
        response = urllib.request.urlopen(url)
        print('head: ', response.info())
        print('code: ', response.getcode())   # value 200
        print('http: ', type(response))

        # read() , readline() , readlines() , fileno() , close()
        b = response.read()
        if 'baidu' in url:
            for bb in [b.decode('utf-8')]:
                if bb:
                    print('BAIDU content: {}'.format(bb))
                else:
                    pass
        elif 'www.qq.com' in url:
            data = gzip.decompress(b)
            print('QQ content: {}'.format(data.decode('gbk')))
        else:
            print('ZHIPIN content: {}'.format(b.decode('utf-8')))
        return b

    def writeFile(self, fileName, data):
        # 打开文件方式为'a'可不覆盖原有数据
        htmlFile = open(fileName, 'a')
        htmlFile.write(data)
        htmlFile.close()

    def getImgSrc(self, fileName):
        # 截取后缀为.jpg的图片, decode()将string转为byte
        imgUrl = re.findall(r'https:.+\.jpg', fileName.decode('utf-8'))
        return imgUrl

    def urlop(self):
        """no charset meaning UTF-8"""
        baiduhtml = self.getHtml('http://www.baidu.com/')

        """Content-Type: text/html; charset=GB2312    www.qq.com"""
        qqhtml = self.getHtml('http://www.qq.com/')

        """meta charset='utf-8' in head"""
        url = 'https://www.zhipin.com/?ka=header-home'
        zhipinhtml = self.getHtml(url)
        imgUrl = self.getImgSrc(zhipinhtml)
        for i in imgUrl:
            print(i)
            self.writeFile('imgUrl.txt', i)

    def basicget(self):
        geturl = 'http://www.httpbin.org/get'
        # GET
        getresponse = requests.get(url=geturl)
        print('Text: {}'.format(getresponse.text))
        print('encoding: {}'.format(getresponse.encoding))
        print('heads: {}'.format(getresponse.headers))

    def basicpost(self):
        # POST
        posturl = 'http://www.httpbin.org/post'
        postresponse = requests.post(url=posturl, data={'name': 'softpo', 'id': 'pie'})
        print(postresponse.text)
        print(postresponse.content)
        print(postresponse.headers)

    def getjpg(self):
        # get baidu jpg
        url = 'http://file02.16sucai.com/d/file/2014/0704/e53c868ee9e8e7b28c424b56afe2066d.jpg'
        baiduresponse = requests.get(url=url)
        with open('./pic/montain.jpg', mode='wb') as fp:
            content = baiduresponse.content
            fp.write(content)
            print('picture save successfully')

    def gethtmlpage(self):
        url = 'https://tieba.baidu.com/f?kw=%E6%B8%B8%E6%88%8F&ie=UTF-8&pn={}'

        for i in range(3):
            response = requests.get(url.format(i*50))
            html = response.text

            with open('./pic/%d.html' % (i+1), mode='w', encoding='utf-8') as fp:
                fp.write(html)
                print('tieba save %d success' % (i+1))

    def shangshui(self):
        # first page
        url1 = 'http://sc.chinaz.com/tupian/shanshuifengjing.html'
        # from second page
        url = 'http://sc.chinaz.com/tupian/shanshuifengjing_%d.html'

        response = requests.get(url=url1)

        # all data
        with open('./pic/shanshui.html', mode='w', encoding='utf-8') as fp:
            fp.write(response.text)
            print('web save successfully')

        # specify data with picture
        # ?遇到第一个单引号就停止
        pattern = r'<img src2="(.*?)".*?>'

        html = response.text
        image_urls = re.findall(pattern, html)

        for img_url in image_urls:
            response = requests.get(img_url)
            content = response.content
            file = img_url.rsplit('/', maxsplit=1)[1]
            print(file)
            for i in range(0, 2):
                with open('./pic/%s' % (file), mode='wb') as fp:
                    fp.write(content)
                    print('pic %s save successfully' % file)
                sleep(10)

    def lotsofpic(self):
        url1 = 'http://sc.chinaz.com/tupian/index.html'
        url2 = 'http://sc.chinaz.com/tupian/index_%d.html'
        try:
            for i in range(1):
                if i == 0:
                    url = url1
                else:
                    url = url2 % (i + 1)
                response = requests.get(url=url)
                html = response.text
                pattern = r'<img src2="(.*?)".*?>'

                img_urls = re.findall(pattern, html)
                img_names = [i.rsplit('/', maxsplit=1)[1] for i in img_urls]
                for img_url, img_name in zip(img_urls, img_names):
                    response = requests.get(img_url, timeout=5)

                    with open('./pic/%s' % img_name, mode='wb') as fp:
                        fp.write(response.content)
                        print('page %s pic %s save successfully' % (i + 1, img_name))
                    sleep(10)
        except Exception as e:
            with open('./error.txt', 'a', encoding='utf-8') as fp:
                fp.write(str(e) + '\n')


if __name__ == '__main__':
    ur = Urlopenlib()
    # ur.urlop()

    """requests lib http://www.httpbin.org
    this is a testing web, only for codeing
    HTTP methods: DELETE, GET, PATCH, POST, PUT"""
    # ur.basicget()
    # ur.basicpost()
    # ur.getjpg()
    # ur.gethtmlpage()
    ur.shangshui()
    # lotsofpic()





