from numpy import sqrt,array,identity,dot

def I(B):
    m=len(B);q=0
    for i in range(1,m):
        for j in range(0,i):
            if B[i,j]==0:
                q=1
            else:
                q=0
                break
    return q

def Find(B):
    m=len(B)
    a=1;b=0;q=0
    for i in range(1,m):
        for j in range(0,i):
            if abs(B[i,j])>abs(q):
                q=B[i,j]
                a=i;b=j
            else:
                q=q
    return array([a,b])

def Givens(B):
    m=len(B)
    a=Find(B)[0];b=Find(B)[1]
    e=(B[b,b]-B[a,a])/(2*B[a,b])
    Q=identity(m)
    if e>=0:
        t=1/(e+sqrt(1+e**2))
        c=1/(sqrt(1+t**2))
        s=c*t
    else:
        t=1/(e-sqrt(1+e**2))
        c=1/(sqrt(1+t**2))
        s=c*t
    Q[a,a]=c;Q[b,b]=c
    Q[a,b]=s;Q[b,a]=-s
    B=dot(Q.T,B).dot(Q)
    return B

def Jacobi(B,k):
    for i in range(k):
        if (i+1)%5==0:
            B=Givens(B)
            print('第'+str(i+1)+'次迭代后矩阵为:'+str(B))
        else:
            B=Givens(B)
    return B[0,0],B[1,1],B[2,2],B[3,3]
B=array([[1,-1,0,0],[-1,2,-1,0],[0,-1,3,-1],[0,0,-1,4]])
print(Jacobi(B,30))