import queue
import threading
import time


class Charger():
    def __init__(self) -> None:
        self.power_per_hour = None
        self.queue = queue.Queue(2)
        self.charger_state = True  # 充电桩的状态(好坏)
        self.use_state = False  # 充电桩的使用状态
        self.total_times = 0  # 总共使用次数
        self.total_charge_power = 0  # 总共充了多少电
        self.total_charge_time = 0  # 总共充电时间


    def join(self):
        if self.queue.full():
            return -1
        else:
            self.queue.put(True)
            return 1


class FastCharger(Charger):
    def __init__(self) -> None:
        super().__init__()
        self.power_per_hour = 30.0


class SlowCharger(Charger):
    def __init__(self) -> None:
        super().__init__()
        self.power_per_hour = 7.0

class Car():
    def __init__(self, user_name, car_id, need_power, charge_mode) -> None:
        self.user_name = user_name
        self.car_id = car_id
        self.need_power = float(need_power)
        self.join_wait_area_time = None
        self.join_charge_queue_time = None
        self.start_charge_time = None
        self.over_charge_time = None
        self.charge_need_time = None
        self.remain_charge_time = None
        self.already_charge_time = None
        self.charge_mode = None
        

def init_charger():
    """
    返回两个快充和三个慢充
    """
    fastcharger = []
    slowcharger = []
    for i in range(2):
        obj = FastCharger()
        fastcharger.append(obj)
    for i in range(3):
        obj = SlowCharger()
        slowcharger.append(obj)

    return fastcharger, slowcharger


def init_wait_area():
    """
    返回等待区六个车位
    """
    fast_wait_area_queue = queue.Queue()
    slow_wait_area_queue = queue.Queue()
    return fast_wait_area_queue, slow_wait_area_queue


def implement_charge(charge_mode, car_id, car_need_power
                     , fastcharger, slowcharger, wait_area_queue
                     , username):
    if wait_area_queue.full():
        # 车位已满无法处理
        return -1
    else:
        # 先进入等待区
        car_info = Car(username, car_id, car_need_power)
        wait_area_queue = queue.Queue()
        wait_area_queue.put(car_info)


