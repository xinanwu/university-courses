import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import math
import matplotlib.ticker as ticker
x1 = np.array([0,
5,
10,
15,
20,
22,
24,
26,
27,
-5,
-10,
-15,
-20,
-22,
-24,
-26,
-27,
-28

])
x2 = np.array([
70,
69,
68,
67,
66,
65,
64,
63,
62,
61,
60,
55,
50,
45,
44,
43,
42,
41,
40,
39,
38,
37,
36,
35,
34,
33,
32,
31,
30])
#x3 = np.array([70,75,80,84])
y1 = np.array([82,
68,
45,
22,
4,
3,
2,
1,
0,
72,
42,
24,
8,
6,
4,
2,
1,
0



])
y2 = np.array([
30,
62,
49,
26,
20,
19,
12,
7,
4,
3,
2,
5,
6,
4,
6,
8,
8,
10,
12,
14,
18,
20,
22,
15,
10,
6,
5,
6,
10])
#y3 = np.array([30,7,4,52])
xnew1 = np.linspace(x1.min(),x1.max(),300) #300 represents number of points to make between T.min and T.max
func1 = interp1d(x1,y1,kind='cubic')
ynew1 = func1(xnew1)
plt.plot(xnew1,ynew1,label='Fit line')
#xnew3 = np.linspace(x3.min(),x3.max(),300) #300 represents number of points to make between T.min and T.max
#func3 = interp1d(x3,y3,kind='cubic')
#ynew3 = func3(xnew3)
#plt.plot(xnew3,ynew3)
#xnew2 = np.linspace(x2.min(),x2.max(),300) #300 represents number of points to make between T.min and T.max
#func2 = interp1d(x2,y2,kind='cubic')
#ynew2 = func2(xnew2)
#plt.plot(xnew2,ynew2)
plt.xlabel('$\theta/^{\circ}$')
plt.ylabel('$I/\mu A$')
plt.grid()
plt.scatter(x1,y1,s=15,marker='x',color=(0.1,0.5,0.3),label='Scatter')
#plt.scatter(x2,y2,s=15,marker='x',color=(0.1,0.5,0.3))
#plt.scatter(x3,y3,s=15,marker='x',color=(0.1,0.5,0.3))
plt.legend(loc=0)
plt.show()
plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.4f'))