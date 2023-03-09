from numpy import sin

def f(x):
    return (x-2*sin(x))**2

def Secant(a,b,e):
    k=s=0
    y1=b
    y2=b
    x1=[]
    x2=[]
    x1.append(a)
    x1.append(b)
    x2.append(a)
    x2.append(b)
    while(abs((x2[s+1]-x2[s])*f(x2[s+1])/(f(x2[s+1])-f(x2[s])))>=e/100):
        s+=1
        y2-=(x2[s]-x2[s-1])*f(x2[s])/(f(x2[s])-f(x2[s-1]))
        x2.append(y2)
    while(abs(y1-y2)>=e):
        print('第'+str(k)+'次迭代时,Secant法的迭代值为'+str(y1))
        k+=1
        y1-=(x1[k]-x1[k-1])*f(x1[k])/(f(x1[k])-f(x1[k-1]))
        x1.append(y1)
    print('第'+str(k)+'次迭代时,Secant法的迭代值为'+str(y1))
    return y1,k

print(Secant(1.5,1.7882791003152174,1e-5))