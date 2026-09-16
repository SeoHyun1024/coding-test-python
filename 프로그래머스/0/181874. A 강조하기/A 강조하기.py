def solution(myString):
    result = ''
    for i in myString:
        if i == 'a':
            result += 'A'
        elif i != 'A' and i.isupper():
            result += i.lower()
        else:
            result += i
    return result