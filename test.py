import queue

q = queue.Queue()
q.put(2)
q.put(3)
print(q.queue[0])
q.get()

print(q.queue[0])