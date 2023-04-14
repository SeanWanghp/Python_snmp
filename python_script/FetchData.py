import re
import time

from Service import Service
import yaml
from Setting import ISROOT, INIT_REBOOT_TIME

class FetchData(Service):
    def __init__(self, ip, port, system_name, owner_name, username, password):
        super(FetchData, self).__init__(ip, port, system_name, owner_name, username, password)


    # root permisson cli
    def root_cli(self, server, initial, INTERVAL):
        # get the initial data
        if initial and INIT_REBOOT_TIME:
            self.initial_uptime()
        sql = f"select * from up_time where IP=\'{self.ip}\'"
        Info = self.conn.select(sql)
        if len(Info) == 0:
            self.initial_uptime()
            sql = "select * from up_time where IP='{}'".format(self.ip)
            Info = self.conn.select(sql)[0]
        else:
            Info = Info[0]
        last_uptime = Info['UPTIME']
        card1_begin = Info['CARD1_REBOOT_TIMES_BEGIN']
        card2_begin = Info['CARD2_REBOOT_TIMES_BEGIN']
        sys_reboot, card1_reboot, card2_reboot, last_uptime = self.read_uptime(last_uptime, card1_begin, card2_begin,
                                                                               INTERVAL)

        server.reboot_times.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(sys_reboot)
        server.reboot_times.labels(IP=self.ip, card='card1', system_name=self.system_name, owner_name=self.owner_name).set(card1_reboot)
        server.reboot_times.labels(IP=self.ip, card='card2', system_name=self.system_name, owner_name=self.owner_name).set(card2_reboot)

        disk = self.disk_space_check()
        server.disk_usage.labels(IP=self.ip, mode='disk_usage', system_name=self.system_name, owner_name=self.owner_name).set(disk)

        sql = "select * from mem_check where id=(select MAX(id) from mem_check where IP='{}' and name='{}')".format(
            self.ip, "lmd")
        temp = self.conn.select(sql)
        sql = "select * from mem_check where id=(select MAX(id) from mem_check where IP='{}' and name='{}')".format(
            self.ip, "ponmgrd")
        temp1 = self.conn.select(sql)
        if len(temp) == 0:
            lmd_begin = 0
        else:
            lmd_begin = temp[0]['MEM']
        if len(temp1) == 0:
            ponmgrd_begin = 0
        else:
            ponmgrd_begin = temp1[0]['MEM']
        lmd, ponmgrd = self.mem_check(lmd_begin, ponmgrd_begin)
        server.main_process_mem.labels(IP=self.ip, mode='lmd', system_name=self.system_name, owner_name=self.owner_name).set(lmd)
        server.main_process_mem.labels(IP=self.ip, mode='ponmgrd', system_name=self.system_name, owner_name=self.owner_name).set(ponmgrd)

        self.mem_top()



    # general permisson cli
    def general_cli(self, server):
        if ISROOT == True:
            self.command('exit')
        self.command("pag false")

        # table data
        self.model_info()
        self.ont_online_info()
        self.module_info()


        cpu_value = self.read_cpu() / 100
        server.cpu_usage.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(cpu_value)
        cpu_value_card1 = self.read_cpu_card('1/1') / 100
        server.cpu_usage.labels(IP=self.ip, card='card1', system_name=self.system_name, owner_name=self.owner_name).set(cpu_value_card1)
        cpu_value_card2 = self.read_cpu_card('1/2') / 100
        server.cpu_usage.labels(IP=self.ip, card='card2', system_name=self.system_name, owner_name=self.owner_name).set(cpu_value_card2)
        mem_value = self.read_mem() / 100
        server.mem_usage.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(mem_value)
        mem_value_card1 = self.read_mem_card('1/1') / 100
        server.mem_usage.labels(IP=self.ip, card='card1', system_name=self.system_name, owner_name=self.owner_name).set(mem_value_card1)
        mem_value_card2 = self.read_mem_card('1/2') / 100
        server.mem_usage.labels(IP=self.ip, card='card2', system_name=self.system_name, owner_name=self.owner_name).set(mem_value_card2)
        core_file_value, newCoreFileFlag = self.read_corefile()
        server.core_file_times.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(core_file_value)
        server.new_core_file_flag.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(newCoreFileFlag)
        crash_value = self.read_crash()
        server.crash_process.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(crash_value)
        critical_value, major_value, minor_value, info_value = self.alarm_act()
        server.alarm_active.labels(IP=self.ip, mode='alarm_critical', system_name=self.system_name, owner_name=self.owner_name).set(critical_value)
        server.alarm_active.labels(IP=self.ip, mode='alarm_major', system_name=self.system_name, owner_name=self.owner_name).set(major_value)
        server.alarm_active.labels(IP=self.ip, mode='alarm_minor', system_name=self.system_name, owner_name=self.owner_name).set(minor_value)
        server.alarm_active.labels(IP=self.ip, mode='alarm_info', system_name=self.system_name, owner_name=self.owner_name).set(info_value)
        ont_missing, ont_departure = self.ont_action_check()
        server.ont_active.labels(IP=self.ip, mode='ont_missing', system_name=self.system_name, owner_name=self.owner_name).set(ont_missing)
        server.ont_active.labels(IP=self.ip, mode='ont_departure', system_name=self.system_name, owner_name=self.owner_name).set(ont_departure)
        pon_rate = self.port_rate_check()
        for key in pon_rate.keys():
            server.port_rate.labels(IP=self.ip, port_name=key, rate_type='fixed_rate', system_name=self.system_name, owner_name=self.owner_name).set(pon_rate[key][0])
            server.port_rate.labels(IP=self.ip, port_name=key, rate_type='assured_rate', system_name=self.system_name, owner_name=self.owner_name).set(pon_rate[key][1])
            server.port_rate.labels(IP=self.ip, port_name=key, rate_type='excess_rate', system_name=self.system_name, owner_name=self.owner_name).set(pon_rate[key][2])

        # sensor temperature begin
        card1, card2 = self.sensors_temperature()
        if len(card1) > 0:
            for i in range(0, len(card1[0])):
                server.sensors_temp.labels(IP=self.ip, card='card1', sensor=card1[0][i], system_name=self.system_name, owner_name=self.owner_name).set(card1[1][i])
        if len(card2) > 0:
            for i in range(0, len(card2[0])):
                server.sensors_temp.labels(IP=self.ip, card='card2', sensor=card2[0][i], system_name=self.system_name, owner_name=self.owner_name).set(card2[1][i])
        # sensor temperature end


    def vm_cli(self, server):
        cpu_vm = self.vm_cpu()
        server.vm_cpu_usage.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(cpu_vm)
        mem_vm = self.vm_mem()
        server.vm_mem_usage.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(mem_vm)
        disk_vm = self.vm_disk()
        server.vm_disk_usage.labels(IP=self.ip, card='system', system_name=self.system_name, owner_name=self.owner_name).set(disk_vm)