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

"""

dhcp = 'root@10.245.59.200:22' # 这里root ip 和 端口22一个都不能少哦
smx = 'user@10.245.247.60:22'
cafe = 'sewang@10.245.243.11:22'


env.passwords = {dhcp:'rootgod',
                 smx:'xxxx123',
                 cafe: 'password77'}

env.roledefs = {'dhcp':[dhcp],
                'smx':[smx],
                'cafe': [cafe]}

env.parallel = False
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
            print green("****print local files")
            # python_log = run('python 1.py')
    with cd('/home/sean'):
        run('pwd')


@roles('cafe')
def cafe_vm():
    run('ls')

@task
def dotask():
    execute(smx_server)
    execute(dhcp_server)
    execute(cafe_vm)








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

