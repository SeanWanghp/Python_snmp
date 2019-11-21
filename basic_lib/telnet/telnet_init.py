# coding=utf-8
__author__ = 'Sean Wang'
#data@:2018-09-20
from telnetlib import Telnet
import time


class myTelnet(Telnet):
    """让此类继承于标准库中的Telnet, 自定义的telnet类
    作用：引用系统标准库telnetlib，在标准库的基础上创建自己熟悉的方法
    """
    def __init__(self, HOST=None, PORT=23, TIMEOUT=None, USER=None, PD=None, chk_err=r"((E|e)rror)|((F|f)ailed)",
                 chk_user=None, chk_password=None, chk_success=None):
        if not TIMEOUT:
            # 如果超时时间没有设置则调用父类构造方法进行初始化
            # super(myTelnet, self).__init__(host=HOST, port=PORT)
            Telnet.__init__(self, host=HOST, port=PORT)
        else:
            # super(myTelnet, self).__init__(host=HOST, port=PORT,timeout=TIMEOUT)
            Telnet.__init__(self, host=HOST, port=PORT, timeout=TIMEOUT)

        print("self:", self.__dict__)
        """调用父类初始化后，检查相关参数，如果关键参数缺失则直接返回异常,否则直接使用参数自动登录并返回结果
        self.sock
        USER 			用户名
        PD 				密码
        chk_user 		输入用户名提示字符串
        chk_password 	输入密码提示字符串
        chk_success 	登录成功提示字符串
        """
        if (not self.sock) or (not USER) or (not PD) or (not chk_user) or (not chk_password) or (not chk_success):
            self. login = False
        else:
            self. login = self.tel_login(USER, PD, chk_err, chk_user, chk_password, chk_success)
            # self.login 是类变量，可以用此参数检查是否已经成功登录

    def tel_login(self, USER=None, PD=None, chk_err=r"((E|e)rror)|((F|f)ailed)",
                  chk_user=None, chk_password=None, chk_success=None):
        """登录 :由构造函数自动执行 也可直接调用当前方法
        USER 用户名；PD 密码；chk_err 异常检测关键字符；
        chk_user 输入用户名提示字符串；chk_password 输入密码提示字符串；
        chk_success	登录成功提示字符串
        返回值：登录成功返回True ，否则返回False 赋值给类属性login 以判断是否登录
        """
        if (not USER) or (not PD) or (not chk_user) or (not chk_password) or (not chk_success):
            return False  # 如果参数不全则直接返回False
        chkList = [chk_err, chk_user, chk_password, chk_success]
        for i in range(len(chkList)):
            """从telnet服务端返回的是二进制字符串，此处也得使用同样类型
            chkList[i]=bytes(chkList[i],"utf-8")
            """
            chkList[i] = bytes(chkList[i])
        # 读取建立连接时返回的数据，查看是否是提示输入用户名
        readBack = self.expect(chkList)

        if readBack[0] == 1:  # 即提示输入用户名
            # self.write(bytes(USER+"\r\n",'utf-8'))
            self.write(bytes(USER + "\r\n"))
        else:
            return False
        readBack = self.expect(chkList)
        if readBack[0] == 2:  # 即提示输入密码！
            # self.write(bytes(PD+"\r\n",'utf-8'))
            self.write(bytes(PD + "\r\n"))
        else:
            return False
        readBack = self.expect(chkList)
        print ('aaaa:', readBack[0])
        if readBack[0] == 3:  # 即提示登录成功
            self.user = USER
            return True
        else:
            return False

    def writeToRead(self, writeLine=None, write_err=r"((E|e)rror)|((F|f)ailed)", write_success=None,
                    chkListStr=[], reWrite=None, return_bool=True):
        """写入一行文本并返回执行结果
        telobj telnet连接对象；
        writeLine 要写入的字符串；
        write_err 执行错误检测字符串；
        write_success 执行成功的字符串；当检测到此值时程序会结束运行，视return_bool的情况，返回True或者是所有返回的内容
        chkListStr 在返回值中要检测的字符串；检测到这其中的任意一个值时才可能执行重写入过程！
        reWrite 当检测到 chkListStr 中内容时所要重新写入的字符串
        return_bool=True 是否返回内容，如不返回则返回bool值
        """
        if (not writeLine) or (not write_success):
            return False  # 没有要写入的内容 或者是没有检测执行成功的字符串则直接返回
        # writeLine = bytes(writeLine+"\r\n",'utf-8') #将输入字符加上回车符并转成二进制文本
        writeLine = bytes(writeLine + "\r\n")
        chkListStr.append(write_success)  # 将执行成功检测字符串加入到列表的最后
        chkListStr.insert(0, write_err)  # 将执行失败检测字符串加入到最前
        for i in range(len(chkListStr)):
            # chkListStr[i]=bytes(chkListStr[i],'utf-8')#将检测字符串转成二进制字符串
            chkListStr[i] = bytes(chkListStr[i])
        self.write(writeLine)
        lsstr = b""
        while True:
            readBack = self.expect(chkListStr)
            if readBack[0] == 0:  # 此时检测到异常
                return False
            elif readBack[0] == len(chkListStr) - 1:  # 此时检测到执行成功
                if return_bool:  # 当需要返回字符时则返回字符，否则返回True
                    return lsstr + readBack[2]
                else:
                    return True
            else:  # 此时是检测到用户输入的chkListStr 字符串，调用回调函数
                if not reWrite:
                    return False
                else:
                    if not isinstance(reWrite, bytes):
                        # reWrite=bytes(reWrite+"\r\n",'utf-8')
                        reWrite = bytes(reWrite + "\r\n")
                    lsstr += readBack[2]
                    self.write(reWrite)


if __name__ == '__main__':
    tn = myTelnet(
        HOST="10.245.46.213",
        USER="sysadmin",
        PD="sysadmin",
        chk_user="NGPON2X4 login: ",
        chk_password="Password: ",
        chk_success="# "
    )

    if tn.login:
        f = open("cli.txt", "wb")
        f.write(bytes(time.strftime("%Y-%m-%d %X")) + b"\r\n")
        line = tn.writeToRead(
            writeLine="show vlan",
            write_success="# ",
            chkListStr=["More"],
            reWrite=" "
        )
        f.write(line)
        f.close()
        print('true')
    else:
        print('no login!')
