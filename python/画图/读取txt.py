import numpy as np
import matplotlib.pyplot as plt
filename = '双缝.txt'
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
s=0
for i in pos and j in Efield:
    s+=i+j
print(s)