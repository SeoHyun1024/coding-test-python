w, h, b = map(int, input().split(" "))

n = float(w*h*b / 8 / 1024 / 1024)

print(format(n, ".2f"), "MB")
