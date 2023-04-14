import os
import os.path
from pathlib import Path
from setting import SERVER_PORT, systemFile, SERVER_HOST
from ssh import SSH

from threading import Thread


def execute(ip, c):
    link = SSH()
    link.olt_login(ip)
    output = link.command(c)
    return output


class CLI(Thread):
    def __init__(self, ip, c, system_name=''):
        Thread.__init__(self)
        self.result = None
        self.system_name = system_name
        self.ip = ip
        self.cli = c

    def run(self):
        try:
            self.result = execute(self.ip, self.cli)
        except Exception as e:
            self.result = 'Wrong!!!'

    def get_result(self):
        return self.result


def retrieve_dir(dir, nodeID):
    p = Path(dir)
    DirTree = []
    for p in list(p.glob('*')):
        fullPath = str(p.parent) + '\\' + str(p.name)
        index = fullPath.split('system_file')[1].replace('\\', '$').replace('/', '$')
        if p.is_file():
            path = f"http://{SERVER_HOST}:{SERVER_PORT}/downloadSystemFile/" + index
            DirTree.append(
                {'id': nodeID, "fileName": p.name, 'path': path, "type": "file"})
            nodeID += 1
        else:
            subdir, nodeID = retrieve_dir(os.path.join(dir, p.name), nodeID=nodeID)
            path = f"http://{SERVER_HOST}:{SERVER_PORT}/downloadSystemFile/" + index
            DirTree.append(
                {'id': nodeID, "fileName": p.name, 'path': path, "type": "folder",
                 "children": subdir})
            nodeID += 1

    return DirTree, nodeID


def cleanOldIP(old_ip, db):
    sql = f'delete from card_model where IP = \'{old_ip}\''
    db.execute_db(sql)
    sql = f'delete from module_information where IP = \'{old_ip}\''
    db.execute_db(sql)
    sql = f'delete from ont_online where IP = \'{old_ip}\''
    db.execute_db(sql)