class ChargeSystem(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        # 初始化充电系统
        self.fast_charger, self.slow_charger = init_charger()
        self.fast_wait_area_queue, self.slow_wait_area_queue = init_wait_area()
        # 初始化时钟系统
        self.timer = SimulateTimer()
        self.start()


    def run(self) -> None:
        while True:
            # 更新等待区的状态
            self.update_wait_station()

            # 更新充电区每个充电桩的状态
            self.update_charger_station()

            # print("等待区快充等待队列", self.fast_wait_area_queue.qsize())
            # print("快充1队列", self.fast_charger[0].queue.qsize())
            # print("快充2队列", self.fast_charger[1].queue.qsize())
            # print("快充1状态", self.fast_charger[0].use_state)
            # print("快充2状态", self.fast_charger[1].use_state)



    def update_wait_station(self):
        # print("正在调度等待区")
        # 更新等待区的状态
        # 快充等待队列
        if not self.fast_wait_area_queue.empty():
            is_all_charger_queue_full = True
            for charger in self.fast_charger:
                if charger.charger_state and not charger.queue.full():
                    is_all_charger_queue_full = False
                    break
            if not is_all_charger_queue_full:
                queue_length = self.fast_wait_area_queue.qsize()
                for i in range(queue_length):
                # for item in self.fast_wait_area_queue.queue.copy():
                    # 看哪个快充充电桩有空闲位置并且等待时间最短
                    current_time = time.time()
                    best_charger = None
                    best_time = float('inf')
                    for charger in self.fast_charger:
                        # 先检查充电桩的状态是否是好的
                        if charger.charger_state:
                            # 看充电桩是否正在被使用
                            if not charger.use_state:
                                best_charger = charger
                                break
                            else:
                                if not charger.queue.full():
                                    # 计算当前充电桩的所需等待的剩余时间
                                    current_charge_car = charger.queue.queue[0]
                                    remain_need_time = self.cal_remain_need_time(current_charge_car, current_time)
                                    if remain_need_time < best_time:
                                        best_time = remain_need_time
                                        best_charger = charger
                    # 如果能放
                    # 将等待区的先来的车放入需要等待时间最少的充电桩队列中
                    if best_charger:
                        best_charger.queue.put(self.fast_wait_area_queue.get())
            else:
                pass
                # print("快充桩现在是满的")

        if not self.slow_wait_area_queue.empty():
            is_all_charger_queue_full = True
            for charger in self.slow_charger:
                if charger.charger_state and not charger.queue.full():
                    is_all_charger_queue_full = False
                    break
            if not is_all_charger_queue_full:
                queue_length = self.slow_wait_area_queue.qsize()
                for i in range(queue_length):
                    # 看哪个快充充电桩有空闲位置并且等待时间最短
                    current_time = time.time()
                    best_charger = None
                    best_time = float('inf')
                    for charger in self.slow_charger:
                        # 先检查充电桩的状态是否是好的
                        if charger.charger_state:
                            # 看充电桩是否正在被使用
                            if not charger.use_state:
                                best_charger = charger
                                break
                            else:
                                if not charger.queue.full():
                                    # 计算当前充电桩的所需等待的剩余时间
                                    current_charge_car = charger.queue.queue[0]
                                    remain_need_time = self.cal_remain_need_time(current_charge_car, current_time)
                                    if remain_need_time < best_time:
                                        best_time = remain_need_time
                                        best_charger = charger
                    # 如果能放
                    # 将等待区的先来的车放入需要等待时间最少的充电桩队列中
                    if best_charger:
                        best_charger.queue.put(self.slow_wait_area_queue.get())
            else:
                pass
        #         print("慢充桩现在是满的")
        # print("调度等待区完成")

    def cal_remain_need_time(self, current_charge_car, current_time):
        # current_charge_car = Car()  # TODO:方便写代码
        # 计算当前正在充电的车的已充电时间, 120为模拟时间比率
        alread_charge_time = (current_time - current_charge_car.start_charge_time) * 120 / 3600
        # 计算剩余需要时间
        remain_need_time = current_charge_car.charge_need_time - alread_charge_time
        return remain_need_time

    def cal_alread_charge_time(self, current_charge_car, current_time):
        alread_charge_time = (current_time - current_charge_car.start_charge_time) * 120 / 3600
        return alread_charge_time

    def is_wait_area_full(self):
        num = self.fast_wait_area_queue.qsize() + self.slow_wait_area_queue.qsize()
        if num == 6:
            return True
        return False

    def update_charger_station(self):
        # print("正在调度充电站")
        # 更新充电区每个充电桩的状态
        # 检查快充的状态
        for item in self.fast_charger:
            # 如果充电桩是空闲状态并且充电桩是好的
            if not item.use_state and item.charger_state:
                # 充电桩的队列中是否有车
                if not item.queue.empty():
                    # 从充电桩的等待队列中选取第一个充电
                    current_car = item.queue.queue[0]
                    # current_car = Car()  # TODO:方便写代码
                    # 记录当前开始充电时间
                    current_car.start_charge_time = time.time()
                    # 计算充电所需要的时间
                    current_car.charge_need_time = current_car.need_power / item.power_per_hour
                    # 更改当前充电桩的充电状态为使用
                    item.use_state = True
            # 需要判断充电结束
            elif item.use_state and item.charger_state:
                current_time = time.time()
                current_car = item.queue.queue[0]
                alread_charge_time = self.cal_alread_charge_time(current_car, current_time)
                # print(f"已经充电{alread_charge_time},总共需要{current_car.charge_need_time}")
                if alread_charge_time >= current_car.charge_need_time:
                    item.total_times += 1
                    item.total_charge_time += current_car.charge_need_time
                    item.total_charge_power += current_car.need_power
                    item.queue.get()
                    # 看队列里有没车
                    if not item.queue.empty():
                        current_car = item.queue.queue[0]
                        current_car.start_charge_time = time.time()
                        current_car.charge_need_time = current_car.need_power / item.power_per_hour
                    else:
                        item.use_state = False
        # 检查慢充的状态
        for item in self.slow_charger:
            # 如果充电桩是空闲状态
            if not item.use_state and item.charger_state:
                # 充电桩的队列中是否有车
                if not item.queue.empty():
                    # 从充电桩的等待队列中选取第一个充电
                    current_car = item.queue.queue[0]
                    # current_car = Car()  # TODO:方便写代码
                    # 记录当前开始充电时间
                    current_car.start_charge_time = time.time()
                    # 计算充电所需要的时间
                    current_car.charge_need_time = current_car.need_power / item.power_per_hour
                    # 更改当前充电桩的充电状态为使用
                    item.use_state = True
            elif item.use_state and item.charger_state:
                current_time = time.time()
                current_car = item.queue.queue[0]
                alread_charge_time = self.cal_alread_charge_time(current_car, current_time)
                # print(f"已经充电{alread_charge_time},总共需要{current_car.charge_need_time}")
                if alread_charge_time >= current_car.charge_need_time:
                    item.total_times += 1
                    item.total_charge_time += current_car.charge_need_time
                    item.total_charge_power += current_car.need_power
                    item.queue.get()
                    # 看队列里有没车
                    if not item.queue.empty():
                        current_car = item.queue.queue[0]
                        current_car.start_charge_time = time.time()
                        current_car.charge_need_time = current_car.need_power / item.power_per_hour
                    else:
                        item.use_state = False

            # print("调度充电站完成")


class SimulateTimer():
    def __init__(self) -> None:
        self.time = {'year': 2023, 'month': 6, 'date': 1, 'hour': 1, 'minute': 0}
        self.timer_flag = True
        self.simulate_time()

    def simulate_time(self):
        self.timer = threading.Timer(0.5, self.update_time)  # 每0.5s模拟1分钟,每30s模拟1小时
        self.timer.start()

    def update_time(self):
        if self.time['minute'] == 59:
            self.time['minute'] = 0
            self.time['hour'] += 1
            if self.time['hour'] == 24:
                self.time['hour'] = 0
                self.time['date'] += 1
                if self.time['month'] in [1, 3, 5, 7, 8, 10, 12]:
                    if self.time['date'] == 32:
                        self.time['date'] = 1
                        self.time['month'] += 1
                    else:
                        self.time['date'] += 1
                elif self.time['month'] in [4, 6, 9, 11]:
                    if self.time['date'] == 31:
                        self.time['date'] = 1
                        self.time['month'] += 1
                    else:
                        self.time['date'] += 1
                else:
                    if self.time['date'] == 29:
                        self.time['date'] = 1
                        self.time['month'] += 1
                    else:
                        self.time['date'] += 1
                if self.time['month'] == 12:
                    self.time['month'] = 1
                    self.time['year'] += 1
                else:
                    self.time['month'] += 1
            else:
                self.time['hour'] += 1
        else:
            self.time['minute'] += 1
        if self.timer_flag:
            self.simulate_time()

    def get_simulate_time(self):
        """
        返回字典类型的时间
        主要用于数据库
        """
        return self.time

    def close_timer(self):
        self.timer_flag = False








            