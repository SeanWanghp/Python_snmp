from MaojunLibrary.TelLibrary import TelnetLibrary
from MaojunLibrary.App import App, App_Web, App_SSH, App_IXIA, App_Snmp
from MaojunLibrary.MobileAppLibrary import MobileAppLibrary

class MaojunLibrary(TelnetLibrary, App, App_Web, App_SSH, App_IXIA, App_Snmp):
    '''
    this is new lib for current RIDE
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

'''MyClass.run_cli()'''
'''MobileAppLibrary.click_element()'''
'''App.App_click_element()'''
'''App_Web.App_web_find_element_by_id()'''
# a = TelnetLibrary()
# a.tel_axos('10.245.46.208', 23, 'sysadmin', 'seanwang')
# a.cli('show card', '# ')

# App_SSH().ssh_('10.245.46.208')
# App_SSH().session_command('show inter sum')
# App_Snmp().App_snmp_walk('10.245.46.216', 161, 'public', 'v2')

'''https://www.cnblogs.com/apple2016/p/7274829.html         ROBOT will stuck and can not running with lots of process
https://blog.csdn.net/teamo_mc/article/details/83856891     python2&3 running at same time
Anaconda和Pycharm的安装和配置 https://www.anaconda.com/download/#windows
kite for AI python:  https://www.kite.com/download/
tensorflow for AI python:
http://www.tensorfly.cn/tfdoc/get_started/os_setup.html

ML and AI learing from YOUTUBER(VERY GOOD FOR STUDY):  
https://www.youtube.com/watch?v=WFr2WgN9_xE&feature=push-fr&attr_tag=1lGXdO_7F1ErGN8z%3A6
Good VIDEO for TKINTER:
https://www.youtube.com/watch?v=YXPyB4XeYLA&feature=push-fr&attr_tag=tGRvWZyeBXIf5sD-%3A6

REALPYTHON:
https://realpython.com/lessons/two-threads/

Danbader:
https://dbader.org/blog/python-file-io
'''


'''12306 python code
12306项目传送门：
https://github.com/testerSunshine/12306
py12306项目传送门：
https://github.com/pjialin/py12306/
'''