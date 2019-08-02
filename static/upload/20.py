import pymysql

class DataBase:
    conn = None
    def __init__(self, host, user, pwd, dbname):
        self.conn = pymysql.connect(host, user, pwd, dbname);

    def res(self, sql):
        cursor = self.conn.cursor();
        cursor.execute(sql)
        result = cursor.fetchall();
        self.conn.commit();
        return result;

    def exe(self, sql):
        cursor = self.conn.cursor();
        cursor.execute(sql);
        self.conn.commit();

    def cnt(self, sql):
        cursor = self.conn.cursor();  # 初始化游标
        result = cursor.execute(sql)
        self.conn.commit();  # 提交上面的sql语句到数据库执行
        return result;

    def __del__(self):
        self.conn.close();