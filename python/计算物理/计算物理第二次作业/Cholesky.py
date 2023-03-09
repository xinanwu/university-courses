from numpy import zeros,array    #调用zeros,array函数

def Cholesky(H,b):                    #定义Cholesky函数，其中n为Hilbert矩阵维数
    n=H.shape[0]
    A=zeros((n,n))
    x=zeros(n)

#Cholesky分解
    for i in range(0,n):
        m=0
        for j in range(0,i):
            if A[j,j]!=0:
                A[i,j]=H[i,j]/A[j,j]
                for k in range(0,j):
                    A[i,j]=A[i,j]-A[j,k]/A[j,j]*A[i,k]
        for j in range(0,i):
            m=m-A[i,j]*A[i,j]      
        A[i,i]=abs(H[i,i]+m)**0.5
    print(A.T)
    #第一步计算Ay=b
    for i in range(0,n):
        if A[i,i]!=0:
            x[i] = b[i]/A[i,i]
            for j in range(0,i):
                x[i]=x[i]-A[i,j]/A[i,i]*x[j]
    #第二步计算A.Tx=y
    for i in range(n-1,-1,-1):
        if A.T[i,i]!=0:
            b[i] = x[i]/A.T[i,i]
            for j in range(n-1,i,-1):
                b[i]=b[i]-A.T[i,j]/A.T[i,i]*b[j]
                
    return b

H=array([[0.05,0.07,0.06,0.05],[0.07,0.10,0.08,0.07],\
            [0.06,0.08,0.10,0.09],[0.05,0.07,0.09,0.10]])
b=array([0.23,0.32,0.33,0.31])
print(Cholesky(H,b))


