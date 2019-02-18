# coding=utf-8                                                                  #this must be in first line
#C:\Python27\Doc python
__author__='Maojun'

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

fabfile全局属性设定
env对象的作用是定义fabfile的全局设定，各属性说明如下：

属性	含义
env.host	定义目标主机,以python的列表表示，如env.host=['xx.xx.xx.xx','xx.xx.xx.xx']
env.exclude_hosts	排除指定主机，以python的列表表示
env.port	定义目标主机端口，默认为22
env.user	定义用户名
env.password	定义密码
env.passwords	与password功能一样，区别在于不同主机配置不同密码的应用情景,配置此项的时候需要配置用户、主机、端口等信息，
				如：env.passwords = {'root@xx.xx.xx.xx:22': '123', 'root@xx.xx.xx.xx':'234'}
env.getway	定义网关
env.deploy_release_dir	自定义全局变量
env.roledefs	定义角色分组

常用的API
Fabric支持常用的方法及说明如下：

方法	说明
local	执行本地命令，如:local('hostname')
lcd	切换本地目录,lcd('/root')
cd	切换远程目录,cd('cd')
run	执行远程命令，如：run('hostname')
sudo	sudo执行远程命令，如：sudo('echo “123456″	passwd --stdin root')
put	上传本地文件到远程主机,如：put(src,des)
get	从远程主机下载文件到本地，如：get(des,src)
prompt	获取用户输入信息，如：prompt（‘please enter a new password:’）
confirm	获取提示信息确认，如：confirm('failed.Continue[Y/n]?')
reboot	重启远程主机，reboot()
@task	函数修饰符，标识的函数为fab可调用的
@runs_once	函数修饰符，表示的函数只会执行一次

作者：爱吃土豆的程序猿
链接：https://www.jianshu.com/p/14c89ae13364

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
            # sudo('cp /mnt/version/install-activate-PMA-BML-284.bin /opt/', user='cccccaaaaaalix')
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
#     run("export PYTHONPATH=/home/maojun/PycharmProjects/cafe/cccccaaaaalix/src/ && "
#         "/opt/ActivePython-2.7/bin/python -m caferobot.cafebot --config_file /home/maojun/PycharmProjects/cafe/cccccaaaaaalix/src/perftest/cafecommander/distributed_runner/data/test_suite/robot_builtin/config.ini "
#         "--cafe_result_path /tmp/aaa$$ "
#         "/home/maojun/PycharmProjects/cafe/cccccaaaaaalix/src/perftest/cafecommander/distributed_runner/data/test_suite/robot_builtin")
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

