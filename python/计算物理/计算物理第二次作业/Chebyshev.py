from numpy import zeros
import math
import matplotlib.pyplot as plt
n=20
x=zeros(n)
y=zeros(n)
c=zeros(n)
T=zeros(n)
for i in range(0,n):
    x[i]=math.cos(math.pi*(i+0.5)/n)
    y[i]=1/(1+25*x[i]*x[i])
#待定系数
for i in range(0,n):
    for j in range(0,n):
        c[i]+=y[j]*(math.cos(math.pi*i*(j+0.5)/n))
c=c/n*2
#Chebyshev递推和拟合
def Fit(a,t,c):
    T[0]=1;T[1]=t;s=-c[0]/2
    for i in range(1,n-1):
        T[i+1]=2*t*T[i]-T[i-1]
    for i in range(0,n):
        s+=T[i]*c[i]
    return s
#取点画图
t=zeros(2*n-1)
P=zeros(len(t))
Y=zeros(len(t))
for i in range(0,len(x)-1):
    t[2*i]=x[i]
    t[2*i+1]=(x[i]+x[i+1])/2
t[2*n-2]=x[n-1]
for i in range(0,len(t)):
    Y[i]=1/(1+25*t[i]*t[i])
    P[i]=Fit(n,t[i],c)
print('Chebyshev法插值结果为:'+str(P)+'\n'+'实际结果为:'+str(Y)+'\n'+'误差大小为:'+str(abs(P-Y))+'\n')
plt.figure(figsize=(6,6))
plt.xlim((-1,1))
plt.ylim((-1,2))
plt.plot(t,Y,marker="*",color="red")
plt.plot(t,P,marker="+",color="blue")
plt.plot(t,P-Y,marker="o",color="green")
label = ["Real Curve", "Chebyshev curve","Error curve"]
plt.legend(label, loc ='lower center')
plt.grid(True)
plt.show()