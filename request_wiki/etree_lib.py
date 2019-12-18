# coding=utf-8
# Date ：2019/12/13 9:28
__author__ = 'Maojun'
import requests
import json
import gzip
from lxml import etree
from time import sleep


def gethtmlcontent():
    """analyze html xpath and check out content"""
    data = '''<div>
                <ul>
                    <li class="item-0"><a href="link.html">first item</a></li>
                    <li class="item-1"><a href="link2.html">second item</a></li>
                </ul>
                </div>
                '''
    tree = etree.HTML(data)
    print(tree, type(tree), etree.tostring(tree).decode('utf-8'), sep='\n')

    # // checking all, / checking current(/html/body/div/ul/li)
    xpa = ['//li', '/html/body/div/ul/li']
    for xp in xpa:
        result = tree.xpath(xp)
        print(result)
        for r in result:
            print('------------', etree.tostring(r).decode('utf-8'))

    # class is label property, xpath using @ for property(属性）
    xpa = ["//li[@class='item-0']", '//a']
    for xp in xpa:
        result = tree.xpath(xp)

        for r in result:
            print('************', etree.tostring(r).decode('utf-8'))

    # get label content
    result = tree.xpath('//a/text()')
    print(result)

    result = tree.xpath('//li[contains(@class, "0")]')
    for r in result:
        print('~~~~~~~~~~~~~~~', etree.tostring(r).decode('utf-8'))


def getfromhtml():
    tree = etree.parse('sh.html')
    print(etree.tostring(tree, encoding='utf-8').decode('utf-8'))

    print(tree.xpath('//li[@id="hehe"]/text()'))
    result = tree.xpath('//div[@id="pp"]//li/a/text()')
    for r in result:
        print('---', r)


def morepic():
    url_first = 'http://sc.chinaz.com/tupian/index.html'
    url_backend = 'http://sc.chinaz.com/tupian/index_%d.html'

    for i in range(1, 2):
        if i is 1:
            url = url_first
        else:
            url = url_backend % i
        response = requests.get(url)
        text = response.text
        tree = etree.HTML(text)

        # @src2表示需要得到属性
        images = tree.xpath('//img/@src2')
        print(images)
        for image_url in images:
            response = requests.get(image_url)
            file_name = image_url.rsplit('/', maxsplit=1)[-1]
            with open('./pic/%s' % file_name, mode='wb') as fp:
                fp.write(response.content)
                print('pic %s save success' % file_name)
            sleep(1)


def xpathgetcontent():
    url_first = 'http://tieba.baidu.com/f?kw=%E4%B8%AD%E5%9B%BD&ie=utf-8&pn=0'
    url_first = 'https://www.qiushibaike.com/text'
    url_first = 'https://www.telnote.cn/xiaohua/zonghe/'
    url_backend = 'https://www.telnote.cn/xiaohua/zonghe/list_{}.htm'
    # url_backend = 'https://www.qiushibaike.com/text/page/%d'
    # url_backend = 'http://tieba.baidu.com/f?kw=%E4%B8%AD%E5%9B%BD&ie=utf-8&pn={}'

    # headers find in 'inspect-> Network -> Filter(find place) -> F5 then selected the first one of 'Name' part
    # -> Headers -> find out 'User-Agent', 'Host', 'Accept-Language'
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                          'Chrome/79.0.3945.79 Safari/537.36',
    #            'Host': 'tieba.baidu.com',
    #            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'}

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/79.0.3945.79 Safari/537.36',
               'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
               'Host': 'www.telnote.cn',
               'Referer': 'https://www.telnote.cn/xiaohua/zonghe/list_3.htm',
               }

    fp = open('./baishi.txt', mode='a', encoding='utf-8')
    fp2 = open('./baishi.json', mode='w', encoding='utf-8')
    url = ''
    data = []
    for i in range(2, 4):
        if i is 2:
            url = url_first
        else:
            url = url_backend.format(i-1)
            pass

        print(url)
        response = requests.get(url=url, headers=headers)
        # response = requests.get(url=url)
        # check the coding mode
        print(response.apparent_encoding)
        # print(response.content.decode('gbk'))
        tree = etree.HTML(response.content)
        # print(tree)

        # '//li[@class=" j_thread_list clearfix"]/div', '//ul[@id="thread_list"]/li'
        # This can works: '//div[@id="content"]/div', ''
        # '//div[@id="pagelet_frs-base/pagelet/content"]/'
        # divs = tree.xpath('//div[@id="content-lef"]/div')
        # divs = tree.xpath('//div[@class="W_linka"]/div')
        divs = tree.xpath('//dd[@class="content"]')

        print(len(divs))
        # print(etree.tostring(divs[0], encoding='utf-8').decode('utf-8'))

        for divv, vv in zip(divs, range(len(divs))):
            # print("divv: {}".format(etree.tostring(divv, encoding='utf-8').decode('utf-8')))
            author = divv.xpath('//dd/h1/a/text()')[vv]
            print('author: {}'.format(author))
            content = divv.xpath('//dd/dl/text()')[vv]
            for con in [content]:
                if con.strip():
                    print('content: {}'.format(con.encode('utf-8').decode('utf-8')))

            # ./ find from current folder
            # author = div.xpath('.//h2/text()')[0]
            # content = div.xpath('.//span/text()')[0]
            # laugh, comments = div.xpath('.//i@class="number"]/text()')
            # print(author, content, laugh, comments)
            # fp.write('author: {}; joke: {}; funny: {}; comments: {}'.format(author, content, laugh, comments))
            # d['author'] = author
            # d['joke'] = content
            # d['laugh'] = laugh
            # d['comments'] = comments
            # data.append(d)
            # print('one joke save successfully')

    # fp.close()
    # # using json for data list
    # result = json.dumps(data, ensure_ascii=False)
    # fp2.write(result)
    # fp2.close()


def find51job():
    key = input("input job keyword: ")

    url = url%(key)

    response = requests.get(url)
    response.encoding = 'gbk'


if __name__ == '__main__':
    # gethtmlcontent()
    # getfromhtml()
    # morepic()
    xpathgetcontent()
