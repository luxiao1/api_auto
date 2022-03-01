import pymysql
from pymysql.cursors import DictCursor


class SQLdbHandler:
    def __init__(self, db_config):
        """
        创建数据库连接
        :param db_config: 是一个字典
        """
        engine = db_config.pop('engine', 'mysql')
        if engine.lower() == 'mysql':
            self.conn = pymysql.connect(**db_config)
        elif engine.lower() == 'oracle':
            pass
    def excute(self,sql,action,res_type='t',*args):
        """
        执行sql
        :param sql:
        :param action: 字符串，指定执行cursor对应的方法
        :param res_type:
        :param args: 其他参数，比如执行fetchmany传入的size
        :return:
        """
        if res_type == 't':
            cursor = self.conn.cursor()
        else:
            cursor = self.conn.cursor(DictCursor)

        try:
            cursor.execute(sql)
            return getattr(cursor,action)(*args)
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def get_one(self, sql, res_type='t'):
        """

        :param sql:
        :param res_type: 返回数据的类型，默认为‘t’表示以元组返回，‘d’表示以字典返回
        :return:
        """
        # if res_type == 't':
        #     cursor = self.conn.cursor()
        # else:
        #     cursor = self.conn.cursor(DictCursor)
        #
        # try:
        #     cursor.execute(sql)
        #     return cursor.fetchone()
        # except Exception as e:
        #     raise e
        # finally:
        #     cursor.close()
        return self.excute(sql,'fetchone',res_type)

    def get_many(self, sql, size, res_type='t'):
        return self.excute(sql, 'fetchmany', res_type,size)

    def get_all(self, sql, res_type='t'):
        return self.excute(sql, 'fetchall', res_type)

    def exist(self,sql):
        if self.get_one(sql):
            return True
        else:
            return False

    def __del__(self):
        """
        关闭数据库连接
        :return:
        """
        self.conn.close()



if __name__ == '__main__':
    db_config = {
        'host': 'api.lemonban.com',
        'user': 'future',
        'password': '123456',
        'port': 3306,
        'db': 'futureloan',
        'charset': 'utf8'
    }
    db = SQLdbHandler(db_config)
    sql = 'select id,reg_name from member limit 5'
    res = db.get_one(sql,res_type='d')
    print(res)

    res1 = db.get_many(sql,res_type='d',size=5)
    print(res1)
