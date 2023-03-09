import colour
import matplotlib.pyplot as plt

[x1,y1]=[0.1049,0.1363]
[x2,y2]=[0.1342,0.0596]
[x3,y3]=[0.0850,0.2087]
[x4,y4]=[0.1166,0.1028]
[x5,y5]=[0.0733,0.2580]
[x6,y6]=[0.0565,0.3687]
colour.plotting.plot_chromaticity_diagram_CIE1931(standalone=False)  
plt.plot(x1,y1,'o',markersize=9,color=(0.1,0.1,0.7))  # 绘图
plt.plot(x2,y2,'o',markersize=9,color=(0.1,0.1,0.7))
plt.plot(x3,y3,'o',markersize=9,color=(0.1,0.1,0.7))
plt.plot(x4,y4,'o',markersize=9,color=(0.1,0.1,0.7))
plt.plot(x5,y5,'o',markersize=9,color=(0.1,0.1,0.7))
plt.plot(x6,y6,'o',markersize=9,color=(0.1,0.1,0.7))
plt.axis([-0.1, 1, -0.1, 1])    #改变坐标轴范围
plt.show()
