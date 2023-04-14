import time
import paramiko
import select
import re
import yaml


class SSH:
    def __init__(self):
        self.ssh = None
        # self.ssh2 = None
        self.ip = None
        self.port = 22
        self.username = None
        self.password = None
        self.cli_finish_flag = None

        # avoid dead cycle
        self.timer = 100

    def olt_login(self, ip):
        self.ip = ip
        # root permissions login
        self.username = 'calixsupport'
        self.password = 'calixsupport'

    def command(self, com):
        """CLI command running"""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password,
                         allow_agent=False, timeout=30,auth_timeout=30,banner_timeout=30)
        t1,output,t2 = self.ssh.exec_command(com)
        output = output.readlines()
        return output