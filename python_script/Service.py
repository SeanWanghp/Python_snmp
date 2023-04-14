import re
import time
import datetime
import os
import yaml
from VMMethod import VMMethod
from AxosMethod import CPU, Memory, Alarm, Other
from Dao import MysqlDb
from Setting import ftp_info

root_dir = ftp_info['root_dir']


class Service(CPU, Memory, Alarm, Other, VMMethod):
    """https://www.jianshu.com/p/a64ad351ebb2
    https://blog.csdn.net/specter11235/article/details/89198032"""

    def __init__(self, ip, port,system_name, owner_name, username, password):
        super(Service, self).__init__()
        self.ip = ip
        self.port = port
        self.owner_name = owner_name
        self.system_name = system_name
        self.username = username
        self.password = password

        self.conn = MysqlDb()


    def initial_uptime(self):
        # clean up_time table
        sql = f"delete from up_time where IP='{self.ip}';"
        self.conn.execute_db(sql)
        free, card1, card2, clock = self.uptime()


        # Assign the initial value of system startup time which is the time of monitor_script startup
        # to facilitate the subsequent calculation of system restart times
        self.updateUpTime(SECONDS=int(free[0]), IP=self.ip, REBOOT=0, TIME=clock,
                              CARD1_REBOOT_TIMES_BEGIN=card1[0], CARD1_REBOOT_INFO=0,
                              CARD2_REBOOT_TIMES_BEGIN=card2[0], CARD2_REBOOT_INFO=0, CARD1_REBOOT_TIMES=0,
                              CARD2_REBOOT_TIMES=0,CARD1_SERIAL=card1[2],CARD2_SERIAL=card2[2],CARD1_SERIAL_PRE=card1[2],CARD2_SERIAL_PRE=card2[2],CARD1_REBOOT_TIMES_PRE=0,CARD2_REBOOT_TIMES_PRE=0)

    def read_uptime(self, last_uptime, card1_reboot_times_begin, card2_reboot_times_begin, INTERVAL):
        # uptime
        free, card1, card2, clock = self.uptime()


        seconds = free[0]
        # system and card reboot times

        card1_reboot = int(card1[0]) - int(card1_reboot_times_begin)
        card2_reboot = int(card2[0]) - int(card2_reboot_times_begin)
        sql = "select * from up_time where IP='{}'".format(self.ip)
        Info = self.conn.select(sql)[0]
        reboot_times = int(Info['REBOOT_TIMES'])

        card1_serial = Info['CARD1_SERIAL']
        card2_serial = Info['CARD2_SERIAL']
        card1_serial_pre = Info['CARD1_SERIAL_PRE']
        card2_serial_pre = Info['CARD2_SERIAL_PRE']
        card1_reboot_times_pre = Info['CARD1_REBOOT_TIMES_PRE']
        card2_reboot_times_pre = Info['CARD2_REBOOT_TIMES_PRE']

        # the system reboot
        if (int(seconds) < int(last_uptime) and int(seconds) < INTERVAL):
            reboot_times += 1
            #   when system reboot, the two cards don't start at the same time, so if don't check one more time,
            # the reboot times number will be so big, because the CARD_REBOOT_TIMES_BEGIN has become zero and
            # the "card_reboot = card - card_reboot_times_begin"
            time.sleep(10)
            free, card1, card2, clock = self.uptime()
            seconds = free[0]
            card1_reboot_times_begin = card1[0]
            card2_reboot_times_begin = card2[0]

            card1_reboot = 0
            card2_reboot = 0

            # update database
            self.updateUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                  CARD1_REBOOT_TIMES=card1_reboot,
                                  CARD1_REBOOT_INFO=card2_reboot,
                                  CARD2_REBOOT_TIMES=0,
                                  CARD2_REBOOT_INFO=0,
                                  CARD1_REBOOT_TIMES_BEGIN=card1_reboot_times_begin,
                                  CARD2_REBOOT_TIMES_BEGIN=card2_reboot_times_begin,
                                  CARD1_SERIAL=card1[2],
                                  CARD2_SERIAL=card2[2],
                                  CARD1_SERIAL_PRE=card1[2],
                                  CARD2_SERIAL_PRE=card2[2],
                                  CARD1_REBOOT_TIMES_PRE=0,
                                  CARD2_REBOOT_TIMES_PRE=0
                                  )
            return reboot_times, card1_reboot, card2_reboot, int(seconds)

        # the card reboot
        # two cards exist
        elif int(card1[0]) != 0 and int(card2[0]) != 0:
            # the system don't reboot but cards do while
            if (int(card1[0]) != int(card1_reboot_times_begin) or int(card2[0]) != int(card2_reboot_times_begin)) or str(card1_serial) != str(card1[2]) or str(card2_serial) != str(card2[2]):
                # card serial number do not change
                if str(card1_serial) == str(card1[2]) and str(card2_serial) == str(card2[2]):
                    self.updateUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                          CARD1_REBOOT_TIMES=card1_reboot,
                                          CARD1_REBOOT_INFO=card1[1],
                                          CARD2_REBOOT_TIMES=card2_reboot,
                                          CARD2_REBOOT_INFO=card2[1],
                                          CARD1_REBOOT_TIMES_BEGIN=card1_reboot_times_begin,
                                          CARD2_REBOOT_TIMES_BEGIN=card2_reboot_times_begin,
                                          CARD1_SERIAL=card1[2],
                                          CARD2_SERIAL=card2[2],
                                          CARD1_SERIAL_PRE=card1_serial,
                                          CARD2_SERIAL_PRE=card2_serial,
                                          CARD1_REBOOT_TIMES_PRE=card1_reboot,
                                          CARD2_REBOOT_TIMES_PRE=card2_reboot)
                    return reboot_times, card1_reboot, card2_reboot, int(seconds)
                # card serial number change
                else:
                    card1_change_info = card1[1]
                    card2_change_info = card2[1]
                    card1_reboot = card1_reboot_times_pre
                    card2_reboot = card2_reboot_times_pre
                    # latest time's serial is not zero
                    if int(card1_serial) != 0 and int(card2_serial) != 0:
                        if card1_serial != card1[2]:
                            card1_change_info = 'card change'
                            card1_reboot += 1
                        if card2_serial != card2[2]:
                            card2_change_info = 'card change'
                            card2_reboot += 1

                        self.updateUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                              CARD1_REBOOT_TIMES=card1_reboot,
                                              CARD1_REBOOT_INFO=card1_change_info,
                                              CARD2_REBOOT_TIMES=card2_reboot,
                                              CARD2_REBOOT_INFO=card2_change_info,
                                              CARD1_REBOOT_TIMES_BEGIN=int(card1[0])-int(card1_reboot),
                                              CARD2_REBOOT_TIMES_BEGIN=int(card2[0])-int(card2_reboot),
                                              CARD1_SERIAL=card1[2],
                                              CARD2_SERIAL=card2[2],
                                              CARD1_SERIAL_PRE=card1[2],
                                              CARD2_SERIAL_PRE=card2[2],
                                              CARD1_REBOOT_TIMES_PRE=card1_reboot,
                                              CARD2_REBOOT_TIMES_PRE=card2_reboot
                                              )
                        return reboot_times, card1_reboot, card2_reboot, int(seconds)
                    # latest time's serial is zero
                    else:
                        card1_reboot_times_begin1 = card1_reboot_times_begin
                        card2_reboot_times_begin1 = card2_reboot_times_begin
                        card1_change_info = card1[1]
                        card2_change_info = card2[1]
                        if int(card1_serial) == 0 and str(card1[2]) != card1_serial_pre:
                            card1_reboot_times_begin1 = int(card1[0]) - card1_reboot_times_pre - 1
                            card1_change_info = 'card change'
                        if int(card2_serial) == 0 and str(card2[2]) != card2_serial_pre:
                            card2_reboot_times_begin1 = int(card2[0]) - card2_reboot_times_pre - 1
                            card2_change_info = 'card change'

                        card1_reboot = int(card1[0])-card1_reboot_times_begin1
                        card2_reboot = int(card2[0])-card2_reboot_times_begin1
                        self.updateUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                              CARD1_REBOOT_TIMES=card1_reboot,
                                              CARD1_REBOOT_INFO=card1_change_info,
                                              CARD2_REBOOT_TIMES=card2_reboot,
                                              CARD2_REBOOT_INFO=card2_change_info,
                                              CARD1_REBOOT_TIMES_BEGIN=card1_reboot_times_begin1,
                                              CARD2_REBOOT_TIMES_BEGIN=card2_reboot_times_begin1,
                                              CARD1_SERIAL=card1[2],
                                              CARD2_SERIAL=card2[2],
                                              CARD1_SERIAL_PRE=card1[2],
                                              CARD2_SERIAL_PRE=card2[2],
                                              CARD1_REBOOT_TIMES_PRE=int(card1[0])-card1_reboot_times_begin1,
                                              CARD2_REBOOT_TIMES_PRE=int(card2[0])-card2_reboot_times_begin1
                                              )
                        return reboot_times, card1_reboot, card2_reboot, int(seconds)

        # one card or two cards don't exist
        else:
            if card1[0] == 0 and card2[0] == 0:
                card1_reboot = -1
                card2_reboot = -1
                self.updateUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                      CARD1_REBOOT_TIMES=card1_reboot,
                                      CARD1_REBOOT_INFO='no card',
                                      CARD2_REBOOT_TIMES=card2_reboot,
                                      CARD2_REBOOT_INFO='no card',
                                      CARD1_REBOOT_TIMES_BEGIN=card1_reboot_times_begin,
                                      CARD2_REBOOT_TIMES_BEGIN=card2_reboot_times_begin,
                                      CARD1_SERIAL=card1[2],
                                      CARD2_SERIAL=card2[2],
                                      CARD1_SERIAL_PRE=card1_serial_pre,
                                      CARD2_SERIAL_PRE=card2_serial_pre,
                                      CARD1_REBOOT_TIMES_PRE=card1_reboot_times_pre,
                                      CARD2_REBOOT_TIMES_PRE=card2_reboot_times_pre
                                      )
                return reboot_times, card1_reboot, card2_reboot, int(seconds)
            elif card1[0] == 0 and card2[0] != 0:
                card1_reboot = -1
                self.updateUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                      CARD1_REBOOT_TIMES=card1_reboot,
                                      CARD1_REBOOT_INFO='no card',
                                      CARD2_REBOOT_TIMES=card2_reboot,
                                      CARD2_REBOOT_INFO=card2[1],
                                      CARD1_REBOOT_TIMES_BEGIN=card1_reboot_times_begin,
                                      CARD2_REBOOT_TIMES_BEGIN=card2_reboot_times_begin,
                                      CARD1_SERIAL=card1[2],
                                      CARD2_SERIAL=card2[2],
                                      CARD1_SERIAL_PRE=card1_serial_pre,
                                      CARD2_SERIAL_PRE=card2_serial,
                                      CARD1_REBOOT_TIMES_PRE=card1_reboot_times_pre,
                                      CARD2_REBOOT_TIMES_PRE=card2_reboot
                                      )
                return reboot_times, card1_reboot, card2_reboot, int(seconds)
            elif card1[0] != 0 and card2[0] == 0:
                card2_reboot = -1
                self.updateUpTime(SECONDS=int(seconds), IP=self.ip, REBOOT=reboot_times, TIME=clock,
                                      CARD1_REBOOT_TIMES=card1_reboot,
                                      CARD1_REBOOT_INFO=card1[1],
                                      CARD2_REBOOT_TIMES=card2_reboot,
                                      CARD2_REBOOT_INFO='no card',
                                      CARD1_REBOOT_TIMES_BEGIN=card1_reboot_times_begin,
                                      CARD2_REBOOT_TIMES_BEGIN=card2_reboot_times_begin,
                                      CARD1_SERIAL=card1[2],
                                      CARD2_SERIAL=card2[2],
                                      CARD1_SERIAL_PRE=card1_serial,
                                      CARD2_SERIAL_PRE=card2_serial_pre,
                                      CARD1_REBOOT_TIMES_PRE=card1_reboot,
                                      CARD2_REBOOT_TIMES_PRE=card2_reboot_times_pre
                                      )
                return reboot_times, card1_reboot, card2_reboot, int(seconds)

        return reboot_times, card1_reboot, card2_reboot, int(seconds)

    def updateUpTime(self, SECONDS, IP, REBOOT, TIME, CARD1_REBOOT_TIMES, CARD1_REBOOT_INFO, CARD2_REBOOT_TIMES,
                     CARD2_REBOOT_INFO, CARD1_REBOOT_TIMES_BEGIN, CARD2_REBOOT_TIMES_BEGIN, CARD1_SERIAL, CARD2_SERIAL,
                     CARD1_SERIAL_PRE, CARD2_SERIAL_PRE, CARD1_REBOOT_TIMES_PRE, CARD2_REBOOT_TIMES_PRE):

        sql = "select * from up_time where ip='{}'".format(IP)
        data = self.conn.select(sql)
        if len(data) == 0:
            sql = f"insert into up_time (UPTIME,IP,REBOOT_TIMES,TIME,CARD1_REBOOT_TIMES,CARD1_REBOOT_INFO,CARD2_REBOOT_TIMES,CARD2_REBOOT_INFO,CARD1_REBOOT_TIMES_BEGIN,CARD2_REBOOT_TIMES_BEGIN,CARD1_SERIAL,CARD2_SERIAL,CARD1_SERIAL_PRE,CARD2_SERIAL_PRE,CARD1_REBOOT_TIMES_PRE,CARD2_REBOOT_TIMES_PRE) value {SECONDS, IP, REBOOT, TIME, CARD1_REBOOT_TIMES, CARD1_REBOOT_INFO, CARD2_REBOOT_TIMES, CARD2_REBOOT_INFO, CARD1_REBOOT_TIMES_BEGIN, CARD2_REBOOT_TIMES_BEGIN, CARD1_SERIAL, CARD2_SERIAL, CARD1_SERIAL_PRE, CARD2_SERIAL_PRE, CARD1_REBOOT_TIMES_PRE, CARD2_REBOOT_TIMES_PRE};"
            self.conn.execute_db(sql)
        else:
            sql = "update up_time set UPTIME='{}',REBOOT_TIMES='{}',TIME='{}',CARD1_REBOOT_TIMES='{}',CARD1_REBOOT_INFO='{}',CARD2_REBOOT_TIMES='{}',CARD2_REBOOT_INFO='{}',CARD1_REBOOT_TIMES_BEGIN='{}',CARD2_REBOOT_TIMES_BEGIN='{}',CARD1_SERIAL='{}',CARD2_SERIAL='{}',CARD1_SERIAL_PRE='{}',CARD2_SERIAL_PRE='{}',CARD1_REBOOT_TIMES_PRE='{}',CARD2_REBOOT_TIMES_PRE='{}' where IP='{}'".format(
                SECONDS, REBOOT, TIME, CARD1_REBOOT_TIMES, CARD1_REBOOT_INFO, CARD2_REBOOT_TIMES, CARD2_REBOOT_INFO,
                CARD1_REBOOT_TIMES_BEGIN, CARD2_REBOOT_TIMES_BEGIN, CARD1_SERIAL, CARD2_SERIAL, CARD1_SERIAL_PRE,
                CARD2_SERIAL_PRE, CARD1_REBOOT_TIMES_PRE, CARD2_REBOOT_TIMES_PRE, IP)
            self.conn.execute_db(sql)

    def checkLastMem(self, card_id, ip):
        # select the latest data
        if card_id == '1/1':
            sql = f"select * from mem_use_card where id = (select MAX(id) from mem_use_card where CARD='1/1' and IP='{ip}')"
            info = self.conn.select(sql)
            if len(info) == 0:
                return 0
            return info[0]
        else:
            sql = f"select * from mem_use_card where id = (select MAX(id) from mem_use_card where CARD='1/2' and IP='{ip}')"
            info = self.conn.select(sql)
            if len(info) == 0:
                return 0
            return info[0]

    def disk_space_check(self):
        usage, clock = self.disk_space()
        sql = f"insert into disk_total_use (DISK,IP,TIME) value {usage, self.ip, clock};"
        self.conn.execute_db(sql)
        return usage

    # only use in mem_check
    def mem_check_judge(self, TIME, memory, name):
        if TIME == 0 and memory == 0:
            return
        sql = "select * from mem_check where id=(select MAX(id) from mem_check where IP='{}' and name='{}')".format(
            self.ip, name)
        preTIME = self.conn.select(sql)
        if len(preTIME) == 0:
            sql = f"insert into mem_check (NAME,IP,TIME,MEM) value {name, self.ip, TIME, memory};"
            self.conn.execute_db(sql)
        else:
            preTIME = preTIME[0]
            preTIME = preTIME['TIME']
            preTIME = preTIME.strftime("%Y-%m-%d %H:%M:%S")
            TIME1 = datetime.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
            preTIME = datetime.datetime.strptime(preTIME, "%Y-%m-%d %H:%M:%S")

            # convert to timestamp to compare
            TIME1 = time.mktime(TIME1.timetuple())
            preTIME = time.mktime(preTIME.timetuple())
            if preTIME < TIME1:
                sql = f"insert into mem_check (NAME,IP,TIME,MEM) value {name, self.ip, TIME, memory};"
                self.conn.execute_db(sql)
            else:
                return

    def mem_check(self, lmd_begin, ponmgrd_begin):
        TIME, lmd_memory = self.mem_check_log("lmd")
        self.mem_check_judge(TIME, lmd_memory, "lmd")
        TIME, pon_memory = self.mem_check_log("ponmgrd")
        self.mem_check_judge(TIME, pon_memory, "ponmgrd")

        return float(lmd_memory), float(pon_memory)
        # return (float(lmd_memory) - float(lmd_begin)), (float(pon_memory) - float(pon_begin))

    def mem_top(self):
        mem_top1, mem_top2, mem_top3 = self.mem_top_log()
        sql = f"delete from mem_increase_top where IP='{self.ip}';"
        self.conn.execute_db(sql)
        sql = f"insert into mem_increase_top (NAME,INCREASE,`RANK`,IP,SYSTEM_NAME) value {mem_top1[0],mem_top1[1],1,self.ip,self.system_name};"
        self.conn.execute_db(sql)
        sql = f"insert into mem_increase_top (NAME,INCREASE,`RANK`,IP,SYSTEM_NAME) value {mem_top2[0], mem_top2[1], 2, self.ip, self.system_name};"
        self.conn.execute_db(sql)
        sql = f"insert into mem_increase_top (NAME,INCREASE,`RANK`,IP,SYSTEM_NAME) value {mem_top3[0], mem_top3[1], 3, self.ip, self.system_name};"
        self.conn.execute_db(sql)

        return mem_top1, mem_top2, mem_top3

    def read_cpu(self):
        # total memory usage
        free, clock = self.cpu_cal()
        cpu_usage = free[0]
        sql = f"insert into cpu_total_use (CPU,IP,TIME) value {cpu_usage, self.ip, clock};"
        self.conn.execute_db(sql)
        return cpu_usage

    def read_cpu_card(self, number):
        # card cpu usage
        free, clock = self.cpu_cal_card(number, )
        cpu_usage_card = free[0]
        sql = f"insert into cpu_use_card (CPU,CARD,IP,TIME) value {cpu_usage_card, number, self.ip, clock};"
        self.conn.execute_db(sql)
        return cpu_usage_card

    def read_mem(self):
        # total memory usage
        free, clock = self.mem_cal()
        mem_usage = free[0]
        sql = f"insert into mem_total_use (MEM,IP,TIME) value {mem_usage, self.ip, clock};"
        self.conn.execute_db(sql)

        if float(mem_usage) > 85:
            sql = f"select * from mem_total_use where id = (select MAX(id) from mem_use_card where CARD='1/1' and IP='{self.ip}')"
            tmp = self.conn.select(sql)
            if len(tmp) == 0:
                self.check_techlog(clock)
            else:
                if tmp[0] < 85:
                    self.check_techlog(clock)

        return mem_usage

    def read_mem_card(self, number):
        # card memory usage
        free, clock = self.mem_cal_card(number, )
        mem_usage = free[0]
        if float(mem_usage) > 85:
            lastmem = self.checkLastMem(number, self.ip)
            if lastmem < 85:
                self.check_techlog(clock)
        sql = f"insert into mem_use_card (MEM,CARD,IP,TIME) value {mem_usage, number, self.ip, clock};"
        self.conn.execute_db(sql)
        return mem_usage

    def read_corefile(self):
        # corefile
        free, clock = self.core_file()
        corefile = free[0]
        sql = f"insert into core_file (CORE_FILE,IP,TIME) value {int(corefile), self.ip, clock};"
        self.conn.execute_db(sql)
        clock = clock.replace(' ','_').replace(':','.')
        newCoreFileFlag = 0

        if int(corefile) != 0:
            file1, file2 = self.read_core_file()
            corefile = len(file1) + len(file2) # update core file number, because there are debug files which is not what we want.
            sql = f"select * from core_file_last_detail where IP='{self.ip}'"
            readDB = self.conn.select(sql)
            # compare the core file name with that at last time to consider weather we should generate tech log
            # there is no core file, skip
            if corefile == 0:
                pass
            # there is no record before, which means it's a new ip
            elif len(readDB) == 0:
                sql = f"delete from core_file_last_detail where IP='{self.ip}';"
                self.conn.execute_db(sql)
                for f in file1:
                    tmp = '1/1'
                    sql = f"insert into core_file_last_detail (IP,CARD,FILE_NAME) value {self.ip, tmp, f};"
                    self.conn.execute_db(sql)
                for f in file2:
                    tmp = '1/2'
                    sql = f"insert into core_file_last_detail (IP,CARD,FILE_NAME) value {self.ip, tmp, f};"
                    self.conn.execute_db(sql)
                newCoreFileFlag = 1
                self.ftp_debug_save_corefile(f"{self.ip}/core_file/{clock}", file1, file2)
                self.check_techlog(clock)
            else:
                lastfile1 = []
                lastfile2 = []
                for item in readDB:
                    if item['CARD'] == '1/1':
                        lastfile1.append(item['FILE_NAME'])
                    else:
                        lastfile2.append(item['FILE_NAME'])
                if len(file1) > len(lastfile1) or len(file2) > len(lastfile2):
                    sql = f"delete from core_file_last_detail where IP='{self.ip}';"
                    self.conn.execute_db(sql)
                    for f in file1:
                        tmp = '1/1'
                        sql = f"insert into core_file_last_detail (IP,CARD,FILE_NAME) value {self.ip, tmp, f};"
                        self.conn.execute_db(sql)
                    for f in file2:
                        tmp = '1/2'
                        sql = f"insert into core_file_last_detail (IP,CARD,FILE_NAME) value {self.ip, tmp, f};"
                        self.conn.execute_db(sql)
                    newCoreFileFlag = 1
                    self.ftp_debug_save_corefile(f"{self.ip}/core_file/{clock}", file1, file2)
                    self.check_techlog(clock)
                else:
                    for item in file1:
                        if item not in lastfile1:
                            sql = f"delete from core_file_last_detail where IP='{self.ip}';"
                            self.conn.execute_db(sql)
                            for f in file1:
                                tmp = '1/1'
                                sql = f"insert into core_file_last_detail (IP,CARD,FILE_NAME) value {self.ip, tmp, f};"
                                self.conn.execute_db(sql)
                            for f in file2:
                                tmp = '1/2'
                                sql = f"insert into core_file_last_detail (IP,CARD,FILE_NAME) value {self.ip, tmp, f};"
                                self.conn.execute_db(sql)
                            self.ftp_debug_save_corefile(f"{self.ip}/core_file/{clock}", file1, file2)
                            self.check_techlog(clock)
                            return int(corefile), 1
                    for item in file2:
                        if item not in lastfile2:
                            sql = f"delete from core_file_last_detail where IP='{self.ip}';"
                            self.conn.execute_db(sql)
                            for f in file1:
                                tmp = '1/1'
                                sql = f"insert into core_file_last_detail (IP,CARD,FILE_NAME) value {self.ip, tmp, f};"
                                self.conn.execute_db(sql)
                            for f in file2:
                                tmp = '1/2'
                                sql = f"insert into core_file_last_detail (IP,CARD,FILE_NAME) value {self.ip, tmp, f};"
                                self.conn.execute_db(sql)
                            self.ftp_debug_save_corefile(f"{self.ip}/core_file/{clock}", file1, file2)
                            self.check_techlog(clock)
                            return int(corefile), 1

        return int(corefile), newCoreFileFlag

    def read_crash(self):
        # crash process
        free, clock = self.crash_process()
        if free:
            crash = free[0]
            if crash:
                sql = f"insert into crash (CRASH,IP,TIME) value {1, self.ip, clock};"
                self.conn.execute_db(sql)
                return 1
            else:
                sql = f"insert into crash (CRASH,IP,TIME) value {0, self.ip, clock};"
                self.conn.execute_db(sql)
                return 0
        else:
            sql = f"insert into crash (CRASH,IP,TIME) value {0, self.ip, clock};"
            self.conn.execute_db(sql)
            return 0

    def alarm_act(self):
        # active alarm
        COUNT, clock = self.active_alarm_check()
        sql = f"insert into alarm (CRITICAL,MAJOR,MINOR,INFO,IP,TIME) value {COUNT[0], COUNT[1], COUNT[2], COUNT[3], self.ip, clock}; "
        self.conn.execute_db(sql)
        return COUNT

    def ont_action_check(self):
        # ont alarm
        COUNT, clock = self.ont_alarm_check()
        sql = f"insert into ont_alarm (ONT_MISSING,ONT_DEPARTURE,IP,TIME) value {COUNT[0], COUNT[1], self.ip, clock};"
        self.conn.execute_db(sql)
        return COUNT

    def port_rate_check(self):
        # ont alarm
        rate, clock = self.real_rate_check()
        for key in rate.keys():
            sql = f"insert into port_rate (PORT_NAME,FIXED_RATE,ASSURED_RATE,EXCESS_RATE,IP,TIME) value {key, rate[key][0], rate[key][1], rate[key][2], self.ip, clock};"
            self.conn.execute_db(sql)
        return rate

    def ont_online_info(self):
        ont, aeont = self.ont_online()
        sql = f"delete from ont_online where IP='{self.ip}'"
        self.conn.execute_db(sql)
        if len(ont) != 0:
            for i in range(len(ont[0])):
                sql = f"insert into ont_online (IP, ONT_TYPE, VENDOR, SERIAL_NUMBER, MODEL, CURRENT_VERSION, SYSTEM_NAME, OWNER_NAME) value {self.ip, 'ont', ont[0][i], ont[1][i], ont[2][i], ont[3][i], self.system_name, self.owner_name};"
                self.conn.execute_db(sql)
        if len(aeont) != 0:
            for i in range(len(aeont[0])):
                sql = f"insert into ont_online (IP, ONT_TYPE, VENDOR, SERIAL_NUMBER, MODEL, CURRENT_VERSION, SYSTEM_NAME, OWNER_NAME) value {self.ip, 'ont', aeont[0][i], aeont[1][i], aeont[2][i], aeont[3][i], self.system_name, self.owner_name};"
                self.conn.execute_db(sql)
        # return number

    def module_info(self):
        pon, ethernet = self.module_information()
        # clean the db once in a loop
        sql = f"delete from module_information where IP='{self.ip}'"
        self.conn.execute_db(sql)
        # add new data into db
        if len(pon) != 0:
            for i in range(len(pon[0])):
                description = ''
                sql = f"select * from Optic_Module where `Calix Part # (red = new entry)` = '{pon[4][i]}'"
                temp = self.conn.select(sql)
                if len(temp) != 0:
                    description = temp[0]['Description']
                sql = f"insert into module_information (IP,INTERFACE_TYPE,INTERFACE_NAME,MANUFACTURE_NAME,MANUFACTURE_PART_NUMBER,VENDOR_NAME,VENDOR_PART_NUMBER,DESCRIPTION,SYSTEM_NAME,OWNER_NAME) value {self.ip, 'pon', pon[0][i], pon[1][i],pon[2][i], pon[3][i],pon[4][i],description, self.system_name, self.owner_name};"
                self.conn.execute_db(sql)
        if len(ethernet) != 0:
            for i in range(len(ethernet[0])):
                description = ''
                sql = f"select * from Optic_Module where `Calix Part # (red = new entry)` = '{ethernet[4][i]}'"
                temp = self.conn.select(sql)
                if len(temp) != 0:
                    description = temp[0]['Description']
                sql = f"insert into module_information (IP,INTERFACE_TYPE,INTERFACE_NAME,MANUFACTURE_NAME,MANUFACTURE_PART_NUMBER,VENDOR_NAME,VENDOR_PART_NUMBER,DESCRIPTION,SYSTEM_NAME,OWNER_NAME) value {self.ip, 'ethernet', ethernet[0][i], ethernet[1][i],ethernet[2][i], ethernet[3][i],ethernet[4][i], description, self.system_name, self.owner_name};"
                self.conn.execute_db(sql)
    def model_info(self):
        model1, model2, version1, version2, SN1, SN2 = self.model_information()
        sql = f'delete from card_model where IP = \'{self.ip}\''
        self.conn.execute_db(sql)
        sql = f"insert into card_model (IP, CARD1, CARD2, VERSION1, VERSION2, SYSTEM_NAME, OWNER_NAME, SN1, SN2) value {self.ip,model1,model2,version1,version2,self.system_name,self.owner_name, SN1, SN2};"
        self.conn.execute_db(sql)

    def check_techlog(self, clock):
        output = self.command('show techlog status')
        if "-----------------------" not in output:
            return
        output = output.split('\r\n')
        index = -2
        clock = clock.replace('_',' ')
        while True:
            # compare with the last techlog's date, if date is as the same as today, do not generate new techlog
            if output[index] != '':
                last_techlog = output[index]
                t = last_techlog.split()[-4:-2]  # ['Sep', '20']
                t1 = [clock.split()[0].split('-')[1],clock.split()[0].split('-')[2]]  # ['09', '20']
                if t[1] != t1[1]:
                    self.save_techlog()
                else:
                    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                    if t[0] != month[int(t1[0])-1]:
                        self.save_techlog()
                break
            index -= 1


    # still not write into DB
    def sensors_temperature(self):
        card1, card2, clock = self.temperature()
        return card1, card2

    # VM
    def vm_cpu(self):
        cpu = self.cpu_use()
        return cpu

    def vm_mem(self):
        mem = self.mem_use()
        return mem

    def vm_disk(self):
        disk = self.disk_use()
        return disk

    def sshclose(self):
        if self.ssh2:
            self.command('exit')
            self.ssh2.close()
            self.ssh.close()
            self.conn.close()

    def vm_sshclose(self):
        if self.ssh2:
            self.command_vm('exit')
            self.ssh2.close()
            self.ssh.close()
            self.conn.close()