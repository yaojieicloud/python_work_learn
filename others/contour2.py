import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.tri as tri

mpl.use('QtAgg')

np.random.seed(19680801)
npts = 200
ngridx = 100
ngridy = 200
x = np.random.uniform(-2, 2, npts)
y = np.random.uniform(-2, 2, npts)
z = x * np.exp(-x ** 2 - y ** 2)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

xi = np.linspace(-2.1, 2.1, ngridx)
yi = np.linspace(-2.1, 2.1, ngridy)
triang = tri.Triangulation(x, y)
interpolator = tri.LinearTriInterpolator(triang, z)
Xi,Yi = np.meshgrid(xi, yi)
zi = interpolator(Xi, Yi)

ax1.contour(xi, yi, zi, levels=15,colors="k")
cntr1 = ax1.contourf(xi, yi, zi, cmap="RdBu_r",levels=15)
ax1.clabel(cntr1, inline=1, fontsize=10)
fig.colorbar(cntr1, ax=ax1)

ax2.tricontour(x,y,z,levels=15,colors="k")
cntr2 = ax2.tricontourf(x,y,z,cmap="RdBu_r",levels=15)
fig.colorbar(cntr2, ax=ax2)
ax2.plot(x, y, "ko",ms=2)
ax2.set(xlim=(-2, 2), ylim=(-2, 2))

plt.subplots_adjust(hspace=0.5)
plt.show()