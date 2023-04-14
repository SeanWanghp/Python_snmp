import re
import os
import datetime
import pandas as pd
import pymysql
import yaml
import threading
import time
from SSH import olt_login, vm_login
from Dao import MysqlDb
import openpyxl
from pythonping import ping
from Setting import ftp_info, ISDEBUG, TESTBEDS_INFO

root_dir = ftp_info['root_dir']


class Run_script:
    def __init__(self, ISROOT, INTERVAL, server, GAP):
        self.ISROOT = ISROOT
        self.INTERVAL = INTERVAL
        self.server = server
        self.GAP = GAP

    # save startup_config.xml every {gap} days
    def save_startup_config_loop(self, ip, port, system_name, owner_name):
        while True:
            try:
                fetch, username = olt_login(ip=ip, port=port, system_name=system_name,
                                            owner_name=owner_name)
                try:
                    # create the ftp_dir
                    fetch.save_startup_config()
                except Exception as e:
                    print(f"error :{e}")
                finally:
                    """close SSH link"""
                    fetch.sshclose()
            except Exception as e:
                print(f"error :{e}")
            time.sleep(60 * 60 * 24 * self.GAP)

    # monitor_script loop
    def loop_run(self, ip, port, system_name, owner_name, initial):
        """use username and psw to login and SSH link"""
        # don't use try……catch
        if ISDEBUG:
            fetch, username = olt_login(ip=ip, port=port, system_name=system_name,
                                        owner_name=owner_name)
            print(ip)

            path = f'{root_dir}/{ip}'
            if not os.path.exists(f'{root_dir}/{ip}'):
                os.makedirs(path)
            # fetch data
            if self.ISROOT:
                # flag of config changed
                pre_config = None
                # test whether can login in the debug mood
                fetch.command('\n')
                output = fetch.command("shell")
                fetch.command('\n')
                # can't login in the debug mood, need to change config
                if re.search(r"error", output) is not None:
                    pre_config = fetch.change_config()
                    fetch.sshclose()
                    fetch, username = olt_login(ip=ip, port=port, system_name=system_name,
                                                owner_name=owner_name)
                    fetch.command('\n')
                # login in the debug mood again after change the config
                fetch.debugLogin()
                """Fetch data begin"""
                fetch.root_cli(server=self.server, initial=initial, INTERVAL=self.INTERVAL)
                fetch.general_cli(server=self.server)
                if pre_config is not None:
                    fetch.change_config_back(pre_config=pre_config)
            else:
                fetch.general_cli(server=self.server)
            fetch.sshclose()

        # use try……catch
        else:
            try:
                fetch, username = olt_login(ip=ip, port=port, system_name=system_name,
                                            owner_name=owner_name)
                try:
                    # create the ftp_dir
                    path = f'{root_dir}/{ip}'
                    if not os.path.exists(f'{root_dir}/{ip}'):
                        os.makedirs(path)
                    # fetch data
                    if self.ISROOT:
                        # flag of config changed
                        pre_config = None
                        # test whether can login in the debug mood
                        fetch.command('\n')
                        output = fetch.command("shell")
                        fetch.command('\n')
                        # can't login in the debug mood, need to change config
                        if re.search(r"error", output) is not None:
                            pre_config = fetch.change_config()
                            fetch.sshclose()
                            fetch, username = olt_login(ip=ip, port=port, system_name=system_name,
                                                        owner_name=owner_name)
                            fetch.command('\n')
                        # login in the debug mood again after change the config
                        fetch.debugLogin()
                        """Fetch data begin"""
                        fetch.root_cli(server=self.server, initial=initial, INTERVAL=self.INTERVAL)
                        fetch.general_cli(server=self.server)
                        if pre_config is not None:
                            fetch.change_config_back(pre_config=pre_config)
                    else:
                        fetch.general_cli(server=self.server)
                except Exception as e:
                    print(f"error: {e} ({ip})")
                finally:
                    """close SSH link"""
                    fetch.sshclose()
            except Exception as e1:
                db = MysqlDb()
                sql = f'select Connected from {TESTBEDS_INFO} where ip=\'{ip}\''
                flag = db.select(sql)[0]
                if flag['Connected'] != 0:
                    sql = f'update {TESTBEDS_INFO} set connected = 3 where ip=\'{ip}\''
                    db.execute_db(sql)

                print(f"error: {e1} ({ip})")

    def VM_detect(self, ip, port, system_name, owner_name):
        if ISDEBUG:
            fetch = vm_login(ip=ip, port=port, system_name=system_name, owner_name=owner_name)
            fetch.vm_cli(server=self.server)
            fetch.vm_sshclose()
        else:
            try:
                fetch = vm_login(ip=ip, port=port, system_name=system_name, owner_name=owner_name)
                try:
                    fetch.vm_cli(server=self.server)
                except Exception as e:
                    print(f"error: {e} ({ip})")
                finally:
                    """close SSH link"""
                    fetch.vm_sshclose()
            except Exception as e1:
                db = MysqlDb()
                sql = f'select Connected from {TESTBEDS_INFO} where ip=\'{ip}\''
                flag = db.select(sql)[0]
                if flag['Connected'] != 0:
                    sql = f'update {TESTBEDS_INFO} set connected = 3 where ip=\'{ip}\''
                    db.execute_db(sql)

                print(f"error: {e1} ({ip})")

    def Individual_detect(self, ip, port, owner_name):
        try:
            fetch, username = olt_login(ip=ip, port=port, system_name='', owner_name=owner_name)
            try:
                fetch.command('pag false')
                fetch.model_info()
                fetch.ont_online_info()
                fetch.module_info()
            except Exception as e:
                print(f"error: {e} ({ip})")
            finally:
                """close SSH link"""
                fetch.sshclose()
        except Exception as e1:
            db = MysqlDb()
            sql = f'select Connected from {TESTBEDS_INFO} where ip=\'{ip}\''
            flag = db.select(sql)[0]
            if flag['Connected'] != 0:
                sql = f'update {TESTBEDS_INFO} set connected = 3 where ip=\'{ip}\''
                db.execute_db(sql)
            print(f"error: {e1} ({ip})")

    def run(self):
        # check the program that weather it is first time start
        initial = True

        # after every loop, the monitor_script auto ssh all the ip again to avoid some of them disconnect
        while True:
            db = MysqlDb()
            sql = f'select * from {TESTBEDS_INFO}'
            cases = db.select(sql)
            db.close()
            systems = {}
            individuals = {}
            vms = {}
            try:
                for item in cases:
                    if item['Type'] == 'VM' or item['Type'] == 'vm':
                        if item['Owner'] not in vms.keys():
                            vms[item['Owner']] = {item['System']: [item['IP']]}
                        else:
                            if item['System'] not in vms[item['Owner']].keys():
                                vms[item['Owner']][item['System']] = [item['IP']]
                            else:
                                vms[item['Owner']][item['System']].append(item['IP'])
                    elif item['System'] == '':
                        if item['Owner'] not in individuals.keys():
                            individuals[item['Owner']] = [item['IP']]
                        else:
                            individuals[item['Owner']].append(item['IP'])

                    else:
                        if item['Owner'] not in systems.keys():
                            systems[item['Owner']] = {item['System']: [item['IP']]}
                        else:
                            if item['System'] not in systems[item['Owner']].keys():
                                systems[item['Owner']][item['System']] = [item['IP']]
                            else:
                                systems[item['Owner']][item['System']].append(item['IP'])
            except Exception as e:
                assert False, "read ips error"
            # if initial:
            #     # asynchronize to save config
            #     print(str(datetime.datetime.now()) + ' save the startup_config begins')
            #     for owner_name in systems.keys():
            #         for system_dict in systems[owner_name].items():
            #             for ip in system_dict[1]:
            #                 threading.Thread(target=self.save_startup_config_loop,
            #                                  args=(ip, 22, system_dict[0], owner_name)).start()
            #     time.sleep(10)

            """ all systems detect """
            print(str(datetime.datetime.now()) + " fetch OLT data begin")
            # clean the thread pool

            l = []
            count = 0
            # create the thread pool
            for owner_name in systems.keys():
                for system_dict in systems[owner_name].items():
                    for ip in system_dict[1]:
                        t = threading.Thread(target=self.loop_run, args=(ip, 22, system_dict[0], owner_name, initial))
                        l.append(t)

            # thread start
            for t in l:
                t.start()
                count += 1

            # thread synchronized
            for t in l:
                t.join()

            """ all individuals detect """
            print(str(datetime.datetime.now()) + " fetch Individual data begin")
            # clean the thread pool

            l = []
            count = 0
            # create the thread pool
            for owner_name in individuals.keys():
                for ip in individuals[owner_name]:
                    t = threading.Thread(target=self.Individual_detect, args=(ip, 22, owner_name))
                    l.append(t)

            # thread start
            for t in l:
                t.start()
                count += 1

            # thread synchronized
            for t in l:
                t.join()

            """ all VMs detect """
            print(str(datetime.datetime.now()) + f' fetch VM data begin')
            l = []
            count = 0

            for owner_name in vms.keys():
                for vm_dict in vms[owner_name].items():
                    for ip in vm_dict[1]:
                        t = threading.Thread(target=self.VM_detect, args=(ip, 22, vm_dict[0], owner_name))
                        l.append(t)

            # thread start
            for t in l:
                t.start()
                count += 1

            # thread synchronized
            for t in l:
                t.join()

            initial = False
            print(
                str(datetime.datetime.now()) + f' script pause for {self.INTERVAL} seconds, please waiting.......................\n')
            time.sleep(self.INTERVAL)
