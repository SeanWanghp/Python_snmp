# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Sean Wang'
#data@:2018-02-22
# coding=gbk                                                                    #spell inspection cancelled
#print out.decode('gbk').encode('utf-8')   #output have Chinese word and English word
#######################http://blog.csdn.net/huilan_same/article/details/52594354#################

####XPATH find by this web("chorme debug xpath"): http://yizeng.me/2014/03/23/evaluate-and-validate-xpath-css-selectors-in-chrome-developer-tools/

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# coding=utf-8
from selenium import webdriver
from time import sleep

from contextlib import contextmanager
'''
driver.find_element("id", "kw").send_keys("yoyoketang")
driver.find_element('css selector', "#su").click()

# 其它定位参考 交流QQ群：232607095
# t1 = driver.find_element("link text", "糯米").text
# t2 = driver.find_element("name", "tj_trnews").text
# t3 = driver.find_element("class name", "bri").text


http://blog.csdn.net/eastmount/article/details/48108259

find_element_by_id
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector

下面是查找多个元素（这些方法将返回一个列表）：
find_elements_by_id
find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector

定位username元素的方法如下：
username = driver.find_element_by_xpath("//form[input/@name='username']")  
username = driver.find_element_by_xpath("//form[@id='loginForm']/input[1]")  
username = driver.find_element_by_xpath("//input[@name='username']") 

操作元素方法
    clear 清除元素的内容
    send_keys 模拟按键输入
    click 点击元素
    submit 提交表单 
    
WebElement接口获取值
    size 获取元素的尺寸
    text 获取元素的文本
    get_attribute(name) 获取属性值
    location 获取元素坐标，先找到要获取的元素，再调用该方法
    page_source 返回页面源码
    driver.title 返回页面标题
    current_url 获取当前页面的URL
    is_displayed() 设置该元素是否可见
    is_enabled() 判断元素是否被使用
    is_selected() 判断元素是否被选中
    tag_name 返回元素的tagName
    
鼠标操作
    context_click(elem) 右击鼠标点击元素elem，另存为等行为
    double_click(elem) 双击鼠标点击元素elem，地图web可实现放大功能
    drag_and_drop(source,target) 拖动鼠标，源元素按下左键移动至目标元素释放
    move_to_element(elem) 鼠标移动到一个元素上
    click_and_hold(elem) 按下鼠标左键在一个元素上
    perform() 在通过调用该函数执行ActionChains中存储行为
    
    
    
键盘操作
    send_keys(Keys.ENTER) 按下回车键
    send_keys(Keys.TAB) 按下Tab制表键
    send_keys(Keys.SPACE) 按下空格键space
    send_keys(Kyes.ESCAPE) 按下回退键Esc
    send_keys(Keys.BACK_SPACE) 按下删除键BackSpace
    send_keys(Keys.SHIFT) 按下shift键
    send_keys(Keys.CONTROL) 按下Ctrl键
    send_keys(Keys.ARROW_DOWN) 按下鼠标光标向下按键
    send_keys(Keys.CONTROL,'a') 组合键全选Ctrl+A
    send_keys(Keys.CONTROL,'c') 组合键复制Ctrl+C
    send_keys(Keys.CONTROL,'x') 组合键剪切Ctrl+X
    send_keys(Keys.CONTROL,'v') 组合键粘贴Ctrl+V
'''



