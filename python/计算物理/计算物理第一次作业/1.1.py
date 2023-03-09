def factorial(number):#定义阶乘函数
    k = 1
    for i in range(number):
        k = k*(i+1)
    return k

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
    
def exp(x):#直接展开法
    s = b = n = 0
    a = 1
    while abs((pow(x,n))/(a)) > pow(10,b)*pow(10,-16):#判断加和项是否影响最后结果确定最高截断项
        s += (pow(x,n))/(a)
        n += 1
        a = factorial(n)
        b = order(abs(s))
    return s

for x in range(0,-110,-10):
    print(f'exp({x})={exp(x)}')