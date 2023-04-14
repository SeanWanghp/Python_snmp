import time
import paramiko
import select
from Dao import MysqlDb
from ecrack import crack
import re
import yaml
from Setting import ISDEBUG, ftp_info, TESTBEDS_INFO


class Login:
    def __init__(self):
        self.ssh = None
        self.ssh2 = None
        self.ip = None
        self.port = None
        self.username = None
        self.password = None
        self.debug = ISDEBUG
        self.cli_finish_flag = None

        # avoid dead cycle
        self.timer = 100

        # FTP server information
        self.ftp_port = ftp_info['port']
        self.root_dir = ftp_info['root_dir']
        self.ftp_user = ftp_info['user']
        self.ftp_pwd = ftp_info['pwd']
        self.ftp_host = ftp_info['host']

    # debug mode login
    def debugLogin(self):
        output = str(self.command("shell"))
        crack_info = re.search(r"\S+\s\w+\s\w+\s\w+\d+\s[\d:]+\s\d+", output)
        assert crack_info != None, "'root' login failed!! Can't match the string used for ecrack.py"
        crack_info = crack_info.group().split()
        # use ecrack.py to get the password
        date = crack_info[1:6]
        hostId = crack_info[0]
        pwd = crack(date=date, hostId=hostId)
        assert len(pwd) == 1, "'root' login failed!! len(pwd) > 1, which has not been processed yet"
        pwd = pwd[0]
        self.command(pwd)
        self.command("\n")

    def change_config(self):
        # Skip initial msg
        output = self.command("show run aaa")
        pattern = r"aaa authentication-order \S+"
        match = re.search(pattern, output)
        if match == None:
            return None
        else:
            pre_config = match.group().split()[2]
            if pre_config == "radius-if-up-else-local":
                self.command("config")
                self.command("aaa authentication-order local")
                self.command("exit")
                return pre_config
            return None

    def change_config_back(self, pre_config):
        if pre_config != None:
            self.command("config")
            self.command("aaa authentication-order " + str(pre_config))
            self.command("exit")
        else:
            pass

    def check_olt(self, ):
        """SSH main"""
        db = MysqlDb()
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password,allow_agent=False)
            sql = f'update {TESTBEDS_INFO} set connected = 1 where ip=\'{self.ip}\''
            db.execute_db(sql)
        except Exception as e:
            sql = f'update {TESTBEDS_INFO} set connected = 0 where ip=\'{self.ip}\''
            db.execute_db(sql)
            assert False, str(self.ip)+'无法连接'


        self.ssh2 = self.ssh.invoke_shell()
        self.ssh2.send(b"\n")

        # get the finish flag of each command
        time.sleep(10)
        output = str(self.ssh2.recv(999999999), encoding='utf-8')

        temp = re.search('ssh on \S+', output)
        temp = temp.group().split()[-1]
        self.cli_finish_flag = [temp + "#", temp + '(config)#', "root@" + temp, "Enter calixsupport role password"]

        return self.ssh2

    def check_vm(self):
        db = MysqlDb()
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password,allow_agent=False)
            sql = f'update {TESTBEDS_INFO} set connected = 1 where ip=\'{self.ip}\''
            db.execute_db(sql)
        except Exception as e:
            sql = f'update {TESTBEDS_INFO} set connected = 0 where ip=\'{self.ip}\''
            db.execute_db(sql)
            assert False, str(self.ip) + '无法连接'
        self.ssh2 = self.ssh.invoke_shell()
        self.ssh2.send(b"\n")

        time.sleep(10)
        output = str(self.ssh2.recv(999999999), encoding='utf-8')

        return self.ssh2

    def command(self, com, t=2):
        """CLI command running"""
        if self.debug:
            print(f"com {self.ip}: ", com)
        self.ssh2.send(com + "\n")
        output = ""
        # avoid endless loop
        timer = self.timer
        while timer:
            rl, wl, xl = select.select([self.ssh2], [], [], 0.0)
            if len(rl) > 0:
                assert 'unconnected' not in str(rl), 'Session has been closed'
                recv = str(self.ssh2.recv(9999999), encoding='utf-8')
                output += recv
                # if finish flag exists , then break
                if len([x for x in self.cli_finish_flag if x in recv]) != 0:
                    break
                if com == 'exit':
                    time.sleep(1)
                    recv = str(self.ssh2.recv(9999999), encoding='utf-8')
                    break
                timer = self.timer
            timer -= 1
            time.sleep(t)
        assert timer != 0, ' The remote server is not responding…… (Command: \"' + com + '\")'
        # if self.debug:
        #     print(output.replace('\r', ''))
        return output

    def command_vm(self, com, t=5):
        if self.debug:
            print(f"com {self.ip}: ", com)
        self.ssh2.send(com + "\n")
        time.sleep(t)
        output = str(self.ssh2.recv(9999999),encoding = 'utf-8')
        return output

