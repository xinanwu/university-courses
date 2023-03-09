import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
filename1 = 'Si-K.txt'
pos1 = []
Efield1 = []
with open(filename1, 'r') as file_to_read:
    while True:
        lines = file_to_read.readline() # 整行读取数据
        if not lines:
            break
        pass
        p_tmp, E_tmp = [float(i) for i in lines.split()] 
        pos1.append(p_tmp)  
        Efield1.append(E_tmp)
        pass
    pos1 = np.array(pos1) # 将数据从list类型转换为array类型。
    Efield1 = np.array(Efield1)
filename2 = 'Ti-K.txt'
pos2 = []
Efield2 = []
with open(filename2, 'r') as file_to_read:
    while True:
        lines = file_to_read.readline() # 整行读取数据
        if not lines:
            break
        pass
        p_tmp, E_tmp = [float(i) for i in lines.split()] 
        pos2.append(p_tmp)  
        Efield2.append(E_tmp)
        pass
    pos2 = np.array(pos2) # 将数据从list类型转换为array类型。
    Efield2 = np.array(Efield2)
plt.plot(pos1*10**(9),Efield1,'orange',label='Si-K')
plt.plot(pos2*10**(9),Efield2,'red',label='Ti-K')
plt.xlabel('$Position/nm$')
plt.ylabel('$Counts$')
plt.grid()
plt.legend()
plt.show()