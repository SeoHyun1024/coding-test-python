# 2072. 홀수만 더하기

def sum_odd_numbers(input_number):
    sum = 0
    for i in input_number:
        if not i % 2 == 0:
            sum += i
    return sum


T = int(input())  # 변수 입력
input_number = []

for test_case in range(1, T + 1):
    user_input = input().split()  # 공백 기준으로 나눔
    input_number = [int(num) for num in user_input]  # 숫자 저장
    print(f"#{test_case} {sum_odd_numbers(input_number)}")
