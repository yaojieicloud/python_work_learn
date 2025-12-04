import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.markers as markers
from matplotlib.lines import Line2D

mpl.use('QtAgg')

df = sns.load_dataset("iris")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lmplot(df, x="sepal_length", y = "sepal_width", hue = "species", legend = False, fit_reg=True,palette="Set2", markers = ["o", "x", "1"])
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()
