from numpy import zeros,linspace
import matplotlib.pyplot as plt
n=21
x=linspace(-1,1,n)
y=zeros(n)

for i in range(0,n):
    y[i]=1/(1+25*x[i]*x[i])
#构造Lagrange多项式函数
def L(x,j,a):
    l=1
    for i in range(0,n):
        if i!=j:
            l*=(x-a[i])/(a[j]-a[i])
    return l
#用Lagrange多项式拟合
def Fit(x,a,b):
    f=0
    for i in range(0,n):
        f+=b[i]*L(x,i,a)
    return f
#选点画图
t=linspace(-1,1,2*n-1)
P=zeros(len(t))
Y=zeros(len(t))
for i in range(0,len(t)):
    P[i]=Fit(t[i],x,y)
    Y[i] =1/(1+25*t[i]*t[i])
print('拉格朗日法插值结果为:'+str(P)+'\n'+'实际结果为:'+str(Y)+'\n'+'误差大小为:'+str(abs(P-Y))+'\n')
plt.figure(figsize=(6,6))
plt.xlim((-1,1))
plt.ylim((-1,2))
plt.plot(t,Y,marker="*",color="red")
plt.plot(t,P,marker="+",color="blue")
plt.plot(t,P-Y,marker="o",color="green")
label = ["Real curve", "Lagrange curve", "Error curve"]
plt.legend(label, loc ='lower center')
plt.grid(True)
plt.show()

