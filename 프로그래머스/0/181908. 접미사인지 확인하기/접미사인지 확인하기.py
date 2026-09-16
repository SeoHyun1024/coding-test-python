def solution(my_string, is_suffix):
    m = len(my_string)
    n = len(is_suffix)
    
    if my_string[m - n:] == is_suffix:
        return 1
    return 0