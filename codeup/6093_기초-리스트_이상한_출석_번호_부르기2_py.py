n = int(input())
li = input().split()

for i in range(n):
    li[i] = int(li[i])
    
for i in range(n-1, -1, -1):
    print(li[i], end=" ")
