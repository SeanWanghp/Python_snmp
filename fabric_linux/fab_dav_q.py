#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from fabric.contrib.files import *
from fabric.decorators import hosts
from fabric.operations import run, sudo, local
from fabric.state import env
from fabric.colors import *

"""
Created on 04/08/2018

现在遇到错误时，控制台会打出一个警告信息，然后继续执行后续任务。那我们怎么捕获错误并处理呢？像”run()”, “local()”, 
“sudo()”, “get()”, “put()”等SSH功能函数都有返回值。当返回值的”succeeded”属性为True时，说明执行成功，反之就是失败。
你也可以检查返回值的”failed”属性，为True时就表示执行失败，有错误发生。

"""

dhcp = 'root@10.245.59.200:22' # 这里root ip 和 端口22一个都不能少哦
smx = 'calix@10.245.247.60:22'
smx_2 = 'calix@10.245.247.6:22'
cafe = 'sewang@10.245.243.11:22'


env.passwords = {dhcp: 'rootgod',
                 smx: 'Calix123',
                 smx_2: 'Calix123',
                 cafe: 'password77'}

env.roledefs = {'dhcp': [dhcp],
                'smx': [smx],
                'smx_2': [smx_2],
                'cafe': [cafe]}

env.parallel = False
env.warn_only = True
env.source_dir="/opt/"
# env.dest_dir="/opt/machtalk/"
env.sudo_prefix = 'sudo'

# @task
@roles('smx')
def smx_server():
    baseline = 'install-activate-PMA-B3L6-69.bin'
    run('pwd')
    with cd('/opt/pma/PMAPMAA/bin'):
        run('./ver.sh')
        with cd('/opt'):
            run('ls')
        with cd ('/mnt/version'):
            run('ls -a')
            # sudo('cp /mnt/version/install-activate-PMA-B3L6-69 /opt/', pty=False)
            # run('sudo cp /mnt/version/%s /opt/'%baseline, shell= False)        #this need remove 'sudo -i' with password
            # sudo('cp /mnt/version/install-activate-PMA-BML-284.bin /opt/', user='calix')
        # run('sudo -i')  #switch user to root and manual run command
        with cd('/opt'):
            run('ls -a')
            # run('sudo rm -rf %s'%baseline)
            run('ls -a')
        # run('cp /mnt/version/install-activate-PMA-BML-127.bin /opt/')
        run('pwd')
        # prompt('password: ')



@roles('dhcp')
def dhcp_server():
    run('pwd')
    with cd('/root'):
        with cd('Desktop'):
            run('ls')
            print(green("****print(local files"))
            upload = put('diango_run.bat', '/root/Desktop')
            if upload.failed:
                print("fail")
                sudo('rm diango_run.bat')
                put('diango_run.bat', '/root/Desktop', use_sudo=True)
            elif upload.succeeded:
                print("upload succeeded")
            download = get('/root/Desktop/diango_run.bat', None)
            if download.failed:
                print('failed')
            elif upload.succeeded:
                print("download succeeded")

            # python_log = run('python 1.py')
    with cd('/home/sean'), prefix('ls'):
        for i in range(0, 2):
            run('pwd')
    with prefix("cd /home"):
        run('pwd')
        local('pwd')

# @parallel
@roles('cafe')
def cafe_vm():
    run('ls')

@roles('smx_2')
def smx_server_2():
    run('ssh root@10.245.46.216')
    if prompt('password:'):
        run('root')
    # if confirm("password:"):
        # run("root")
    # run('yes')
    # run('root')
    run('ps aux --sort -rss')

@task
def dotask():
    '''C:\GitHub\python_lib\basic_lib\fabric_basic>fab -H localhost -f fab_dav_q.py dotask
    fab -f fab_dav_q.py dotask'''
    # execute(smx_server)
    # execute(dhcp_server)
    # execute(cafe_vm)
    execute(smx_server_2)








# executor_hosts = ['nanlnx-ccafe28']
# executor_dup_cnt = 10
# mq_host = ['nanlnx-ccafe03']
# cafecommander_host = ['nanlnx-ccafe131']
#
# env.user = 'cafetest'
# env.password = 'cafetest'
# env.parallel = True
# env.dedupe_hosts = False
#
#
# @hosts(executor_hosts)
# def deploy_cafe():
#     """
#     Deploy cafe on the VMs
#     """
#     run('mkdir mycafe || ls')
#     run('cd mycafe && rm -rf cafe && git clone http://git/repos/sqa/cafe.git && cd cafe && git checkout S-01902')
#     install_deps()
#
#
# @hosts(executor_hosts)
# def install_deps():
#     sudo('/opt/ActivePython-2.7/bin/pip install celery objgraph cerberus ipaddress netaddr', shell=False)
#
#
# @hosts(executor_hosts * executor_dup_cnt)
# def start_test():
#     """
#     Run test suites
#     """
#     run("export PYTHONPATH=/home/xizhang/PycharmProjects/cafe/calix/src/ && "
#         "/opt/ActivePython-2.7/bin/python -m caferobot.cafebot --config_file /home/xizhang/PycharmProjects/cafe/calix/src/perftest/cafecommander/distributed_runner/data/test_suite/robot_builtin/config.ini "
#         "--cafe_result_path /tmp/aaa$$ "
#         "/home/xizhang/PycharmProjects/cafe/calix/src/perftest/cafecommander/distributed_runner/data/test_suite/robot_builtin")
#
#
# def print_hostname():
#     run('uname -a; sleep 3')
#
# @hosts(mq_host + cafecommander_host)
# def get_cpu(interval=10, count=30):
#     ret = run('sar -u %d %d' % (interval, count))
#     _save_logs('%s_cpu.log' % env.host, ret)
#
#
# @hosts(mq_host + cafecommander_host)
# def get_mem(interval=10, count=30):
#     ret = run('sar -r %d %d' % (interval, count))
#     _save_logs('%s_mem.log' % env.host, ret)
#
#
# @hosts(mq_host + cafecommander_host)
# def get_load(interval=10, count=30):
#     ret = run('sar -q %d %d' % (interval, count))
#     _save_logs('%s_load.log' % env.host, ret)
#
#
# def _save_logs(logname, content):
#     dirname = 'logs'
#     local('mkdir -p %s' % dirname)
#     logname = os.path.join(dirname, logname)
#     with open(logname, 'w') as f:
#         f.write(content)

