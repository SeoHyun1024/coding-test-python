n = int(input())
li = input().split()

for i in range(n):
    li[i] = int(li[i])
    
MIN = li[0]

for i in li:
    if i < MIN:
        MIN = i
        
print(MIN)
