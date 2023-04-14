from FetchData import FetchData
import yaml
from Setting import database

def olt_login(ip, port, system_name, owner_name):
    # root permissions login
    username = 'calixsupport'
    password = 'calixsupport'

    """ssh Link and Mysql DB Link"""
    fetch = FetchData(ip, port, system_name, owner_name, username, password)

    fetch.check_olt()
    return fetch, username


def vm_login(ip, port, system_name, owner_name):
    if 'GEO SMX system' in system_name:
        username = 'root'
        password = 'f0rmat'
    else:
        username = 'calix'
        password = 'Calix123'

    fetch = FetchData(ip, port, system_name, owner_name, username, password)

    fetch.check_vm()
    return fetch