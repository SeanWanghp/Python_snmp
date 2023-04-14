import re
import time
from Login import Login
import os
import yaml
from Setting import ISROOT

def ReFind(str1, march, start=0):
    """Search all the string find out all the text which fullfill the re

    Args:
        str1 (string): the string which going to be search
        march (Match type of the re.compile()): your re.compile()type
        start (int, optional): start position of the string . Defaults to 0.

    Returns:
        string: all the text which founded
    """
    searchres = march.search(str1, start)
    if searchres is not None:
        TmpResut = searchres.group()
        startPos = searchres.end()
        if startPos < len(str1):
            a = ReFind(str1, march, startPos)
            if a is not None:
                TmpResut += ',' + a
            return TmpResut
        else:
            return TmpResut
    else:
        return None


class CPU(Login):
    def __init__(self, ):
        super(CPU, self).__init__()
        pass

    def cpu_cal(self, ):
        """check out OLT CPU
        action: need check out which value is high and not accepted"""
        cpu_match = 0.0
        self.command('show card')
        command_line = "show system process"
        output = self.command(command_line)
        patt = r"root\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\w\s+(\d+.\d)"
        cpu1_pattern = re.compile(patt)
        cpu1_match = cpu1_pattern.findall(output)
        for cpu1 in cpu1_match:
            # print(float(cpu1))
            cpu_match += float(cpu1)
        self.ssh2.send(("\003" + "\r").encode('utf-8'))
        time.sleep(1)
        output = self.ssh2.recv(3000)

        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        return [cpu_match / 4], clock

    def cpu_cal_card(self, number, ):
        """check out OLT CPU
        action: need check out which value is high and not accepted"""
        cpu_match = 0.0
        self.command('show card')
        command_line = "show info {}".format(number)
        output = self.command(command_line)
        patt = r"cpu-usage\s+(\d+)\s+%"
        cpu1_pattern = re.compile(patt)
        cpu1_match = cpu1_pattern.findall(output)
        for cpu1 in cpu1_match:
            # print(float(cpu1))
            cpu_match += float(cpu1)
        self.ssh2.send(("\003" + "\r").encode('utf-8'))
        time.sleep(1)
        output = self.ssh2.recv(3000)

        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        return [cpu_match], clock


class Memory(Login):
    def __init__(self, ):
        super(Memory, self).__init__()
        pass

    def mem_cal(self, ):
        """check out OLT memory"""
        mem_match = 0
        command_line = "show system process"
        output = self.command(command_line)
        patt = r"root\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\w\s+\d+.\d\s+(\d+.\d)"
        mem1_pattern = re.compile(patt)
        mem1_match = mem1_pattern.findall(output)
        for mem1 in mem1_match:
            mem_match += float(mem1)
        self.ssh2.send(("\003" + "\r").encode('utf-8'))
        time.sleep(1)
        output = self.ssh2.recv(3000)

        clock = re.search(r'\".+\"', self.command("show clock"))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        return [mem_match], clock

    def mem_cal_card(self, number, ):
        """check out OLT memory"""
        mem_match = 0
        command_line = "show info {}".format(number)
        output = self.command(command_line)
        patt = r"ram-usage\s+(\d+)\s+%"
        mem1_pattern = re.compile(patt)
        mem1_match = mem1_pattern.findall(output)

        for mem1 in mem1_match:
            mem_match += float(mem1)
        self.ssh2.send(("\003" + "\r").encode('utf-8'))
        time.sleep(1)
        output = self.ssh2.recv(3000)

        clock = re.search(r'\".+\"', self.command("show clock"))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        return [mem_match], clock

    def mem_check_log(self, name):
        """check lmd memory
        action :still need find all for two cards
        wang1>debug
        Entering character mode
        Escape character is '^]'.
        calix E5 Debug Interface

        wang1:1.2:> cd /fw
        wang1:1.2:/fw> memdb show

        root@localhost:~# cat /proc/meminfo
                MemTotal:        1915284 kB
                MemFree:          553140 kB"""

        command_line = f"cat /var/log/mem_check/{name}.log"
        output = self.command(command_line)
        if re.search('No such file or directory', output) is not None:
            return 0, 0
        data = output.split('\r\r\n')[-2]
        TIME = data.split(',')[0]
        memory = data.split(',')[1].split()[1]

        return TIME, memory

    def mem_top_log(self):
        command_line = f"cat /var/log/mem_check_results.log"
        output = self.command(command_line)

        output = output.split('\r\r\n')
        start = 0
        end = 0
        for i in range(len(output)-1,-1,-1):
            if 'DM_name' in output[i]:
                start = i+1
                break
            if 'Note' in output[i]:
                end = i
            if i == 0:
                start = 1

        DM_name = []
        inc = []
        top = []
        if start < end:
            for i in range(start,end):
                line = output[i]
                DM_name.append(line.split()[0])
                inc.append(float(line.split()[3])/float(line.split()[1]))
            for i in range(3):
                mx = 0
                for j in range(len(inc)):
                    if inc[j] > inc[mx]:
                        mx = j
                top.append([DM_name[mx],inc[mx]])
                inc[mx] = 0
        else:
            top = [[-1,-1],[-1,-1],[-1,-1]]
        return top



