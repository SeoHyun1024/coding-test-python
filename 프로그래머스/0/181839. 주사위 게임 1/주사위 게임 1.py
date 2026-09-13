def solution(a, b):
    if a % 2 == 1 and b % 2 == 1:
        result = a*a + b*b
    elif a % 2 == 1 or b % 2 == 1:
        result = 2*(a+b)
    else:
        result = abs(a-b)
        
    return result
        