import time

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler,ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import yaml
from Setting import ftp_info

root_dir = ftp_info['root_dir']
port = ftp_info['port']
ftp_user = ftp_info['user']
ftp_pwd = ftp_info['pwd']


# 实例化虚拟用户，这是FTP的首要条件
authorizer = DummyAuthorizer()
# 添加用户权限和路径，括号内的参数是（用户名、密码、用户目录、权限），可以为不同的用户添加不同的目录和权限
authorizer.add_user(ftp_user, ftp_pwd, root_dir, perm='elradfmw')
# 添加匿名用户（用户名："anonymous"，密码为空），只需要路径
authorizer.add_anonymous(root_dir)

# 初始化ftp句柄
handler = FTPHandler
handler.authorizer = authorizer

# 上传下载的速度设置
# dtp_handler = ThrottledDTPHandler
# dtp_handler.read_limit = 300 * 1024          # 300 kb/s
# dtp_handler.write_limit = 300 * 1024         # 300 kb/s
# handler.dtp_handler = dtp_handler



# 监听ip和端口 ， linux里需要root用户才能使用21端口
server = FTPServer(('0.0.0.0', port), handler)

# 最大连接数
# server.max_cons = 150
# server.max_cons_per_ip = 15

# 开始服务，自带打印日志信息
server.serve_forever()

