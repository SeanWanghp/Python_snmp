# 服务端口配置
SERVER_HOST = "nanst-nagios-06.calix.local"
SERVER_PORT = 5000

# MySQL配置
# host = "nanst-nagios-06.calix.local"
# port = 3307
# database = "monitor"
# user = "root"
# passwd = "123456"
# TESTBEDS_INFO = 'testbeds_info'


# MySQL配置
host = "10.245.46.201"
port = 3306
database = "monitor"
user = "sean"
passwd = "p@SSword77"
TESTBEDS_INFO = 'testbeds_info'

# token过期时间(单位：秒)
EXPIRE_TIME = 600

# MD5加密盐值
MD5_SALT = "test2020#%*"

# VM文件存储地址
systemFile = r'/home/corey/system_file'
# monitorFile = r'/home/corey/python_script/monitor.log'
monitorFile = r'C:\GitHub\python_lib\AXOS\python_script\Main.py'
monitormore = r'C:\GitHub\python_lib\AXOS\python_script\monitor.log'
PICTURE_UPLOAD_PATH = r'/home/corey/monitor-web/src/assets'

# 设置拓扑图的root ip
rootIP = '10.245.48.21'