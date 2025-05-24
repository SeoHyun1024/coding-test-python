# 18258 큐 2

import sys
from collections import deque


class Queue:
    def __init__(self):  # 초기화
        self.items = deque()

    def push(self, item):   # 삽입
        self.items.append(item)

    def pop(self):  # 삭제
        if not self.is_empty():
            return self.items.popleft()
        return -1

    def is_empty(self): # 빈 큐인지 검사
        return int(len(self.items) == 0)

    def size(self): # 크기
        return len(self.items)

    def front(self):  # 맨 앞 원소 반환
        if not self.is_empty():
            return self.items[0]
        return -1

    def back(self): # 맨 뒤 원소 반
        if not self.is_empty():
            return self.items[-1]
        return -1


queue = Queue()
N = int(sys.stdin.readline())
output = []


def wrap_output(func):
    return lambda: output.append(str(func()))


command_map = {"pop": wrap_output(queue.pop), "empty": wrap_output(queue.is_empty), "size": wrap_output(queue.size),
               "front": wrap_output(queue.front), "back": wrap_output(queue.back), }

for i in range(N):
    command = sys.stdin.readline().split()
    if command[0] == "push":
        queue.push(command[1])
    else:
        action = command_map.get(command[0])
        if action:
            action()

print('\n'.join(output))
