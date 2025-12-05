import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.markers as markers
from matplotlib.lines import Line2D

# mpl.use('QtAgg')

df = pd.read_csv(r"E:\00_Temp\mpg_ggplot2.csv")

fig, ax = plt.subplots(figsize=(12, 6),dpi=100)
sns.stripplot(x="cty", y="hwy",hue="class", data=df, jitter=0.5,ax=ax, size=6, palette="Set2", linewidth=0.5)
plt.title("MPG by City and Class")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()
