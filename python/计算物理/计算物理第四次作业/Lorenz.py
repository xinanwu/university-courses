from numpy import array,zeros
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

r1=array([12,4,0,10,28,5/3])
r2=array([12,4,0,12,28,5/3])
r3=array([12,4,0,10,24,5/3])
r4=array([12,4,0,10,28,2])

def L(t,ini):
    return array([-ini[5]*ini[0]+ini[2]*ini[1],-ini[3]*ini[1]+ini[3]*ini[2],\
                  -ini[1]*ini[0]+ini[4]*ini[1]-ini[2],0,0,0])

def RK4(ini,step,iter,f):
    S=zeros((iter,len(ini)))
    t=zeros(iter)
    S[0,]=ini
    for k in range(iter-1):
        k1=f(t[k],S[k,])
        k2=f(t[k]+step/2,S[k,]+step/2*k1)
        k3=f(t[k]+step/2,S[k,]+step/2*k2)
        k4=f(t[k]+step,S[k,]+step*k3)
        S[k+1,]=S[k,]+(k1+2*k2+2*k3+k4)*step/6
        t[k+1]=t[k]+step
    return S

plt.figure()
N1=RK4(r1,0.001,10000,L)
N2=RK4(r2,0.001,10000,L)
N3=RK4(r3,0.001,10000,L)
N4=RK4(r4,0.001,10000,L)
plt.subplot(221,projection='3d')
plt.plot(N1[:,0],N1[:,1],N1[:,2],linewidth=1,color="red")
plt.subplot(222,projection='3d')
plt.plot(N2[:,0],N2[:,1],N2[:,2],linewidth=1,color="blue")
plt.subplot(223,projection='3d')
plt.plot(N3[:,0],N3[:,1],N3[:,2],linewidth=1,color="green")
plt.subplot(224,projection='3d')
plt.plot(N4[:,0],N4[:,1],N4[:,2],linewidth=1,color="purple")
plt.grid(True)
plt.show()
