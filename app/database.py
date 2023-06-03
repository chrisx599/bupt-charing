import pymysql

class DBConfig:
    def __init__(self) -> None:
        self.database()

    def database(self):
        # 创建数据库连接
        self.connection = pymysql.connect(
            host="rm-2ze935axdc9v74c3ono.mysql.rds.aliyuncs.com",
            port=3306,
            user='chr1ce',
            password='wolegequ599L',
            database='chr1ce_db',
            charset='utf8mb4'
        )

