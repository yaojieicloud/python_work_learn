import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch

mpl.use('QtAgg')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.subplots_adjust(wspace=0.5)

overall_ratios = [0.27, 0.56, 0.17]
labels = ["A", "B", "C"]
explode = [0.1, 0, 0]
angle = -180 * overall_ratios[0]
wedges, texts, autotexts = ax1.pie(overall_ratios,
                                   explode=explode,
                                   labels=labels,
                                   autopct="%1.1f%%",
                                   startangle=angle)

age_ratios = [0.33, 0.54, 0.07, 0.06]
age_labels = ["Under 35", "35-49", "50-65", "Over 65"]
bottom = 1
width = 0.2

for j, (height, lable) in enumerate(reversed([*zip(age_ratios, age_labels)])):
    bottom -= height
    bc =ax2.bar(0,
            height,
            width,
            color="C0",
            alpha=0.1 + 0.25 * j,
            bottom=bottom,
            label=lable)

    ax2.bar_label(bc,
                  labels = [f"{height:.0%}"],
                  label_type="center",
                  padding=3)

ax2.set_title("Age Distribution")
ax2.legend()
ax2.axis("off")
ax2.set_xlim(-2.5*width, 2.5*width)

theta1,theta2 = wedges[0].theta1,wedges[0].theta2
center,r = wedges[0].center,wedges[0].r
bar_height = sum(age_ratios)

x=r*np.cos(np.pi/180 * theta2) + center[0]
y=r*np.sin(np.pi/180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width/2,bar_height),coordsA=ax2.transData,xyB=(x,y),coordsB=ax1.transData)
con.set_linewidth(2)
con.set_color([0,0,0])
ax2.add_artist(con)



plt.show()
