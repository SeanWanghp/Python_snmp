from MaojunLibrary.TelLibrary import TelnetLibrary
from MaojunLibrary.App import App, App_Web, App_SSH, App_IXIA
from MaojunLibrary.MobileAppLibrary import MobileAppLibrary

class MaojunLibrary(TelnetLibrary, App, App_Web, App_SSH, App_IXIA):
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


'''https://www.cnblogs.com/apple2016/p/7274829.html         ROBOT will stuck and can not running with lots of process
https://blog.csdn.net/teamo_mc/article/details/83856891     python2&3 running at same time'''

'''12306 python code
12306项目传送门：
https://github.com/testerSunshine/12306
py12306项目传送门：
https://github.com/pjialin/py12306/
'''