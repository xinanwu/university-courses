from numpy import zeros,array      #调用zeros,array函数
def GEM(A):#定义GEM函数，其中n为A矩阵维数,A为线性方程组增广矩阵
    n=A.shape[0]
    x=zeros(n)

    #高斯消元算法
    for j in range(0,n-1):
        m=j
        for i in range(j+1,n):#将第j+1行到第n行元素清零
            for k in range(j,n):#支点遴选
                if abs(A[k,j]) > abs(A[m,j]):
                    m=k
            A[[j,m],:]=A[[m,j],:]
            A[i]=A[i]-A[i,j]/A[j,j]*A[j]
    #反代消元
    for i in range(n-1,-1,-1):
        if A[i,i]!=0:
            x[i] = A[i,n]/A[i,i]
            for j in range(n-1,i,-1):
                x[i]=x[i]-A[i,j]/A[i,i]*x[j]
    return(x)
A=array([[0.05,0.07,0.06,0.05,0.23],[0.07,0.10,0.08,0.07,0.32],\
            [0.06,0.08,0.10,0.09,0.33],[0.05,0.07,0.09,0.10,0.31]])
print(GEM(A))