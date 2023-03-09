from numpy import sin

def f(x):
    return x-2*sin(x)

def dichotomize(a,b,e):
    k=0
    while(abs(a-b)/2>=e):
        print('第'+str(k)+'次迭代时,二分法的区间为'+str([a,b]))
        k+=1
        x=(a+b)/2
        if f(x)<0:
            a=x
        elif f(x)>0:
            b=x
        else:
            break
    print('第'+str(k)+'次迭代时,二分法的区间为'+str([a,b]))
    return x,k

print(dichotomize(1.5,2,1e-5))