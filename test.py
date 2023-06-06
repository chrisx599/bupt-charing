# from app.database import DBConfig
#
# db = DBConfig()
# cursor = db.connection.cursor()
# sql = """SELECT charger_num, charge_time, charge_degree, id
#          FROM bill
#          WHERE id = %s"""
# cursor.execute(sql, 'e2c2477e-03b4-11ee-8cdc-a87eea364d30')
# result = cursor.fetchone()
# print(result)
# print(type(result[0]))
# if result[0]:
#     print("666")
# print(type(result[1]))
# print(type(result[2]))
# print(type(result[3]))
# cursor.close()
# db.connection.close()
# import queue
# my_queue = queue.Queue()  # 创建一个空队列
#
# # 向队列中添加元素
# my_queue.put(1)
# my_queue.put(2)
# my_queue.put(3)
#
# print("原始队列:", my_queue.queue)
#
# # 删除队尾元素
# if my_queue:
#     my_queue.queue.pop()
#
# print("删除队尾元素后的队列:", my_queue.queue)

def calculate_charging_cost(mode: str, start_time, end_time, peak_rate, standard_rate, off_peak_rate):
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

cost, cs2 = calculate_charging_cost('fast', '3:39', '5:51', 1.0, 0.7, 0.4)
# cost, cs2 = calculate_charging_cost('fast', '4:00', '5:51', 1.0, 0.7, 0.4)
print(cost, cs2)
