import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
filename = '单缝.txt'
pos = []
Efield = []
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
x1=np.linspace(0,20,4000)
y1=3248.8*(((np.sin(0.854967*(x1-7.4426)))/(0.854967*(x1-7.4426)))**2)
plt.plot(pos,Efield,'orange')
plt.plot(x1,y1,'r',linestyle='--')
plt.xlabel('$\Delta x/mm$')
plt.ylabel('$I$')
plt.grid()
plt.text(17.5,3050,'x  Scatter\n---  Fit Line',size = 8,\
         family = "fantasy",style = "italic",bbox = dict(alpha = 0.2))
plt.show()
x2=np.linspace(0,70,14000)
y2=361.14*(((np.sin(0.2652*(x2-29.9066)))/(0.2652*(x2-29.9066)))**2)*(((np.sin(0.5933*3*(x2-29.9066)))/(np.sin(0.5933*(x2-29.9066))))**2)
plt.plot(x2,y2,'black',linestyle='--')