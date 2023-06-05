class BillingSystem:

    def __init__(self,db):
        self.state = 0
        self.db = db

    def add_user_bill(self,data_list): #(time, charge_time, charge_degree, charge_cost, service_cost, total_cost, user_name)
        cursor = self.db.connection.cursor()
        sql = """
            INSERT INTO bill
            (time, charge_time, charge_degree, charge_cost, service_cost, total_cost, user_name)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(sql, tuple(data_list))
        self.db.connection.commit()


class Bill:
    def __int__(self):
        self.id = None #初始化可确定
        self.time = None #读取此刻系统时间，提交订单时确定
        self.charger_num = None #充电桩编号，开始充电时确定
        self.charge_degree = None #充电度数，提交订单时确定
        self.charge_time = None #充电总时长，需要充多久，提交时确定
        self.start_time = None #充电开始时间，充电时确定
        self.end_time = None #充电结束时间，若无故障，无提前停止，即为开始时间+充电时间，充电时确定
        self.charge_cost = None #充电费，充电度数*每度价格，每度价格根据日期有所不同，提交订单时确定
        self.service_cost = None #服务费，充电度数*服务费，提交订单时确定
        self.total_cost = None #总花费为充电费+服务费，提交订单时确定
        self.user_name = None #用户名