class axos_web(object):
    def __init__(self, driver):
        self.driver = driver

    def element_find_by_name_send(self, name, key, click):
        if click == None and key:
            inputElement = self.driver.find_element_by_name(name).clear()
            inputElement = self.driver.find_element_by_name(name).send_keys(key)
            time.sleep(5)
        elif key == None and click:
            inputElement = self.driver.find_element_by_name(name).click()
            time.sleep(5)

    def element_find_by_id_send(self, id, key, click):
        print id, key, click
        if click == None and key:
            inputElement = self.driver.find_element_by_id(id).clear()
            inputElement = self.driver.find_element_by_id(id).send_keys(key)
            time.sleep(5)
        elif key == None and click:
            inputElement = self.driver.find_element_by_id(id).click()
            time.sleep(5)

    def element_find_by_xpath_send(self, id, key, click):
        print id, key, click
        if click == None and key:
            inputElement = self.driver.find_element_by_xpath(id).clear()
            inputElement = self.driver.find_element_by_xpath(id).send_keys(key)
            time.sleep(5)
        elif key == None and click:
            inputElement = self.driver.find_element_by_xpath(id).click()
            time.sleep(5)


    def log_in(self, username, password):
        self.element_find_by_name_send("userName", username, None)
        self.element_find_by_name_send("password", password, None)
        self.element_find_by_id_send("btn-login", None, True)
        time.sleep(5)

    def log_out(self):
        self.element_find_by_xpath_send("//span[@title='admin']", None, True)
        self.element_find_by_id_send("logout", None, True)
        time.sleep(5)


    def go_to_page(self, eqpt, node_path, sub_path):
        # element_find_by_xpath_send('(//*[@id="viewNodeAction"])[1]', None, True)  #also can using this method

        inputElement = self.driver.find_element_by_link_text(eqpt).click()  # link_text value 可以写成缩写， http://www.mamicode.com/info-detail-2200176.html
        if node_path != 'None':
            self.driver.find_element_by_xpath(node_path).click()  # class_name 只能取最后部分，取全称会报错（className不允许使用复合类名做参数）
            time.sleep(2)
        if sub_path != 'None':
            self.driver.find_element_by_xpath(sub_path).click()  # class_name 只能取最后部分，取全称会报错（className不允许使用复合类名做参数）
            time.sleep(2)
        time.sleep(2)

    def modify_eqpt_node_items(self, eqpt, node_item, item_value, *args):

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




    def clear_finish_button(self):
        # if driver.find_element_by_id('alerts-container'):
        #     print driver.find_element_by_id('alerts-container').get_attribute()
        #     print "Apply failed"
        print "\n" + self.driver.find_element_by_class_name('alert')

        if self.driver.find_element_by_class_name('alert') == True:
            print "alert showing up"
            alert_content = self.driver.find_element_by_class_name('alert').text
            if alert_content.find('error'):
                print "Apply failed"
            else: print "Apply passed"

            time.sleep(2)
            self.driver.find_element_by_class_name('close').click()
        else: pass


    def check_all_page_exist(self, page_name_t):

        for page_name in page_name_t:
            print "page_name:", page_name
            try:
                self.element_find_by_name_send(page_name, None, "click")
            except:
                pass

            if page_name == 'Network':
                self.element_find_by_id_send("add-network-btn", None, True)
                self.element_find_by_xpath_send('//*[@id="region-node-detail-tabbar"]/li[2]/a', None, True)

            else:
                pass


    def modify_eqpt_node_items_by_xpath(self, id, key, click):
        if click == True and key == None:
            self.driver.find_element_by_xpath(id).click()

##############CASE STEP AS FOLLOWING
if __name__ == "__main__":
    '''
    this is a draft of selenium automation
    '''
    # driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    driver.get('https://10.245.247.60:3443')

    driver.set_window_size(1920, 1080)
    # find the element that's name attribute is q (the google search box)
    print 'selenium start to working, please enjoy it.'
    time.sleep(5)
    run_web = axos_web(driver)

    while True:
        run_web.log_in("admin", "test123")
        eqpt_id = driver.find_element_by_xpath("(//*[@id='viewNodeAction'])[1]").text
        time.sleep(2)
        print "AXOS_ID: ", eqpt_id
        run_web.go_to_page(eqpt_id, '//a[text()="VLAN"]', '//a[text()="Transport Service Profile"]')
        # run_web.go_to_page("ngpon", 'None', 'None')
        # run_web.modify_eqpt_node_items("ngpon", "Contact", "maojunwan@163.com", None)
        # run_web.modify_eqpt_node_items_by_xpath('//input[@id="CLITelnet_disable"]', None, True)
        # run_web.clear_finish_button()

        page_name_t =("Topology", "Subscriber", "Reports", "Auditlog", "Alarms", "System", "Profiles", "Templates", "Workflows", "Network")
        page_name_t =("Network", "System", "Profiles", "Templates", "Workflows")
        run_web.check_all_page_exist(page_name_t)
        run_web.log_out()
        time.sleep(5)