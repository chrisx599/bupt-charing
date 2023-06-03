import queue

# 创建一个队列
my_queue = queue.Queue()

# 向队列中添加元素
my_queue.put(1)
my_queue.put(2)
my_queue.put(3)

# 获取队列中的第一个元素但不删除
first_element = my_queue.queue[0]
first_element = 5
print("第一个元素：", first_element)

# 获取队列中的第二个元素但不删除
second_element = my_queue.queue[1]
print("第二个元素：", second_element)
