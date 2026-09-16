def solution(arr1, arr2):
    n = len(arr1)
    m = len(arr2)
    if n == m:
        n = sum(arr1)
        m = sum(arr2)
    
    if n > m:
        return 1
    elif n < m:
        return -1
    else:
        return 0