# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_rose_annoMV.py
# @Time      :2022/9/16 10:28
# @Author    :XuYang
import matplotlib
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
import seaborn as sns

matplotlib.use('Qt5Agg')
movement_index = {'running': 1,
                  'walking': 2,
                  'right_turning': 3,
                  'left_turning': 4,
                  'stepping': 5,
                  'climb_up': 6,
                  'rearing': 7,
                  'hunching': 8,
                  'rising': 9,
                  'grooming': 10,
                  'sniffing': 11,
                  'pause': 12,
                  'jumping': 13,
                  }

color_dict = {'running': '#F44336',
              'walking': '#FF5722',
              'right_turning': '#FFCDD2',
              'left_turning': '#FFAB91',
              'stepping': '#BCAAA4',
              'climb_up': '#43A047',
              'rearing': '#66BB6A',
              'hunching': '#81C784',
              'rising': '#9CCC65',
              'grooming': '#AB47BC',
              'sniffing': '#26A69A',
              'pause': '#B0BEC5',
              'jumping': '#FFB74D',
              }
movement_label = list(movement_index.keys())
color = list(color_dict.values())

time = 'day'

# for item in movement_label:
#     colors = [color_dict['{}'.format(item)]] * 60
#     data = pd.read_excel(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre'
#                          r'\{}_time_single_minute.xlsx'.format(time))
#
#     plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
#     input_data = {'movements': [i for i in range(1, 61)],
#                   'value': data['{}'.format(item)]}
#     pdat = pd.DataFrame(input_data)
#     # print(pdat)
#
#     # 角度
#     l = pdat['value']
#     print(l)
#     N = pdat.shape[0]  # 总数
#     width = 2 * np.pi / N
#     rad = np.cumsum([width] * N)  # 每个扇形的起始角度
#
#     # color
#     # colors = ['darkgoldenrod', 'goldenrod', 'orange', 'gold', 'yellow']
#
#     plt.figure(figsize=(10, 10))  # 创建画布
#     ax = plt.subplot(projection='polar')
#     # 删除不必要的内容
#     ax.set_ylim(-4, np.ceil(l.max() + 1))  # 中间空白
#     ax.set_theta_zero_location('N')  # 设置极坐标的起点（即0度）在正上方向
#     ax.grid(False)  # 不显示极轴
#     ax.spines['polar'].set_visible(False)  # 不显示极坐标最外的圆形
#     ax.set_yticks([])  # 不显示坐标间隔
#     ax.set_thetagrids([])  # 不显示极轴坐标
#     # 绘画
#     ax.bar(rad, l, width=width, color=colors, alpha=1)
#     ax.bar(rad, 5, width=width, color='white', alpha=0.3)  # 中间添加白色色彩使图案变浅
#     ax.bar(rad, 8, width=width, color='white', alpha=0.2)  # 中间添加白色色彩使图案变浅
#     # text
#     # for i in np.arange(N):
#     #     ax.text(rad[i],  # 角度
#     #             l[i] + 1,  # 长度
#     #             input_data['movements'][i],  # 文本
#     #             rotation=rad[i] * 180 / np.pi,  # 文字角度
#     #             rotation_mode='anchor',  # this parameter is a trick
#     #             alpha=1,
#     #             fontweight='bold', size=12
#     #             )
#     plt.tight_layout()
#     plt.show()
#     plt.savefig(
#         r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre\rose\{}_time_{}.tiff'.format(
#             time, item), dpi=300, transparent=True)
#     plt.close()

"""
    line plot
"""

data = pd.read_excel(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre'
                     r'\{}_time_single_minute.xlsx'.format(time))
# fig, ax = plt.subplots()
fig = plt.figure(figsize=(10, 6), dpi=300)
ax = plt.axes()
ax = sns.lineplot(data=data, palette=color, legend=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(1.5)

# plt.colorbar(ax, cax=[0.15, 0.05, 0.7, 0.03], orientation='horizontal')  # 方向
# plt.colorbar(fig, ax=ax, cax=[0.15, 0.05, 0.7, 0.03])
plt.xlabel('Time', fontsize=20)
plt.ylabel('Frequency', fontsize=20)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
plt.show()
plt.savefig(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre\all_behavior.tiff', dpi=300, transparent=True)
plt.close()