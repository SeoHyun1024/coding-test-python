def solution(n_str):
    for i in range(len(n_str)):
        if n_str[i] == '0':
            continue
        else:
            break
    
    result = n_str[i:]
    
    return result