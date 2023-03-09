from numpy import sin,cos

def f(x):
    return (x-2*sin(x))**2

def f1(x):
    return 2*(1-2*cos(x))*(x-2*sin(x))

def Newton_Ralphson(a,e):
    k=0
    y=a
    x=a
    while(abs(f(y)/f1(y))>=e/100):
        y-=f(y)/f1(y)
    while(abs(x-y)>=e):
        print('第'+str(k)+'次迭代时,Newton-Ralphson法的迭代值为'+str(x))
        k+=1
        x-=f(x)/f1(x)
    print('第'+str(k)+'次迭代时,Newton-Ralphson法的迭代值为'+str(x))
    return x,k

print(Newton_Ralphson(1.5,1e-5))