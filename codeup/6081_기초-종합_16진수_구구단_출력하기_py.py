c = int(input(), 16)

for i in range(1, 16):
    print('%X'%c, '*%X'%i, '=%X'%(c*i), sep='')