class Alarm(Login):
    def __init__(self, ):
        super(Alarm, self).__init__()
        pass

    def active_alarm_check(self, ):
        """check active alarm"""
        alarm_label = 'perceived-severity'
        # if self.username == root_username:
        #     self.command('cli')
        self.command('pag false')
        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]
        crital_value = 0
        major_value = 0
        minor_value = 0
        info_value = 0
        command_line = "show alarm active"
        output = self.command(command_line, t=5)
        if alarm_label in output:
            for line in output.splitlines():
                if alarm_label in line:
                    alarm_pattern = re.compile("perceived-severity\s+(\w+)")
                    alarm_match = re.search(alarm_pattern, line)
                    if alarm_match.group(1) == 'CRITICAL':
                        crital_value += 1
                    elif alarm_match.group(1) == 'MAJOR':
                        major_value += 1
                    elif alarm_match.group(1) == 'MINOR':
                        minor_value += 1
                    elif alarm_match.group(1) == 'INFO':
                        info_value += 1
                    else:
                        pass
                else:
                    pass
            # if self.username == root_username:
            #     self.command('exit')
            return [crital_value, major_value, minor_value, info_value], clock
        else:
            pass
            # if self.username == root_username:
            #     self.command('exit')
            return [0,0,0,0], clock

    def ont_alarm_check(self, ):
        self.command("\n")
        """check active alarm"""
        ont_miss = 'missing'
        ont_departure = 'departure'
        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]
        ont_miss_value = 0
        ont_departure_value = 0

        command_line = ['show ont status | include missing']
        for command in command_line:
            output = self.command(command, t=5)
            if ont_miss or ont_departure in output:
                for line in output.splitlines():
                    if ont_miss in line or ont_departure in line:
                        alarm_pattern = re.compile("\s+oper-state\s+(\w+)")
                        alarm_match = re.search(alarm_pattern, line)
                        if alarm_match:
                            if alarm_match.group(1) == 'missing':
                                ont_miss_value += 1
                            if alarm_match.group(1) == 'departure':
                                ont_departure_value += 1
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
            else:
                pass

            self.command("\n")
        return [ont_miss_value, ont_departure_value], clock


