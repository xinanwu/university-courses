from numpy import zeros,array

def p(x,B,i):
    if i==0:
        return 1
    elif i==1:
        return B[0,0]-x
    else:
        return (B[i-1,i-1]-x)*p(x,B,i-1)-((B[i-1,i-2])**2)*p(x,B,i-2)

def s(x):
    s=0
    for i in range(0,4):
        if p(x,B,i)*p(x,B,i+1)<0:
            s+=1
        else:
            s+=0
    return s

def dichotomize(a,b,e,i):
    k=0
    while(k<=e):
        x=(a+b)/2
        if s(x)>len(B)-i:
            b=x
        elif s(x)<=len(B)-i:
            a=x
        else:
            break
        if k%5==0 and k!=0:
            print('i='+str(i)+'时,第'+str(k)+'次迭代后本征值大小为:'+str(x))
        k+=1
    return x

B=array([[1,-1,0,0],[-1,2,-1,0],[0,-1,3,-1],[0,0,-1,4]])
for i in range(1,5):
    print(dichotomize(0,5,30,i))