import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl

mpl.use('QtAgg')

df = sns.load_dataset("iris")
fig,axs = plt.subplots(1,3,figsize=(12,10))
sns.jointplot(x="sepal_length",y="sepal_width",data=df,kind="scatter")
sns.jointplot(x="sepal_length",y="sepal_width",data=df,kind="hex")
sns.jointplot(x="sepal_length",y="sepal_width",data=df,kind="kde")
plt.show()