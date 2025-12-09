import seaborn as sns
import matplotlib as mpl
import pandas as pd
import numpy as np
from matplotlib.pyplot import xlabel

import packages.colors.color_builder as cb
from matplotlib import pyplot as plt

mpl.use('QtAgg')

midwest = pd.read_csv(r"E:\00_Temp\midwest_filter.csv")
categories = np.unique(midwest.category)
builder = cb.ColorBuilder()
builder.build_colors("b","g",categories)
colors = builder.all_colors

fig = plt.figure(figsize=(10, 6),dpi=100,facecolor="w",edgecolor='k')
for i,category in enumerate(categories):
    plt.scatter("area","poptotal",data=midwest.loc[midwest.category==category,:],color=colors[i],label=str(category))

plt.gca().set(xlim=(0.0,0.1), ylim=(0,90000),xlabel="Area",ylabel="Population")
plt.title("Midwest Population by Area",fontsize=15)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(loc="upper left",fontsize=10)

plt.show()