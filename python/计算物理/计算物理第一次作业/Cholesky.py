from numpy import zeros,ones    #调用zeros,ones函数

def Cholesky(n):                    #定义Cholesky函数，其中n为Hilbert矩阵维数
    H=A=zeros((n,n))
    b=ones(n)
    x=zeros(n)
#生成Hilbert矩阵
    for i in range(0,n):
        for j in range(0,n):
            H[i,j]=1/(i+j+1)

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

for i in range(1,11):
    print(f'n={i}时,x={Cholesky(i)}')


