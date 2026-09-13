def solution(arr):
    result = []
    
    for i in arr:
        for j in range(i):
            result.append(i)
    return result