def solution(arr):
    result = []
    for i in arr:
        if i >= 50 and i % 2 == 0:
            result.append(i // 2)
        elif i < 50 and i % 2 != 0:
            result.append(i*2)
        else:
            result.append(i)
    return result
        