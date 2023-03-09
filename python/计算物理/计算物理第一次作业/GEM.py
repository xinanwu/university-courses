from numpy import zeros      #调用zeros函数
def GEM(n):                       #定义GEM函数，其中n为Hilbert矩阵维数
    H=zeros((n,n+1))
    x=zeros(n)
    #生成Hilbert增广矩阵
    for i in range(0,n):
        H[i,n] = 1
        for j in range(0,n):
            H[i,j]=1/(i+j+1)

    #高斯消元算法
    for j in range(0,n-1):
        m=j
        for i in range(j+1,n):#将第j+1行到第n行元素清零
            for k in range(j,n):#支点遴选
                if abs(H[k,j]) > abs(H[m,j]):
                    m=k
            H[[j,m],:]=H[[m,j],:]
            H[i]=H[i]-H[i,j]/H[j,j]*H[j]
    #反代消元
    for i in range(n-1,-1,-1):
        if H[i,i]!=0:
            x[i] = H[i,n]/H[i,i]
            for j in range(n-1,i,-1):
                x[i]=x[i]-H[i,j]/H[i,i]*x[j]
    return(x)

for i in range(1,11):
    print(f'n={i}时,x={GEM(i)}')