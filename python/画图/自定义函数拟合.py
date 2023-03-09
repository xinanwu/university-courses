import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import numpy as np

#xy数据输入
x = np.array([295.21,
288.38,
283.28,
274.57,
265.60,
257.96,
250.22,
243.08,
234.42,
225.36,
217.67,
210.13,
200.81,
193.34,
186.32,
177.72,
169.37,
162.40,
154.83,
144.93,
133.83,
130.45
])
y = np.array([5.962,
5.719,
5.527,
5.181,
4.883,
4.612,
4.342,
4.103,
3.815,
3.521,
3.270,
3.049,
2.766,
2.522,
2.350,
2.117,
1.880,
1.708,
1.511,
1.223,
0.988,
0.921
])
#指数函数拟合曲线
def func(x,a,b,c):
    return a+b*x+c*x**2
popt, pcov = curve_fit(func, x, y)#训练函数
a=popt[0]
b=popt[1]
c=popt[2]
yvals=func(x,a,b,c)
print(a)
#绘图
plot2=plt.plot(x, yvals, 'r',label='fit line')
plot1=plt.scatter(x, y, marker='x',label='scatter')
plt.xlabel('$\lambda/nm$')
plt.ylabel('$n$')
plt.legend(loc=0)
plt.annotate('$y=a\cdot e^{-bx}$\n$a=2.1848V$\n$b=10.4992m^{-1}$',xy=(110,690),xytext=(125,750),size = 8,\
         family = "fantasy",style = "italic",bbox = dict(facecolor = "r", alpha = 0.2),\
             arrowprops=dict(facecolor='b', shrink=0.02))
plt.grid()
plt.show()