from numpy import zeros,linspace,exp
import matplotlib.pyplot as plt
import numpy.polynomial.legendre as leg

def p(x):
    return 99*(exp(-49.5*x-50.5))/(99*x+101)

def f(x):
    return exp(-x)/x

def Gauss_Legendre(n):
    x,w = leg.leggauss(n)
    s=0
    for i in range(n):
        s+=w[i]*p(x[i])
    return s

def trapezoidal(a,b,n):
    t=linspace(a,b,n)
    s=0
    for i in range(n-1):
        s+=((b-a)/(2*(n-1)))*(f(t[i])+f(t[i+1]))
    return s

def Simpson(a,b,n):
    t=linspace(a,b,n)
    s=0
    for i in range(n-1):
        s+=((b-a)/(6*(n-1)))*(f(t[i])+4*f((t[i]+t[i+1])/2)+f(t[i+1]))
    return s

t=linspace(1,1000,1000)
G=zeros(1000)
T=zeros(1000)
S=zeros(1000)
for i in range(1000):
    G[i]=Gauss_Legendre(i+1)
    T[i]=trapezoidal(1,100,i+1)
    S[i]=Simpson(1,100,i+1)
plt.figure(figsize=(6,6))
plt.xlim((0,1000))
plt.ylim((0.2,0.25))
plt.plot(t,G,linewidth=1.5,color="red")
plt.plot(t,T,linewidth=1.5,color="blue")
plt.plot(t,S,linewidth=1.5,color="green")
label = ["Gauss-Legendre", "Trapezoidal", "Simpson"]
plt.legend(label, loc ='lower center')
plt.grid(True)
plt.show()