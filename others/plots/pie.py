import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

mpl.use('QtAgg')

df = pd.read_csv(r"E:\00_Temp\mpg_ggplot2.csv")
data = df.groupby("class").size().reset_index(name="counts")
print(data)
flg,ax = plt.subplots(figsize=(6,6))
df_count = data["counts"]
df_class = data["class"]
explode = [0 for _ in range(len(df_class))]
explode[4] = 0.1

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    pcts = f"{pct:.1f}%\n({absolute:d})"
    return pcts

wedges, texts, autotexts = ax.pie(df_count,
                                  autopct = lambda pct: func(pct, df_count),
                                  explode = explode,
                                  shadow = False,
                                  startangle = 90,
                                  labels = df_class,
                                  textprops = {"fontsize": 12,"color":"w"},
                                  wedgeprops = {"linewidth": 1,"edgecolor":"w"},
                                  colors=plt.cm.Dark2.colors
                                  )
ax.legend(wedges,
          df_class,
          title="Vehicle Class",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1),
          fancybox=True,
          shadow=True,
          fontsize=12,
          facecolor="lightgray")

plt.setp(autotexts, size=8, weight="bold")
plt.show()