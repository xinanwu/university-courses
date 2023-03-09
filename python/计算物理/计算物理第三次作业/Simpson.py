from numpy import zeros,linspace,exp
def Simpson(a,b,n):
    t=linspace(a,b,n)
    s=0
    for i in range(n-1):
        s+=((b-a)/(6*(n-1)))*(f(t[i])+4*f((t[i]+t[i+1])/2)+f(t[i+1]))
    return s

def f(x):
    return exp(-x)/x

print('n=10时结果为:'+str(Simpson(1,100,10)))
print('n=100时结果为:'+str(Simpson(1,100,100)))
print('n=1000时结果为:'+str(Simpson(1,100,1000)))
