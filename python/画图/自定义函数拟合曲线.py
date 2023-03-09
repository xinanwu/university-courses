import numpy as np
import matplotlib.pyplot as plt
filename = '三缝.txt'
pos = []
Efield = []
list1=[]
list2=[]
with open(filename, 'r') as file_to_read:
    while True:
        lines = file_to_read.readline() # 整行读取数据
        if not lines:
            break
        pass
        p_tmp, E_tmp = [float(i) for i in lines.split()] 
        pos.append(p_tmp)  
        Efield.append(E_tmp)
        pass
    pos = np.array(pos) # 将数据从list类型转换为array类型。
    Efield = np.array(Efield)
l=[[] for i in range(100)]
m=361.14
n=29.9066
e=0.00064
c=0.227733
w=0.553067
k=0
g=0
def residual_function(a,d):
    s=0
    i=0
    while i <=13999:
        s+=(Efield[i]-m*(((np.sin(a*(pos[i]-n)))/(a*(pos[i]-n)))**2)*(((np.sin(d*3*(pos[i]-n)))/(np.sin(d*(pos[i]-n))))**2))**2
        i+=1
    return s
while k <=99:
    j=0
    while j <=99:
        l[k].append(residual_function(c+j*e,w+k*e))
        j+=1
    k+=1
while g<=99:
    list1.append(min(l[g]))
    list2.append(l[g].index(min(l[g])))
    g+=1
q=list1.index(min(list1))
p=list2[q]
print(p,q)
x1=np.linspace(0,70,14000)
y1=9*m*(((np.sin((c+p*e)*(x1-n)))/((c+p*e)*(x1-n)))**2)
x2=np.linspace(0,70,14000)
y2=m*(((np.sin((c+p*e)*(x2-n)))/((c+p*e)*(x2-n)))**2)*(((np.sin((w+q*e)*3*(x2-n)))/(np.sin((w+q*e)*(x2-n))))**2)
plt.plot(pos,Efield,'orange')
plt.plot(x2,y2,'black',linestyle='--')
plt.plot(x1,y1,'r',linestyle='--')
plt.xlabel('$\Delta x/mm$')
plt.ylabel('$I$')
plt.grid()
plt.text(57,2880,'x Scatter\n---Fit Line\n---Enveloping Line',size = 8,\
         family = "fantasy",style = "italic",bbox = dict(alpha = 0.2))
plt.show()      
        
        
        
        