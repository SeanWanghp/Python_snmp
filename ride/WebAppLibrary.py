# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__ = 'Sean Wang'
#data@:2019-07-30
#update data@:2019-xx-xx                                                                 #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
from Selenium2Library import Selenium2Library
from selenium import webdriver
import time

class WebAppLibrary(object):
    def __init__(self):
        '''
        this is a draft of selenium automation
        '''
        # driver = webdriver.Firefox()
        # driver = webdriver.Chrome()

    @classmethod
    def Web_login(self, ip, port, ff):

        if ff == 'chrome':
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--no-sandbox")
            self.driver = webdriver.Chrome(chrome_options=self.options)
        elif ff == 'firefox':
            self.driver = webdriver.Firefox(executable_path="C:\Python37\geckodriver.exe")
        self.driver.set_window_size(1920, 1080)
        # find the element that's name attribute is q (the google search box)
        self.driver.get('https://10.245.247.60:3443')
        print ('selenium start to working, wait 5 seconds and enjoy it.')
        time.sleep(5)
        return self.driver

    @classmethod
    def Web_logout(self):
        '''
        [Arguments]    ${none}
        [Documentation]
        ...
        Keyword: close_browse
        ...
        ArgSpec(args=['self', 'none')
        [Tags] @author = Sean W
        self.drive.close() will not quit the chromedriver.exe and cause robot stuck
        '''
        return self.driver.quit()

    # @classmethod
    def Web_find_element_by_id(self, id_):
        '''
        [Arguments]    ${locator}    ${selected}    ${timeout} =${30}
        [Documentation]
        ...
        Keyword: check_element
        ...
        ArgSpec(args=['self', 'locator', 'selected', 'timeout'], varargs=None, keywords=None, defaults=(30,))
        [Tags] @author = Sean W
        '''
        self.driver.find_element_by_id(id_).click()
        time.sleep(10)
        return None

    @classmethod
    def Web_find_by_name_send(self, name, key, click):
        if click == None and key:
            inputElement = self.driver.find_element_by_name(name).clear()
            inputElement = self.driver.find_element_by_name(name).send_keys(key)
            time.sleep(2)
        elif key == None and click:
            inputElement = self.driver.find_element_by_name(name).click()
            time.sleep(2)

    @classmethod
    def Web_find_by_id_send(self, id, key, click):
        print (id, key, click)
        if click == 'None' and key:
            inputElement = self.driver.find_element_by_id(id).clear()
            inputElement = self.driver.find_element_by_id(id).send_keys(key)
            time.sleep(2)
        elif key == 'None' and click:
            inputElement = self.driver.find_element_by_id(id).click()
            time.sleep(2)

    def Web_find_by_xpath_send(self, id, key, click):
        print (id, key, click)
        if click == 'None' and key:
            inputElement = self.driver.find_element_by_xpath(id).clear()
            inputElement = self.driver.find_element_by_xpath(id).send_keys(key)
            time.sleep(2)
        elif key == 'None' and click:
            inputElement = self.driver.find_element_by_xpath(id).click()
            time.sleep(2)

    def Web_smx_log_in(self, username, password):
        self.element_find_by_name_send("userName", username, None)
        self.element_find_by_name_send("password", password, None)
        self.element_find_by_id_send("btn-login", None, True)
        time.sleep(2)

    def Web_smx_log_out(self):
        self.element_find_by_xpath_send("//span[@title='admin']", None, True)
        self.element_find_by_id_send("logout", None, True)
        time.sleep(2)

    def Web_go_to_page(self, eqpt, node_path, sub_path):
        # element_find_by_xpath_send('(//*[@id="viewNodeAction"])[1]', None, True)  #also can using this method

        inputElement = self.driver.find_element_by_link_text(eqpt).click()  # link_text value 可以写成缩写， http://www.mamicode.com/info-detail-2200176.html
        if node_path != 'None':
            self.driver.find_element_by_xpath(node_path).click()  # class_name 只能取最后部分，取全称会报错（className不允许使用复合类名做参数）
            time.sleep(2)
        if sub_path != 'None':
            self.driver.find_element_by_xpath(sub_path).click()  # class_name 只能取最后部分，取全称会报错（className不允许使用复合类名做参数）
            time.sleep(2)
        time.sleep(2)

    def Web_modify_eqpt_node_items(self, eqpt, node_item, item_value, *args):

        self.element_find_by_id_send(node_item, item_value, None)
        time.sleep(2)

        # driver.find_element_by_id('ntp-server-2').clear()
        # element_find_by_id_send('ntp-server-2', "192.168.33.11", None)

        ############滚动条的移动角本#############
        # js = "windows.scrollTo(100, 1000);"
        # driver.execute_script(js)

        # js = "window.scrollTo(0,document.body.scrollHeight)"
        # driver.execute_script(js)

        # js = "var q=document.body.scrollTop=10000"
        # driver.execute_script(js)

        self.driver.find_element_by_class_name('create-btn').click()  #class_name 只能取最后部分，取全称会报错（className不允许使用复合类名做参数）
        time.sleep(5)

    def Web_clear_finish_button(self):
        # if driver.find_element_by_id('alerts-container'):
        #     print driver.find_element_by_id('alerts-container').get_attribute()
        #     print "Apply failed"
        print ("\n" + self.driver.find_element_by_class_name('alert'))
        if self.driver.find_element_by_class_name('alert') is True:
            print ("alert showing up")
            alert_content = self.driver.find_element_by_class_name('alert').text
            if alert_content.find('error'):
                print ("Apply failed")
            else: print ("Apply passed")

            time.sleep(2)
            self.driver.find_element_by_class_name('close').click()
        else:
            pass

    def Web_check_all_page_exist(self, page_name_t):

        for page_name in page_name_t:
            print ("page_name:", page_name)
            try:
                self.element_find_by_name_send(page_name, None, "click")
            except e:
                pass

            if page_name == 'Network':
                self.element_find_by_id_send("add-network-btn", None, True)
                self.element_find_by_xpath_send('//*[@id="region-node-detail-tabbar"]/li[2]/a', None, True)

            else:
                pass

    def Web_modify_eqpt_node_items_by_xpath(self, id, key, click):
        if click == True and key == None:
            self.driver.find_element_by_xpath(id).click()
