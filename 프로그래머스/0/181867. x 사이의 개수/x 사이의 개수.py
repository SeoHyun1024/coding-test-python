def solution(myString):
    answer = myString.strip().split("x")
    answer = [len(s) for s in answer]
    return answer