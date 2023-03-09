from numpy import identity,copy,zeros,sqrt,dot,array

def HouQR(B):
    m=len(B);
    Q=identity(m)
    R=copy(B)
    for i in range(0,m):
        x=zeros(m)
        x[i:m]=R[i:m,i]
        x[i]=x[i]-sqrt(dot(x,x))
        temp=dot(x,x)
        if temp!=0:
            for j in range(0,m):
                Q[j,i:m]=Q[j,i:m]-2*x[i:m]*dot(Q[j,i:m],x[i:m])/temp
            for j in range(i,m):
                R[i:m,j]=R[i:m,j]-2*x[i:m]*dot(R[i:m,j],x[i:m])/temp
    return Q,R

def StandQR(B,k):
    m=len(B)
    Q=identity(m)
    Qbar=Q;R=B
    for i in range(0,k):
        Q,R=HouQR(R.dot(Q))
        Qbar=Q.dot(Qbar)
        if (i+1)%5==0:
            print('第'+str(i+1)+'次迭代矩阵为:'+str(R.dot(Q)))
    return R.dot(Q)[0,0],R.dot(Q)[1,1],R.dot(Q)[2,2],R.dot(Q)[3,3]

B=array([[1,-1,0,0],[-1,2,-1,0],[0,-1,3,-1],[0,0,-1,4]])
print(StandQR(B,30))