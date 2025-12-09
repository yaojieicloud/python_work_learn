import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt

mpl.use('QtAgg')

delta= 0.0125
x=np.arange(-3.0,3.0,delta)
y=np.arange(-2.0,2.0,delta)
X,Y=np.meshgrid(x,y)
Z1=np.exp(-X**2-Y**2)
Z2=np.exp(-(X-1)**2-(Y-1)**2)
Z=10.0*(Z2-Z1)
fig = plt.figure(figsize=(10, 6),dpi=100)
cs = plt.contour(X,Y,Z,cmap="jet")
plt.clabel(cs, inline=1, fontsize=10)
plt.show()