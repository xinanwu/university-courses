from numpy import zeros
import math
import matplotlib.pyplot as plt
n=9
p=zeros(n)
Ax=zeros(n)
Ay=zeros(n)
x=zeros(n)
Bx=zeros(n)
By=zeros(n)
y=zeros(n)
Mx=zeros(n)
My=zeros(n)

#Cardioid曲线
for i in range(0,n):
    p[i]=math.pi*i/4
    y[i]=math.sin(p[i])*(1-math.cos(p[i]))
    x[i]=math.cos(p[i])*(1-math.cos(p[i]))
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
Mx=solveM(p,x)
My=solveM(p,y)
pp=zeros(91)
Px=zeros(len(pp))
Py=zeros(len(pp))
Y=zeros(len(pp))
X=zeros(len(pp))
for i in range(0,len(pp)):
    pp[i]=2*math.pi*i/(len(pp)-1)
    Y[i]=math.sin(pp[i])*(1-math.cos(pp[i]))
    X[i]=math.cos(pp[i])*(1-math.cos(pp[i]))
for i in range(0,n-1):
    Ax[i]=((x[i+1]-x[i])/(p[i+1]-p[i])-(p[i+1]-p[i])*(Mx[i+1]-Mx[i])/6)*(math.pi)/4
    Ay[i]=((y[i+1]-y[i])/(p[i+1]-p[i])-(p[i+1]-p[i])*(My[i+1]-My[i])/6)*(math.pi)/4
    Bx[i]=x[i]-Mx[i]*(p[i+1]-p[i])*(p[i+1]-p[i])/6
    By[i]=y[i]-My[i]*(p[i+1]-p[i])*(p[i+1]-p[i])/6
    for k in range(math.ceil(len(pp)/(len(p)-1)*i), math.ceil(len(pp)/(len(p)-1)*(i+1))):
        Px[k]=Fit(i,pp[k],p,x,Mx)
        Py[k]=Fit(i,pp[k],p,y,My)
print('\n'+r'$S_{\Delta}$(x;t)')
for j in range(8):
    print(r'$%d\leq t\leq %d$:'%(j,j+1))
    print(r'$%.8f\cdot (t-%d)^3+%.8f\cdot(t-%d)^3+%.8f\cdot(t-%d)+%.8f$'\
          %(-(Mx[j]/(6*(p[j+1]-p[j]))*((math.pi)/4)**3), j+1, (Mx[j+1]/(6*(p[j+1]-p[j]))*((math.pi)/4)**3), j, Ax[j], j, Bx[j]))
print(r'$S_{\Delta}$(y;t):')
for j in range(8):
    print(r'$%d\leq t\leq %d$:'%(j,j+1))
    print(r'$%.8f\cdot (t-%d)^3+%.8f\cdot(t-%d)^3+%.8f\cdot(t-%d)+%.8f$'\
          %(-(My[j]/(6*(p[j+1]-p[j]))*((math.pi)/4)**3), j+1, (My[j+1]/(6*(p[j+1]-p[j]))*((math.pi)/4)**3), j, Ay[j], j, By[j]))
plt.figure(figsize=(6,6))
plt.xlim((-3,1))
plt.ylim((-2,2))
plt.plot(x,y,'ro',color="green")
plt.plot(X,Y,color="red")
plt.plot(Px,Py,color="blue")
label=["Sample Point","Real Curve", "Spline3 curve"]
plt.legend(label, loc ='lower left')
plt.grid(True)
plt.show()