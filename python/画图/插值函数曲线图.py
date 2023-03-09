import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import math
import matplotlib.ticker as ticker
x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

y = np.array([0.2478,0.2473,0.2475,0.2497,0.25,0.2495,0.2488,0.2471,0.2448,0.2496,\
              0.2398,0.2434,0.2501,0.2503,0.2455,0.2467,0.2521,0.2474,0.2432,0.2465])
t=0*x+24.73
#xnew = np.linspace(x.min(),x.max(),300) #300 represents number of points to make between T.min and T.max
#func = interp1d(x,y,kind='cubic')
#ynew = func(xnew)
#plt.plot(xnew,ynew)
plt.xlabel('$N$')
plt.ylabel(r'$d/nm$')
plt.grid()
plt.scatter(x,y,s=15,marker='o',color=(0.1,0.5,0.3),label='Scatter')
plt.plot(x,t,label='Average')
plt.legend()
#print(func(0.62000078),func(0.51506778),func(0.40737338),func(0.320389447),func(0.2637808539),func(0.2223599319))
plt.show()
#plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
#plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.4f'))
#plt.text(2.4,3.1,'$f_{p}=2.145kHz$\n$f_{1}=2.043kHz$\n$f_{2}=2.247kHz$',size = 8,family = "fantasy",style = "italic",bbox = dict(facecolor = "r", alpha = 0.2))