def solution(num_list, n):
    result = 0 
    
    for i in num_list:
        if i == n:
            result = 1
    return result 