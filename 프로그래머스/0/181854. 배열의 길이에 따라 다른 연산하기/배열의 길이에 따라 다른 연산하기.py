def solution(arr, n):
    l = len(arr)
    for i in range(((l+1) % 2),  len(arr), 2):
        arr[i] += n
    return arr