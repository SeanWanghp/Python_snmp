# coding=utf-8
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2017-3-2
# coding=gbk
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word

import unittest, os
from selenium import webdriver
from telnetlib import Telnet
from time import sleep

import HTMLTestRunner

'''
this is a draft for unittest with HTML report
'''
class TestDiv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enter = '\r\n'
        cls.res = ''
        cls.type = None
        cls.driver = webdriver.Chrome()
        cls.driver.get('http://www.baidu.com')
        cls._testcase = {}
        cls._name = cls._testcase['name'] = 'Not Set'


    @classmethod  #will only run one time, setupClass added
    def tearDownClass(cls):
        cls.driver.quit()

    def test_001(self):
        self.assertEqual(self.driver.title, u'百度一下，你就知道')

    def test_002(self):
        self.assertTrue(self.driver.find_element_by_id('kw').is_enabled())

    def test_003(self):
        self.assertIsNot(self.driver.current_url,'www.baidu.com')
        print "sef._name:", self._name
        print "sef._testcase:", self._testcase
        print self._testcase['name']
        from smx_upgrade import cli
        b = cli('10.245.247.60', 23, None)
        # getattr(b, 'timeout', setattr(b, 'timeout', 20))    #用来设置变量和改变值
        # b.cli_lines('install-activate-PMA-BML-116.bin')

    def test_004(self):  ######需要用PYTHON自带的IDLE才能产生报告
        self.session = Telnet('10.245.247.60', 23)
        if self.type == None:
            self.res += self.session.read_until("login: ")
            self.session.write("admin" + self.enter)
            self.res += self.session.read_until(": ")
            self.session.write("admin" + self.enter)
            self.res += self.session.read_until("$ ", 5)
            self.session.write("pwd" + self.enter)
            self.res += self.session.read_until("$ ", 5)
            self.session.write("exit" + self.enter)
            print self.res

    @unittest.skip("i don't want to run this case.")
    def test_005(self):
        self.assertIsNot(self.driver.current_url, 'www.baidu.com')
        # from smx_upgrade import cli
        # b = cli('10.245.247.60', 23, None)
        # b.cli_lines('install-activate-PMA-BML-116.bin')


if __name__ == '__main__':
    report_path = os.getcwd() + "\\testReport.html"

    suite = unittest.TestLoader().loadTestsFromTestCase(TestDiv)
    with open(report_path, "wb") as outfile:
        runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,
                                               title=u'自动化测试报告',
                                               description=u'SEAN的测试结果如下:')
        runner.run(suite)