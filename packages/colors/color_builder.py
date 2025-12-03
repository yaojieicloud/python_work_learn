import matplotlib.colors as colors
import numpy as np
import pandas as pd


class ColorBuilder:
    """
    用于资源生成和管理的颜色构建类。
    ColorBuilder 类用于创建颜色对象并管理其属性，
    方便用户在图形界面、主题构建以及其他需要颜色值的应用中操作颜色。
    """

    def __init__(self):
        """
        控制两个颜色之间过渡效果的类
        该类用于表示从一个颜色逐渐过渡到另一个颜色的渐变效果。
        """
        self.dict_colors = {}
        self.all_colors = []

    def __build_distinct(self, values):
        if not values:
            raise ValueError("values must not be empty")

        dist_values = pd.unique(values)
        return dist_values

    def build_colors(self,start_color,end_color,values):
        """
        生成色阶
        """
        start_color = start_color
        end_color = end_color
        start_rgb = np.array(colors.to_rgb(start_color))
        end_rgb = np.array(colors.to_rgb(end_color))
        colors_count = len(values)
        dist_values =self.__build_distinct(values.tolist())
        dist_colors = [start_rgb + ((end_rgb - start_rgb) / colors_count) * i for i in range(colors_count)]
        self.dict_colors = dict(zip(dist_values, dist_colors))
        self.all_colors = [self.dict_colors[key] for key in values]
