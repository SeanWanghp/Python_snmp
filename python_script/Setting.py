# Code MACRO definition
ISDEBUG = False
ISROOT = True  # whether is debug mode
INTERVAL = 21600  # seconds between every Loop
GAP = 3  # the days' number which gap between backup startup_config processes
INIT_REBOOT_TIME = True  # set all the reboot_time zero
TESTBEDS_INFO = 'testbeds_info'  # r对路径进行转义，windows需要

# mysql database config
database = {
    'host': 'nanst-nagios-06.calix.local',
    'port': 3307,
    'db_name': 'monitor',
    'user': 'root',
    'password': '123456'
}

ftp_info = {
    'host': 'nanst-nagios-06.calix.local',
    'port': 1110,
    'root_dir': '/home/corey/system_file/',
    'user': 'Corey',
    'pwd': 'Corey'
}
