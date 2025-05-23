#10828 스택
import sys

class Stack:
    def __init__(self): # 자동 호출
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return -1

    def is_empty(self):
        return int(len(self.items) == 0)

    def top(self):
        if not self.is_empty():
            return self.items[-1]
        return -1

    def size(self):
        return len(self.items)


N = int(sys.stdin.readline())    # 정수 입력

s = Stack()
output = [] # 출력값 한 번에 표시

def out_wrap(func):
    return lambda : output.append(str(func()))

command_map = {"pop":out_wrap(s.pop), "size": out_wrap(s.size), "empty": out_wrap(s.is_empty), "top":out_wrap(s.top)}


for i in range(N):
    command = sys.stdin.readline().split()
    if command[0] == "push":
        s.push(command[1])
    else:
        action = command_map.get(command[0])
        if action:
            action()

print('\n'.join(output))