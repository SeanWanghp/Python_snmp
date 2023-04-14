import re
import time
import select
from Login import Login
import os
import yaml

class VMMethod(Login):
    def __init__(self):
        super(VMMethod, self).__init__()
        pass

    def cpu_use(self):
        output = self.command_vm('top -n1 | fgrep "Cpu(s)"')
        rest = output.split('\r\n')[1].split()
        index = 0
        for i in range(len(rest)):
            if 'id' in rest[i]:
                index = i - 1
                break
        rest = rest[index]
        try:
            usage = 100 - float(rest)
        except Exception as e:
            rest = rest.split('[1m')[1]
            usage = 100 - float(rest)
        return usage/100.0

    def mem_use(self):
        output = self.command_vm('free').split('\r\n')
        result = 0.0
        for line in output:
            if 'Mem' in line:
                line = line.split()
                total = float(line[1])
                used = float(line[2])
                result = used / total
                break
        return result

    def disk_use(self):
        output = self.command_vm('df').split('\r\n')
        res = ''
        for line in output:
            # if '/dev/mapper/centos-root' in line:
            if '/dev/mapper/centos' in line:
                res = line.split()[4].replace('%', '')

        res = float(res) / 100
        return res