def order(s):#判断位数
    i = 0
    if s >= 1:
        while s/10 > 1:
            s = s/10
            i += 1
        return i
    elif s < 1 and s > 0:
        while s*10 <1:
            s = s*10
            i -= 1
        return i
    elif s == 0:
        return i
    
def exp(x):#递归求倒数法
    s = n = a = b = 1
    while abs(a) > pow(10,b)*pow(10,-16):#判断加和项是否影响最后结果确定最高截断项
        a = -a*x/n
        n += 1
        s += a
        b = order(abs(s))
    return 1/s

for x in range(0,-110,-10):
    print(f'exp({x})={exp(x)}')