class Other(Login):
    def __init__(self, ):
        super(Other, self).__init__()
        pass

    # root cli
    def uptime(self, ):
        """check system uptime"""
        command_line = "dcli ifmgrd debug timers"
        output = self.command(command_line)
        uptime_pattern = re.compile("SysUpTime is\s(\d+).\d+\s+secs")
        uptime_match = re.search(uptime_pattern, output)
        if self.debug:
            assert uptime_match != None, "IP={}".format(self.ip)

        """check each card uptime"""
        # check cards' number (1 or 2)
        if ISROOT:
            self.command("exit")
        self.command("pag false")
        # get clock
        msg = self.command("show info")

        # check the cards' number
        temp1 = re.search(r"info 1/1\s+uptime", msg)
        temp2 = re.search(r"info 1/2\s+uptime", msg)

        clock = re.search(r'\".+\"', self.command("show clock"))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        card1_serial = 0
        card2_serial = 0
        msg = self.command("show card").split('\r\n')
        fenge = []
        for i in range(len(msg)):
            if "---------------" in msg[i]:
                fenge.append(i)

        for i in range(len(fenge)):
            if "Unequipped" not in msg[fenge[i]+1]:
                card_flag = msg[fenge[i]+1].split()[0]

                if "SERIAL" in msg[fenge[i]-1]:
                    index_begin = msg[fenge[i]-1].find("SERIAL")
                else:
                    index_begin = msg[fenge[i] - 1].find("NO")

                if "SOFTWARE" in msg[fenge[i]-1]:
                    index_end = msg[fenge[i] - 1].find("SOFTWARE")
                else:
                    index_end = msg[fenge[i] - 1].find("VERSION")

                if card_flag == '1/1':
                    card1_serial = msg[fenge[i]+1][index_begin:index_end].strip()
                else:
                    card2_serial = msg[fenge[i]+1][index_begin:index_end].strip()




        if ISROOT:
            self.debugLogin()


        card1_reboot_times = 0
        card1_reboot_info = 0
        card2_reboot_times = 0
        card2_reboot_info = 0
        if temp1 != None and temp2 != None:
            """there are two cards"""
            msg = self.command("cat /FLASH/persist/logs/rebootCause.log")
            msg = msg.split("\n")[-2].split()
            # login to another card
            sign = self.command("sshMate")
            msg_ = self.command("cat /FLASH/persist/logs/rebootCause.log")

            msg_ = msg_.split("\n")
            index = -2
            while True:
                if '#' in msg_[index]:
                    msg_ = msg_[index].split(' # ')
                    break
                index -= 1
            # check the default login card, sometimes run cli "sshMate" is card1 to card2, and sometimes is card2 to card1
            if re.search("I'm card 1", sign) != None:

                card1_reboot_times = msg[0]
                card1_reboot_info = msg[2].strip()
                card2_reboot_times = msg_[0]
                card2_reboot_info = msg_[2].strip()
            else:
                card1_reboot_times = msg_[0]
                card1_reboot_info = msg_[2].strip()
                card2_reboot_times = msg[0]
                card2_reboot_info = msg[2].strip()
            self.command("exit")

        else:
            """there is just one card"""
            msg = self.command("cat /FLASH/persist/logs/rebootCause.log")
            msg = msg.split("\n")[-2].split()
            if temp1 != None:
                # only card1
                card1_reboot_times = msg[0]
                card1_reboot_info = msg[4]
            else:
                # only card2
                card2_reboot_times = msg[0]
                card2_reboot_info = msg[4]

        return [uptime_match.group(1)], [card1_reboot_times, card1_reboot_info, card1_serial], [card2_reboot_times,
                                                                                  card2_reboot_info, card2_serial], clock

    def disk_space(self):
        if ISROOT:
            self.command("exit")
        self.command("pag false")
        clock = re.search(r'\".+\"', self.command("show clock"))
        assert clock is not None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]
        if ISROOT:
            self.debugLogin()

        str1 = self.command("df -h")
        tempstr = re.search(r'/dev/mmcblk0p2\s+\d+[.]?\d+[MG]\s+\d+[.]?\d+[MG]\s+\d+[.]?\d+[MG]\s+\d+%', str1)
        usage = 0
        if tempstr:
            usage = int(str(tempstr.group()).split()[-1][:-1])
        return float(usage), clock

    # general cli
    def core_file(self, ):
        """check core file
        action :still need find all for two cards"""
        core_match = 0

        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        command_line = """show file contents core"""
        output = self.command(command_line)
        patt = r"number-of-files\s+(\d)"
        core_file_pattern = re.compile(patt)
        core_file_match = core_file_pattern.findall(output)
        for core1 in core_file_match:
            core_match += int(core1)

        return [core_match], clock

    def crash_process(self, ):
        """check OLT uptime
        name application-restart
        primary-element aemgrd
        dcli arcmgrd dump summary
        df -k"""
        restart = 'application-restart'
        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]
        command_line = "show event log start-value 0 end-value 200"
        output = self.command(command_line,t=5)

        if restart in output:
            crash_process_pattern = re.compile("primary-element\s+(\w+)")
            crash_process_match = re.search(crash_process_pattern, output)
            if crash_process_match:
                return [crash_process_match.group(1)], clock
            else:
                pass
        else:
            pass
            return False, clock

    def real_rate_check(self, ):
        """check active alarm"""
        fixed_rate = 'fixed-rate'
        assured_rate = 'assured-rate'
        excess_rate = 'excess-rate'

        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock is not None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]

        # scan for all pon port
        scan = self.command("show run inter pon")
        pattern = re.compile("interface pon \S+")

        pons = ReFind(scan, pattern)
        if pons is not None:
            pons = pons.split(",")
        else:
            return {}, clock

        command_line = []
        for i in range(len(pons)):
            command_line.append("show " + pons[i] + " utilization")

        fixed_rate_value = []
        assured_rate_value = []
        excess_rate_value = []
        for command in command_line:
            output = self.command(command)
            if fixed_rate in output or assured_rate in output or excess_rate in output:
                for line in output.splitlines():
                    if fixed_rate in line:
                        alarm_pattern = re.compile("fixed-rate\s+(\d+.\d+)")
                        alarm_match = re.search(alarm_pattern, line)
                        if alarm_match:
                            fixed_rate_value.append(float(alarm_match.group(1)))
                    elif assured_rate in line:
                        alarm_pattern = re.compile("assured-rate\s+(\d+.\d+)")
                        alarm_match = re.search(alarm_pattern, line)
                        if alarm_match:
                            assured_rate_value.append(float(alarm_match.group(1)))
                    elif excess_rate in line:
                        alarm_pattern = re.compile("excess-rate\s+(\d+.\d+)")
                        alarm_match = re.search(alarm_pattern, line)
                        if alarm_match:
                            excess_rate_value.append(float(alarm_match.group(1)))
                    else:
                        pass
            else:
                if self.debug:
                    pass
                assured_rate_value.append(0.0)
                fixed_rate_value.append(0.0)
                excess_rate_value.append(0.0)

        # dict{  'pon name':[fixed_rate_value, assured_rate_value, excess_rate_value]  }
        pon_value_dict = {}
        for i in range(len(pons)):
            pon_value_dict[pons[i]] = [fixed_rate_value[i], assured_rate_value[i], excess_rate_value[i]]
        self.command('\n')

        return pon_value_dict, clock

    def ont_online(self):
        ont_num = str(
            re.search(r'\w+\-\w+\s+\w+\-\w+\s+\d+', self.command("show discovered-ont ont-count", t=5)).group().split()[
                -1])
        aeont_num = str(re.search(r'\w+\-\w+\-\w+\s+\w+\-\w+\s+\d+',
                                  self.command("show discovered-ae-ont ont-count", t=5)).group().split()[-1])

        ont_res = []
        aeont_res = []
        if ont_num != '0':
            ont_info = self.command("show discovered-ont", t=5).split("\n")
            ont_vendor = []
            ont_serial_number = []
            ont_model = []
            ont_current_version = []
            index = 0
            for i in range(len(ont_info)):
                if "---------------------------" in ont_info[i]:
                    index = i
                    break
            pattern = "\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+"
            for i in range(index + 1, len(ont_info)):
                if re.search(pattern, ont_info[i]) is not None:
                    temp = ont_info[i].split()
                    ont_vendor.append(temp[0])
                    ont_serial_number.append(temp[1])
                    ont_model.append(temp[7])
                    ont_current_version.append(temp[8])
            ont_res = [ont_vendor, ont_serial_number, ont_model, ont_current_version]

        if aeont_num != '0':
            aeont_info = self.command("show discovered-ae-ont").split("\n")
            aeont_vendor = []
            aeont_serial_number = []
            aeont_model = []
            aeont_current_version = []
            index = 0
            for i in range(len(aeont_info)):
                if "---------------------------" in aeont_info[i]:
                    index = i
                    break
            pattern = "\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+"
            for i in range(index + 1, len(aeont_info)):
                if re.search(pattern, aeont_info[i]) is not None:
                    temp = aeont_info[i].split()
                    aeont_vendor.append(temp[0])
                    aeont_serial_number.append(temp[1])
                    aeont_model.append(temp[7])
                    aeont_current_version.append(temp[8])
            aeont_res = [aeont_vendor, aeont_serial_number, aeont_model, aeont_current_version]

        return ont_res, aeont_res

    def temperature(self):
        self.command('pag false')
        str1 = self.command('show sensors')
        card1 = re.search(r'sensors 1/1[\s\n\r\D\d]+sensors 1/2', str1).group()
        card2 = re.search(r'sensors 1/2[\s\n\r\D\d]*', str1).group()

        card1 = re.search(r'temperature[\s\n\r\D\d]+VOLTAGE-SENSOR', card1)
        card2 = re.search(r'temperature[\s\n\r\D\d]+VOLTAGE-SENSOR', card2)
        card1_sensor_name = []
        card1_temperature = []
        card2_sensor_name = []
        card2_temperature = []
        if card1 != None:
            card1 = card1.group().split('\n')
            for index in range(3, len(card1) - 2):
                temp1 = card1[index].split()
                card1_sensor_name.append(temp1[0])
                card1_temperature.append(float(temp1[1]))
        if card2 != None:
            card2 = card2.group().split('\n')
            for index in range(3, len(card2) - 2):
                temp2 = card2[index].split()
                card2_sensor_name.append(temp2[0])
                card2_temperature.append(float(temp2[1]))
        clock = re.search(r'\".+\"', self.command("show clock"))
        assert clock != None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20]
        return [card1_sensor_name, card1_temperature], [card2_sensor_name, card2_temperature], clock

    def module_information(self):
        # temp
        self.command("pag false")

        # scan all
        command_line = "show interface pon displaylevel 1"
        output = self.command(command_line)
        interface_pon = output.split('\r\n')[1:-1]

        command_line = "show interface ethernet displaylevel 1"
        output = self.command(command_line)
        interface_ethernet = output.split('\r\n')[1:-1]

        # fix commmand_line
        pon_command = []
        ethernet_command = []
        pon_name = []
        pon_module_manufacture_name = []
        pon_module_manufacture_part_number = []
        pon_module_vendor_name = []
        pon_module_vendor_part_number = []

        ethernet_name = []
        ethernet_module_manufacture_name = []
        ethernet_module_manufacture_part_number = []
        ethernet_module_vendor_name = []
        ethernet_module_vendor_part_number = []

        pattern1 = "manufacturer-name.+"
        pattern2 = "manufacturer-part-number.+"
        pattern3 = "vendor-name.+"
        pattern4 = "vendor-part-number.+"

        pon_res = []
        ethernet_res = []

        if '% No entries found.' not in interface_pon:
            for item in interface_pon:
                pon_command.append("show " + item + " module")
                # regular match
            # match pon port and module
            for i in range(len(pon_command)):
                output = self.command(pon_command[i])
                res1 = re.search(pattern1, output)
                res2 = re.search(pattern2, output)
                res3 = re.search(pattern3, output)
                res4 = re.search(pattern4, output)
                if res1 is not None:
                    res1 = res1.group().split()
                    res2 = res2.group().split()
                    res3 = res3.group().split()
                    res4 = res4.group().split()
                    pon_name.append(interface_pon[i])
                    pon_module_manufacture_name.append(' '.join(res1[1:]).replace("\"", ""))
                    pon_module_manufacture_part_number.append(' '.join(res2[1:]).replace("\"", ""))
                    pon_module_vendor_name.append(' '.join(res3[1:]).replace("\"", ""))
                    pon_module_vendor_part_number.append(' '.join(res4[1:]).replace("\"", ""))
            pon_res = [pon_name, pon_module_manufacture_name, pon_module_manufacture_part_number,
                       pon_module_vendor_name, pon_module_vendor_part_number]

        if '% No entries found.' not in interface_ethernet:
            for item in interface_ethernet:
                ethernet_command.append("show " + item + " module")
            # match ethernet port and module
            for i in range(len(ethernet_command)):
                output = self.command(ethernet_command[i])
                res1 = re.search(pattern1, output)
                res2 = re.search(pattern2, output)
                res3 = re.search(pattern3, output)
                res4 = re.search(pattern4, output)
                if res1 is not None:
                    res1 = res1.group().split()
                    res2 = res2.group().split()
                    res3 = res3.group().split()
                    res4 = res4.group().split()
                    ethernet_name.append(interface_ethernet[i])
                    ethernet_module_manufacture_name.append(' '.join(res1[1:]).replace("\"", ""))
                    ethernet_module_manufacture_part_number.append(' '.join(res2[1:]).replace("\"", ""))
                    ethernet_module_vendor_name.append(' '.join(res3[1:]).replace("\"", ""))
                    ethernet_module_vendor_part_number.append(' '.join(res4[1:]).replace("\"", ""))
            ethernet_res = [ethernet_name, ethernet_module_manufacture_name, ethernet_module_manufacture_part_number,
                            ethernet_module_vendor_name, ethernet_module_vendor_part_number]

        return pon_res, ethernet_res

    def model_information(self):
        output = self.command('show card').split('\r\n')
        model1 = ''
        model2 = ''
        SN1 = ''
        SN2 = ''
        index_begin = 0
        index_end = 0
        for line in output:
            if 'SERIAL NO' in line:
                index_begin = line.find("MODEL")
                index_end = line.find("SERIAL")
                continue
            if '1/1' in line:
                if 'card 1/1' in line:
                    pass
                elif 'unequipped' not in line and 'Unequipped' not in line:
                    model1 = line[index_begin:index_end].strip()
                    SN1 = line[index_end:].split()[0]
            elif '1/2' in line:
                if 'card 1/2' in line:
                    pass
                elif 'unequipped' not in line and 'Unequipped' not in line:
                    model2 = line[index_begin:index_end].strip()
                    SN2 = line[index_end:].split()[0]

        version1 = ''
        version2 = ''
        output = self.command('show version').split('\r\n')
        flag = 0
        for line in output:
            if '1/2' in line:
                flag = 1
            if 'details' in line:
                if flag == 0:
                    version1 = line.split()[1]
                else:
                    version2 = line.split()[1]

        return model1, model2, version1, version2, SN1, SN2

    def save_startup_config(self):
        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock is not None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20].replace(' ','_').replace(':','.')
        path = f'{self.root_dir}/{self.ip}'
        if not os.path.exists(f'{self.root_dir}/{self.ip}'):
            os.makedirs(path)
        self.command('pag false')

        output = self.command("show version")
        version = re.search("details\s+\S+",output).group().split()[1]

        path = f"{self.root_dir}/{self.ip}/startup_config/{version}_{clock}"
        if not os.path.exists(path):
            os.makedirs(path)
        self.command(
            f"upload file config from-file startup-config.xml to-URI ftp://{self.ftp_user}:{self.ftp_pwd}@{self.ftp_host}:{self.ftp_port}/{self.ip}/startup_config/{version}_{clock}/")
        time.sleep(10)

    def ftp_debug_save_corefile(self, path, file1, file2):
        clock = re.search(r'\".+\"', str(self.command("show clock")))
        assert clock is not None, "Match 'clock' failed, ip={}".format(self.ip)
        clock = clock.group()[1:20].replace(' ','_').replace(':','.')

        self.debugLogin()
        id = int(self.command("/usr/bin/scripts/xml2txt.sh /nvpd/product/platform/chassis/slot_id").split('\r\r\n')[1])
        flag = 2
        while flag:
            if id == 1:
                if len(file1) != 0:
                    if not os.path.exists(f"{self.root_dir}/{path}/card1/"):
                        os.makedirs(f"{self.root_dir}/{path}/card1/")

                    self.command("cd /FLASH/persist/core/")
                    for i in range(len(file1)):
                        self.command(
                            f"ftpput -u {self.ftp_user} -p {self.ftp_pwd} {self.ftp_host}:{self.ftp_port} {path}/card1/{file1[i]} {file1[i]}")
                        time.sleep(10)
            else:
                if len(file2) != 0:
                    if not os.path.exists(f"{self.root_dir}/{path}/card2/"):
                        os.makedirs(f"{self.root_dir}/{path}/card2/")

                    self.command("cd /FLASH/persist/core/")
                    for i in range(len(file2)):
                        self.command(
                            f"ftpput -u {self.ftp_user} -p {self.ftp_pwd} {self.ftp_host}:{self.ftp_port} {path}/card2/{file2[i]} {file2[i]}")
                        time.sleep(10)
            if len(file1) == 0 or len(file2) == 0:
                self.command("exit")
                return

            if flag == 2:
                self.command("sshMate")
                id = 1 if id == 2 else 2
                flag -= 1
            else:
                self.command("exit")
                self.command("exit")
                return

    def read_core_file(self):
        output = self.command("show file contents core")
        output = output.split('1/2')
        file1 = []
        file2 = []
        # card1 exists
        if 'number-of-files' in output[0]:
            temp = re.search('number-of-files \d+', output[0])
            if temp is not None:
                temp = int(temp.group().split()[1])
                if temp != 0:
                    pattern = re.compile('core.+\.\S+')
                    file_name = ReFind(output[0], pattern)
                    if file_name is not None:
                        file1 = file_name.split(',')
        # card2 exists
        if 'number-of-files' in output[1]:
            temp = re.search('number-of-files \d+', output[1])
            if temp is not None:
                temp = int(temp.group().split()[1])
                if temp != 0:
                    pattern = re.compile('core.+\.\S+')
                    file_name = ReFind(output[1], pattern)
                    if file_name is not None:
                        file2 = file_name.split(',')
        return file1, file2

    def save_techlog(self):
        path = f"{self.root_dir}/{self.ip}/techlog"
        if not os.path.exists(path):
            os.makedirs(path)
        self.command("generate techlog")
        timer = 10
        flag = True
        while flag and timer:
            timer -= 1
            time.sleep(120)
            self.command('\n')
            output = self.command('show techlog status')
            if 'Success' in output:
                output1 = output.split('\r\n')[-3].split()[0]
                while True:
                    time.sleep(10)
                    output2 = self.command(
                        f"upload file techlog from-file {output1} to-URI ftp://{self.ftp_user}:{self.ftp_pwd}@{self.ftp_host}:{self.ftp_port}/{self.ip}/techlog/")
                    if 'Initiating upload' in output2:
                        flag = False
                        break
        pass
