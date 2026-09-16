def solution(arr, idx):
    new_arr = arr[idx:]
    
    for i in range(len(new_arr)):
        if arr[idx+i] == 1:
            return idx+i
        
    return -1