from numpy import zeros,sqrt
#delta函数
def delta(i,j):
    if i==j: s=1
    else: s=0
    return s

#生成周期条件的链矩阵并输出，n决定矩阵尺寸
def ChainMatrix(n):
    A=zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            A[i,j]=2*delta(i,j)-delta(i+1,j)-delta(i-1,j)
    A[0,n-1]=-1;A[n-1,0]=-1
    return A

#幂次法求解链矩阵的最大本征值和相应本征矢，k是迭代次数
def Pow(A,k):
    m=len(A)
    q=zeros(m);q[0]=1
    for i in range(0,k):
        z=A.dot(q)
        q=z/sqrt(z.T.dot(z))
        v=q.T.dot(A.dot(q))
    return v,q
print(Pow(ChainMatrix(10),1000))