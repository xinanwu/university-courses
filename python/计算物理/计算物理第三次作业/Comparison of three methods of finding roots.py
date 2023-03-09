from numpy import sin,cos,log10,zeros,linspace
from scipy.optimize import root   #为了求得精确解作比较
import matplotlib.pyplot as plt

def f(x):
    return x-2*sin(x)

def f1(x):
    return 1-2*cos(x)

def Newton_Ralphson(a,e):
    k=0
    x=a
    while(k<e):
        if abs(f(x)/f1(x))>1e-16:
            k+=1
            x-=f(x)/f1(x)
        else:
            return x
    return x

def Secant(a,b,e):
    k=0
    y=b
    x=[]
    x.append(a)
    x.append(b)
    while(k<e):
        if k<=6:
            k+=1
            y-=(x[k]-x[k-1])*f(x[k])/(f(x[k])-f(x[k-1]))
            x.append(y)
        else:
            k+=1
            x.append(y)
    return y

def dichotomize(a,b,e):
    k=0
    while(k<e):
        k+=1
        x=(a+b)/2
        if f(x)<0:
            a=x
        elif f(x)>0:
            b=x
        else:
            break
    return x

z=(root(f,1.8)).x     #用root函数求得的值作为精确解计算相对误差
t=linspace(1,50,50)
N=zeros(50)
D=zeros(50)
S=zeros(50)
for i in range(50):
    N[i]=log10(abs((Newton_Ralphson(1.5,i+1)-z)/z)+1e-16)
    D[i]=log10(abs((dichotomize(1.5,2,i+1)-z)/z)+1e-16)
    S[i]=log10(abs((Secant(1.5,2.076558200630435,i+1)-z)/z)+1e-16)
plt.figure(figsize=(6,6))
plt.xlim((0,50))
plt.ylim((-17,0))
plt.plot(t,N,linewidth=2,color="red")
plt.plot(t,D,linewidth=2,color="blue")
plt.plot(t,S,linewidth=2,color="green")
label = ["Newton-Ralphson", "Dichotomize", "Secant"]
plt.legend(label, loc ='upper center')
plt.grid(True)
plt.show()