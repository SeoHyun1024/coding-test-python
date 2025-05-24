# 1206. [S/W 문제해결 기본] 1일차 - View

def count_view_building(building_array, i):
    left_max = max(building_array[i - 2], building_array[i - 1])
    right_max = max(building_array[i + 2], building_array[i + 1])
    view_cnt = min(building_array[i] - left_max, building_array[i] - right_max)
    if view_cnt > 0:
        return view_cnt
    return 0


for _ in range(1, 11):
    N = int(input())  # 변수 입력
    building_array = []
    total_view_cnt = 0
    user_input = input().split()  # 공백 기준으로 나눔
    building_array = [int(num) for num in user_input]  # 숫자 저장
    for i in range(2, N - 2):
        total_view_cnt += count_view_building(building_array, i)

    print(f"#{_} {total_view_cnt}")
