from numpy import zeros,linspace
import matplotlib.pyplot as plt

n=21
x=linspace(-1,1,n)
y=zeros(n)
A=zeros((n,n))
a=zeros(n)
for i in range(0,n):
    y[i]=1/(1+25*x[i]*x[i])

for i in range(0,n):
    A[i,0]=1
    for j in range(0,i):
            A[i,j+1]=A[i,j]*(x[i]-x[j])
for i in range(0,n):
    if A[i,i]!=0:
        a[i] = y[i] / A[i, i]
        for j in range(0,i):
            a[i]=a[i]-A[i,j]/A[i,i]*a[j]

def Fit(t,a):
    f=a[n-1]
    for i in reversed(range(0,len(a)-1)):
        f=f*(t-x[i])+a[i]
    return f

t=linspace(-1,1,2*n-1)
P=zeros(2*n-1)
Y=zeros(2*n-1)
for i in range(0,len(t)):
    P[i]=Fit(t[i],a)
    Y[i]=1/(1+25*t[i]*t[i])
print('牛顿法插值结果为:'+str(P)+'\n'+'实际结果为:'+str(Y)+'\n'+'误差大小为:'+str(abs(P-Y))+'\n')
plt.figure(figsize=(6,6))
plt.xlim((-1,1))
plt.ylim((-1,2))
plt.plot(t,Y,marker="*",color="red")
plt.plot(t,P,marker="+",color="blue")
plt.plot(t,P-Y,marker="o",color="green")
label = ["Real Curve", "Newton curve","Error curve"]
plt.legend(label, loc ='lower center')
plt.grid(True)
plt.show()