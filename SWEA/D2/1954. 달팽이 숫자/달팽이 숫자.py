# 1954. 달팽이 숫자

def snail(n):
    arr = [[0] * n for _ in range(n)]  # 배열 초기화
    visited = [[0] * n for _ in range(n)]  # 방문 배열 초기화

    dx = [0, 1, 0, -1]  # 방향 배열
    dy = [1, 0, -1, 0]

    x, y = 0, 0
    dir = 0
    num = 1

    for _ in range(n * n):
        arr[x][y] = num
        visited[x][y] = 1

        num += 1

        nx = x + dx[dir]
        ny = y + dy[dir]

        if nx >= n or nx < 0 or ny >= n or ny < 0 or visited[nx][ny] == 1:
            dir = (dir + 1) % 4
            nx = x + dx[dir]
            ny = y + dy[dir]

        x, y = nx, ny

    return arr


T = int(input())
for _ in range(T):
    # 배열 출력
    N = int(input())

    result = snail(N)

    print(f"#{_+1}")
    for i in range(N):
        for j in range(N):
            print(result[i][j], end=" ")
        print('\n', end="")
