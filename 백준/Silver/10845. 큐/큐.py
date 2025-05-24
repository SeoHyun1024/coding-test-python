# 10845 큐

import sys


class Queue:
    def __init__(self):  # 초기화
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop(0)
        return -1

    def is_empty(self):
        return int(len(self.items) == 0)

    def size(self):
        return len(self.items)

    def front(self):
        if not self.is_empty():
            return self.items[0]
        return -1

    def back(self):
        if not self.is_empty():
            return self.items[self.size() - 1]
        return -1


queue = Queue()
N = int(sys.stdin.readline())
output = []


def wrap_output(func):
    return lambda: print(str(func()))


command_map = {"pop": wrap_output(queue.pop), "empty": wrap_output(queue.is_empty), "size": wrap_output(queue.size),
               "front": wrap_output(queue.front), "back": wrap_output(queue.back), }

for i in range(N):
    command = sys.stdin.readline().split()
    if command[0] == "push":
        queue.push(command[1])
    else:
        action = command_map.get(command[0])
        if action :
            action()

print('\n'.join(output))