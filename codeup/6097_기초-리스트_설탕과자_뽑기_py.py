h, w = map(int, input().split())

matrix = []
for i in range(h+1):
    matrix.append([])
    for j in range(w+1):
        matrix[i].append(0)
        
n = int(input())

for i in range(n):
    l, d, x, y = map(int, input().split(" "))
    
    for j in range(l):
        matrix[x][y] = 1
        
        if d == 0:
            y += 1
        else :
            x += 1

for i in range(1, h+1):
    for j in range(1, w+1):
        print(matrix[i][j], end=" ")
    print()
