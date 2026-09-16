def solution(myString):
    result = myString.split("x")
    result = [s for s in result if s != ""]
    result.sort()

    return result