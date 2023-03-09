#线性回归
import numpy as np # 快速操作结构数组的工具
import matplotlib.pyplot as plt  # 可视化绘制
from sklearn.linear_model import LinearRegression  # 线性回归
import math

# 样本数据集，第一列为x，第二列为y，在x和y之间建立回归模型
data1=[[19.1182,-0.129],[20.9455,-0.1308],[23.4755,-0.1348],[25.7947,-0.1381],[28.3248,-0.1418],[30.644,-0.1458]]
#data2=[[1/60,60.71],[1/55,66.23],[1/50,74.18],[1/45,83.42],[1/40,91.7],[1/35,105.3],[1/30,123.9]] 
#生成X和y矩阵
dataMat1 = np.array(data1)
x1 = dataMat1[:,0:1]   # 变量x
y1 = dataMat1[:,1]   #变量y
 
# ========线性回归========
model1 = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
model1.fit(x1, y1)   # 线性回归建模

# 使用模型预测
predicted1 = model1.predict(x1)
 
# 绘制散点图 参数：x横轴 y纵轴
a1=plt.scatter(x1, y1, marker='x',label='scatter')
b1=plt.plot(x1, predicted1,c='r',label='fit line')

#生成X和y矩阵
#dataMat2 = np.array(data2)
#x2 = dataMat2[:,0:1]   # 变量x
#y2 = dataMat2[:,1]   #变量y
 
# ========线性回归========
#model2 = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
#model2.fit(x2, y2)   # 线性回归建模

# 使用模型预测
#predicted2 = model2.predict(x2)
 
# 绘制散点图 参数：x横轴 y纵轴
#a2=plt.scatter(x2, y2, marker='x',label='scatter2')
#b2=plt.plot(x2, predicted2,c='r',label='fit line2')
# 绘制x轴和y轴坐标
plt.xlabel(r'$t/s$')
plt.ylabel(r'$T/K$')
plt.legend(loc=0,ncol=1)
plt.text(28.6,-0.1325,'$\lambda=0.001468K/s $\n$r=0.9985$',size = 8,\
         family = "fantasy",style = "italic",bbox = dict(facecolor = "r", alpha = 0.2))
plt.grid()
# 显示图形
plt.show()