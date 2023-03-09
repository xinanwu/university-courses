from numpy import zeros,linspace
import matplotlib.pyplot as plt
n=21
x=linspace(-1,1,n)
y=zeros(n)
T=zeros((n,n))
for i in range(0,n):
    y[i]=1/(1+25*x[i]*x[i])

def Fit(r,x,y):
    for j in range(0,n):
        T[j,0]=y[j]
        for k in range(1,j+1):
            T[j,k]=((r-x[j-k])*T[j,k-1]-(r-x[j])*T[j-1,k-1])/(x[j]-x[j-k])
    return T[n-1,n-1]
#选点画图
t=linspace(-1,1,2*n-1)
P=zeros(len(t))
Y=zeros(len(t))
for i in range(0,len(t)):
    P[i]=Fit(t[i],x,y)
    Y[i] =1/(1+25*t[i]*t[i])
print('Neville法插值结果为:'+str(P)+'\n'+'实际结果为:'+str(Y)+'\n'+'误差大小为:'+str(abs(P-Y))+'\n')
plt.figure(figsize=(6,6))
plt.xlim((-1,1))
plt.ylim((-1,2))
plt.plot(t,Y,marker="*",color="red")
plt.plot(t,P,marker="+",color="blue")
plt.plot(t,P-Y,marker="o",color="green")
label = ["Real curve", "Neville curve", "Error curve"]
plt.legend(label, loc ='lower center')
plt.grid(True)
plt.show()


