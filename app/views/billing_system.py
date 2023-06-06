import time


class BillingSystem:

    def __init__(self, db, charge_system):
        self.state = 0
        self.db = db
        self.charge_system = charge_system

    def add_user_bill(self, data_list): #(time, charge_time, charge_degree, charge_cost, service_cost, total_cost, user_name)
        cursor = self.db.connection.cursor()
        sql = """
            INSERT INTO bill
            (id, time, charge_time, charge_degree, user_name)
            VALUES
            (%s, %s, %s, %s, %s)
            """
        cursor.execute(sql, tuple(data_list))
        self.db.connection.commit()
        # cursor.close()

    def get_user_bill(self,username):
        cursor = self.db.connection.cursor()
        sql = """
            select*
            from bill
            where user_name = %s
            """
        cursor.execute(sql, username)
        user_bill_list = []
        result = cursor.fetchall()

        for row in result:
            user_bill_list.append(row)
            # print(row)

        return user_bill_list



    def del_user_bill(self, order_id):
        cursor = self.db.connection.cursor()
        sql = """SELECT charger_num, charge_time, charge_degree
                 FROM bill
                 WHERE id = %s"""
        cursor.execute(sql, order_id)
        result = cursor.fetchone()
        car = self.return_car_by_id(order_id)
        if not car.is_in_charger_queue_state:
            power_speed = result[2] / result[1]
            if power_speed == self.charge_system.fast_charger[0].power_per_hour:
                self.del_car_in_wait_area_queue(self.charge_system.fast_wait_area_queue, order_id)
            elif power_speed == self.charge_system.slow_charger[0].power_per_hour:
                self.del_car_in_wait_area_queue(self.charge_system.slow_wait_area_queue, order_id)
        else:
            num = int(car.charger_num[1]) - 1
            if car.charger_num[0] == 'f':
                if car.is_charge_now:
                    sql = """UPDATE bill
                             SET charge_cost = %s, service_cost = %s, total_cost = %s
                             WHERE id = %s"""
                    start_charge_simulate_time = str(car.start_charge_simulate_time.hour) + ':' \
                                                 + str(car.start_charge_simulate_time.minute)
                    current_simulate_time = str(self.charge_system.timer.get_simulate_time().hour) + ':' \
                                                 + str(self.charge_system.timer.get_simulate_time().minute)
                    charge_cost, service_cost = self.calculate_charging_cost('fast', start_charge_simulate_time
                                                                             , current_simulate_time, 1.0, 0.7, 0.4)
                    total_cost = charge_cost + service_cost
                    cursor.execute(sql, [charge_cost, service_cost, total_cost, order_id])
                    self.db.connection.commit()
                    if self.charge_system.fast_charger[num].queue.qsize() == 1:
                        self.charge_system.fast_charger[num].use_state = False
                        self.charge_system.fast_charger[num].queue.get()
                        return
                    else:
                        self.charge_system.fast_charger[num].queue.queue.pop()
                # self.del_car_in_queue(self.charge_system.fast_charger[num].queue, order_id)
            elif car.charger_num[0] == 's':
                if car.is_charge_now:
                    sql = """UPDATE bill
                             SET charge_cost = %s, service_cost = %s, total_cost = %s
                             WHERE id = %s"""
                    start_charge_simulate_time = str(car.start_charge_simulate_time.hour) + ':' \
                                                 + str(car.start_charge_simulate_time.minute)
                    current_simulate_time = str(self.charge_system.timer.get_simulate_time().hour) + ':' \
                                            + str(self.charge_system.timer.get_simulate_time().minute)
                    charge_cost, service_cost = self.calculate_charging_cost('slow', start_charge_simulate_time
                                                                             , current_simulate_time, 1.0, 0.7, 0.4)
                    total_cost = charge_cost + service_cost
                    cursor.execute(sql, [charge_cost, service_cost, total_cost, order_id])
                    self.db.connection.commit()
                    if self.charge_system.slow_charger[num].queue.qsize() == 1:
                        self.charge_system.slow_charger[num].use_state = False
                        self.charge_system.slow_charger[num].queue.get()
                        return
                    else:
                        self.charge_system.slow_charger[num].queue.queue.pop()
                # self.del_car_in_queue(self.charge_system.slow_charger[num].queue, order_id)
        sql = """DELETE FROM bill 
                 WHERE id = %s"""
        cursor.execute(sql, order_id)
        self.db.connection.commit()

    def calculate_charging_cost(self, mode: str, start_time, end_time, peak_rate, standard_rate, off_peak_rate):
        """
        计算充电费用
        :param start_time: 充电开始时间，格式为"HH:MM"，例如"08:30"
        :param end_time: 充电结束时间，格式为"HH:MM"，例如"12:45"
        :param peak_rate: 峰时费率，单位为元/小时
        :param off_peak_rate: 谷时费率，单位为元/小时
        :param standard_rate: 平时费率，单位为元/小时
        :return: 充电费用，单位为元
        """
        start_hour, start_minute = map(int, start_time.split(":"))
        end_hour, end_minute = map(int, end_time.split(":"))

        # 将起始时间和结束时间转换为分钟数
        start_minute = start_hour * 60 + start_minute
        end_minute = end_hour * 60 + end_minute

        # 计算总充电时间，单位为分钟
        total_minutes = end_minute - start_minute
        total_hour = total_minutes / 60
        if mode == 'fast':
            service_cost = total_hour * 30 * 0.8
        elif mode == 'slow':
            service_cost = total_hour * 7 * 0.8

        # 初始化总费用为0
        total_cost = 0

        end = (start_minute // 60 + 1) * 60
        if start_minute >= 600 and start_minute < 900:  # 峰时
            cost = peak_rate * ((end - start_minute) / 60)
        elif start_minute >= 1080 and start_minute < 1260:  # 峰时
            cost = peak_rate * ((end - start_minute) / 60)
        elif start_minute >= 420 and start_minute < 600:  # 平时
            cost = standard_rate * ((end - start_minute) / 60)
        elif start_minute >= 900 and start_minute < 1080:  # 平时
            cost = standard_rate * ((end - start_minute) / 60)
        elif start_minute >= 1260 and start_minute < 1380:  # 平时
            cost = standard_rate * ((end - start_minute) / 60)
        else:  # 谷时
            cost = off_peak_rate * ((end - start_minute) / 60)

        if mode == 'fast':
            cost *= 30
        elif mode == 'slow':
            cost *= 7
        # 累加当前时间段的费用
        total_cost += cost

        start_minute = (start_minute // 60 + 1) * 60
        # 遍历充电时间段，计算每个时间段的费用
        while start_minute < end_minute:
            # 判断当前时间段属于哪个时间段
            if start_minute >= 600 and start_minute < 900:  # 峰时
                cost = peak_rate * min(1, (end_minute - start_minute) / 60)
            elif start_minute >= 1080 and start_minute < 1260:  # 峰时
                cost = peak_rate * min(1, (end_minute - start_minute) / 60)
            elif start_minute >= 420 and start_minute < 600:  # 平时
                cost = standard_rate * min(1, (end_minute - start_minute) / 60)
            elif start_minute >= 900 and start_minute < 1080:  # 平时
                cost = standard_rate * min(1, (end_minute - start_minute) / 60)
            elif start_minute >= 1260 and start_minute < 1380:  # 平时
                cost = standard_rate * min(1, (end_minute - start_minute) / 60)
            else:  # 谷时
                cost = off_peak_rate * min(1, (end_minute - start_minute) / 60)

            if mode == 'fast':
                cost *= 30
            elif mode == 'slow':
                cost *= 7
            # 累加当前时间段的费用
            total_cost += cost

            # 将起始时间调整到下一个时间段的开始时间
            start_minute = (start_minute // 60 + 1) * 60

        return total_cost, service_cost

    def del_car_in_wait_area_queue(self, queue, element_to_remove):
        queue_size = queue.qsize()  # 获取队列的大小
        for i in range(queue_size):
            element = queue.queue[i].order_id
            queue.get()
            if element == element_to_remove:
                continue  # 跳过要移除的元素
            queue.put(element)

    def return_car_by_id(self, element_to_find):
        queue = self.charge_system.fast_wait_area_queue
        queue_size = queue.qsize()  # 获取队列的大小
        for i in range(queue_size):
            element = queue.queue[i].order_id
            if element == element_to_find:
                return queue.queue[i]
        queue = self.charge_system.slow_wait_area_queue
        queue_size = queue.qsize()  # 获取队列的大小
        for i in range(queue_size):
            element = queue.queue[i].order_id
            if element == element_to_find:
                return queue.queue[i]
        for fast_charger in self.charge_system.fast_charger:
            queue = fast_charger.queue
            queue_size = queue.qsize()  # 获取队列的大小
            for i in range(queue_size):
                element = queue.queue[i].order_id
                if element == element_to_find:
                    return queue.queue[i]
        for slow_charger in self.charge_system.slow_charger:
            queue = slow_charger.queue
            queue_size = queue.qsize()  # 获取队列的大小
            for i in range(queue_size):
                element = queue.queue[i].order_id
                if element == element_to_find:
                    return queue.queue[i]

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