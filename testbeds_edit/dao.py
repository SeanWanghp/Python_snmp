import pymysql
from setting import host, port, user, passwd, database


class MysqlDb():

    def __init__(self, host, port, user, passwd, db):
        # 建立数据库连接
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
            autocommit=True
        )
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self): # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select(self, sql):
        try:
            # 查询
            print(sql)
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # sql = "select * from testbeds_info"
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 使用 fetchall() 获取查询结果
            data = self.cur.fetchall()
            return data
        except Exception as e:
            print("mysql查找操作出现错误：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()


    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            print(sql)
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            print("mysql更新/新增/删除操作出现错误：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()

db = MysqlDb(host, port, user, passwd, database)
