matrix = []
for i in range(11):
    matrix.append([])
    for j in range(11):
        matrix[i].append(0)
        
for i in range(1, 11):
    s = list(map(int, input().split()))
    for j in range(1, 11):
        matrix[i][j] = s[j-1]
        
x = 2
y = 2

while True:
    if matrix[x][y] == 2:
        matrix[x][y] = 9
        break
    
    matrix[x][y] = 9    # 현재 위치 9로 표시
    
    if x >= 1 and x < 10 and y >= 1 and y < 10:
        if  matrix[x][y+1] != 1:
            y += 1  # 오른쪽으로 이동
                
        elif  matrix[x+1][y] != 1 :
            x += 1  # 아래로 이동
        else :
            break

for i in range(1, 11):
    for j in range(1, 11):
        print(matrix[i][j], end=" ")
    print()
