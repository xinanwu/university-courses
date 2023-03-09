from numpy import exp
import numpy.polynomial.legendre as leg

def p(x):
    return 99*(exp(-49.5*x-50.5))/(99*x+101)

def Gauss_Legendre(n):
    x,w = leg.leggauss(n)
    s=0
    for i in range(n):
        s+=w[i]*p(x[i])
    return s

print('n=10时结果为:'+str(Gauss_Legendre(10)))
print('n=100时结果为:'+str(Gauss_Legendre(100)))