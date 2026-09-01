n = int(input())

for i in range(1, n+1):
    a = i // 10
    b = i % 10
    
    if a > 0:
        if a % 3 == 0 or (b % 3 == 0 and b != 0):
            print("X", end=" ")
        else:
            print(i, end=" ")
    else :
        if b % 3 == 0 and b != 0:
            print("X", end=" ")
        else:
            print(i, end=" ")
