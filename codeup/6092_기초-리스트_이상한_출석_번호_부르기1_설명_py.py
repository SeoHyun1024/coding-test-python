n = int(input())
li = input().split()

for i in range(n):
    li[i] = int(li[i])
    
d = []
for i in range(24): # 빈 리스트 생성
    d.append(0)
    
for i in range(n):
    d[li[i]] += 1
    
for i in range(1, 24):
    print(d[i], end=' ')
