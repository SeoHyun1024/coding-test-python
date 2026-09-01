d = []
d.append([])

for i in range(20):
    d.append([])
    for j in range(20):
        d[i].append(0)
    

for i in range(1, 20):
    s = list(map(int, input().split()))
    for j in range(1, 20):
        d[i][j] = s[j - 1]
    
n = int(input())
for i in range(n):
    x, y = map(int, input().split())
    for j in range(1, 20):
        if d[j][y] == 0:
            d[j][y] = 1
        else :
            d[j][y] = 0
            
        if d[x][j] == 0:
            d[x][j] = 1
        else :
            d[x][j] = 0
    
for i in range(1, 20):
    for j in range(1, 20):
        print(d[i][j], end=" ")
    print()
