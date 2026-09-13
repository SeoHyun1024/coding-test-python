def solution(num_list):
    result = -1
    
    for i in range(len(num_list)):
        if num_list[i] < 0:
            result = i
            break
    return result