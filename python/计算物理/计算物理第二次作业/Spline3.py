from numpy import linspace,zeros
import math
import matplotlib.pyplot as plt
n=21
x=linspace(-1,1,n)
y=zeros(n)
N=zeros(n)
#Runge函数
for i in range(0,n):
    y[i]=1/(1+25*x[i]*x[i])
#自然三次样条插值
def solveM(x,y):
    h = zeros(n)
    b = zeros(n)
    L = zeros((n, n))
    U = zeros((n, n))
    M = zeros(n)
    v = zeros(n)
    for i in range(0,n-1):
        h[i]=x[i+1]-x[i]
        b[i]=(y[i+1]-y[i])/h[i]*6
    U[1,1]=2*(h[1]+h[0])
#分解插值矩阵
    for i in range(1,n-1):
        L[i,i]=1
        v[i]=b[i]-b[i-1]
        if i!=n-2:
            L[i+1,i]=h[i]/U[i,i]
            U[i+1,i+1]=2*(h[i+1]+h[i])-h[i]/U[i,i]*h[i]
            U[i,i+1]=h[i]
#回带求解插值系数
    for i in range(1,n-1):
        b[i]=v[i]
        b[i]=b[i]-L[i,i-1]*b[i-1]
    for i in reversed(range(1,n-1)):
        if U[i,i]!=0:
            M[i]=b[i]/U[i,i]
            M[i]=M[i]-U[i,i+1]/U[i,i]*M[i+1]
    return M

#计算分段插值函数
def Fit(r,t,x,y,M):
    A=(y[r+1]-y[r])/(x[r+1]-x[r])-(x[r+1]-x[r])*(M[r+1]-M[r])/6
    B=y[r]-M[r]*(x[r+1]-x[r])*(x[r+1]-x[r])/6
    S=A*(t-x[r])+B+M[r]/(x[r+1]-x[r])*pow(x[r+1]-t,3)/6+M[r+1]/(x[r+1]-x[r])*pow(t-x[r],3)/6
    return S
#取点画图
N=solveM(x,y)
t=linspace(-1,1,41)
P=zeros(len(t))
Y=zeros(len(t))
for i in range(0,n-1):
    for k in range(math.ceil(len(t)/(len(x)-1)*i), math.ceil(len(t)/(len(x)-1)*(i+1))):
        P[k]=Fit(i,t[k],x,y,N)
for i in range(0,len(t)):
    Y[i] =1/(1+25*t[i]*t[i])
print('三次样条函数插值结果为:'+str(P)+'\n'+'实际结果为:'+str(Y)+'\n'+'误差大小为:'+str(abs(P-Y))+'\n')
plt.figure(figsize=(6,6))
plt.xlim((-1,1))
plt.ylim((-1,2))
plt.plot(t,Y,marker="*",color="red")
plt.plot(t,P,marker="+",color="blue")
plt.plot(t,P-Y,marker="o",color="green")
label = ["Real Curve", "Spline3 curve","Error curve"]
plt.legend(label, loc ='lower center')
plt.grid(True)
plt.show()