# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_video.py
# @Time      :2022/4/12 11:58
# @Author    :XuYang
# function   :画出老鼠的三维动态骨架

# import matplotlib
# import matplotlib as mpl
# import pandas as pd
# from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# import seaborn as sns
# matplotlib.use('Qt5Agg')
#
# zuobiao = pd.read_csv('D:/3D_behavior/looming_behavior/looming_video_zhizuo/rec-1-M-20211110105228_Cali_Data3d.csv')
#
# df = zuobiao
# df1 = np.transpose(df[0:len(df)])
#
# def get_data(dataframe, fps_num):
#     for i in range(0, 47, 3):
#         x = np.float64(dataframe.iloc[[i], [fps_num]].values[0][0])
#         y = np.float64(dataframe.iloc[[i + 1], [fps_num]].values[0][0])
#         z = np.float64(dataframe.iloc[[i + 2], [fps_num]].values[0][0])
#
#         a.append(x)
#         b.append(y)
#         c.append(z)
#
#     return a, b, c
#
#
# def point_connnet(list_a, list_b, list_c, x, y):
#     # ax.scatter([list_a[x], list_a[y]], [list_b[x], list_b[y]], [list_c[x], list_c[y]])
#     ax.plot([list_a[x], list_a[y]], [list_b[x], list_b[y]], [list_c[x], list_c[y]], color='black')
#
#     return
#
#
# def plane_vis(list_a, list_b, list_c, x, y, z):
#     vertices = [list(
#         zip([list_a[x], list_a[y], list_a[z]], [list_b[x], list_b[y], list_b[z]], [list_c[x], list_c[y], list_c[z]]))]
#     # poly = Poly3DCollection(vertices, alpha=0.8, edgecolors='blue', facecolors='gray')
#     poly = Poly3DCollection(vertices, alpha=0.8, facecolors='#ececea')
#     ax.add_collection3d(poly)
#
#     return
#
#
# def point_color(list_a, list_b, list_c, point_size):
#     # ax.scatter(list_a[z], list_b[x], list_c[y], c=color, s=point_size)
#
#     ax.scatter(list_a[0:3], list_b[0:3], list_c[0:3], c='goldenrod', s=point_size)  # Nose、Left_ear、Right_ear
#     ax.scatter(list_a[4:12], list_b[4:12], list_c[4:12], c='lightseagreen', s=point_size)  # Limb、Claw
#     ax.scatter(list_a[3:4], list_b[3:4], list_c[3:4], c='crimson', s=point_size)  # Back
#     ax.scatter(list_a[12:16], list_b[12:16], list_c[12:16], c='crimson', s=point_size)  # Tail
#
#     return
#
#
# if __name__ == '__main__':
#     for fps in range(19885, 20410):
#         a = []
#         b = []
#         c = []
#
#         a, b, c = get_data(df1, fps)  # 帧数
#
#         fig = plt.figure(figsize=(5, 5), dpi=300)
#         ax = fig.add_subplot(111, projection='3d')
#
#         plane_vis(a, b, c, 0, 1, 2)
#         plane_vis(a, b, c, 0, 1, 3)
#         plane_vis(a, b, c, 0, 2, 3)
#         plane_vis(a, b, c, 1, 2, 3)
#         plane_vis(a, b, c, 3, 4, 8)
#         plane_vis(a, b, c, 5, 8, 3)
#         plane_vis(a, b, c, 5, 9, 3)
#         plane_vis(a, b, c, 3, 4, 9)
#         plane_vis(a, b, c, 4, 5, 12)
#         plane_vis(a, b, c, 4, 12, 6)
#         plane_vis(a, b, c, 7, 5, 12)
#         plane_vis(a, b, c, 7, 6, 12)
#         plane_vis(a, b, c, 4, 6, 10)
#         plane_vis(a, b, c, 7, 5, 11)
#         plane_vis(a, b, c, 7, 6, 13)
#         # plane_vis(a, b, c, 7, 8, 10)
#
#         point_connnet(a, b, c, 0, 1)  # nose2Lear
#         point_connnet(a, b, c, 0, 2)  # nose2Rear
#         point_connnet(a, b, c, 1, 2)  # Lear2Rear
#         point_connnet(a, b, c, 1, 3)  # Lear2Neck
#         point_connnet(a, b, c, 2, 3)  # Rear2Neck
#         point_connnet(a, b, c, 3, 4)  # Neck2LFLimb
#         point_connnet(a, b, c, 3, 5)  # Neck2RFLimb
#         point_connnet(a, b, c, 4, 8)  # LFLimb2LFClaw
#         point_connnet(a, b, c, 5, 9)  # RFLimb2RFClaw
#         point_connnet(a, b, c, 4, 6)  # LFLimb2LHLimb
#         point_connnet(a, b, c, 5, 7)  # RFLimb2RHLimb
#         point_connnet(a, b, c, 6, 10)  # LHLimb2LHClaw
#         point_connnet(a, b, c, 7, 11)  # RHLimb2RHClaw
#         point_connnet(a, b, c, 6, 13)  # LHLimb2Rtail
#         point_connnet(a, b, c, 7, 13)  # RHLimb2Rtail
#         point_connnet(a, b, c, 14, 13)  # Rtail2Mtail
#         point_connnet(a, b, c, 4, 12)  # LFLimb2Back
#         point_connnet(a, b, c, 5, 12)  # RFLimb2Back
#         point_connnet(a, b, c, 6, 12)  # LHLimb2Back
#         point_connnet(a, b, c, 7, 12)  # RHLimb2Back
#         point_connnet(a, b, c, 14, 15)  # Mtail2Ttail
#         point_color(a, b, c, point_size=100)
#         # ax.scatter(a[0:2], b[0:2], c[0:2], c='#965454', s=5)
#         # plt.axis('off')
#         plt.tick_params(left=False,
#                         bottom=False,
#                         labelleft=False,
#                         labelbottom=False)
#         # plt.grid()
#         # ax.axes.get_xaxis().set_visible(False)
#         # ax.axes.get_yaxis().set_visible(False)
#         plt.rcParams['figure.figsize'] = (5, 5)  # 2.24, 2.24 设置figure_size尺寸
#         plt.show()
#         plt.savefig('D:/3D_behavior/looming_behavior/looming_video_zhizuo/figure/{}.png'.format(fps), dpi=300)
#         plt.close()


import numpy as np
import cv2

size = (1500, 1500)  # 这个是图片的尺寸，一定要和要用的图片size一致
# 完成写入对象的创建，第一个参数是合成之后的视频的名称，第二个参数是可以使用的编码器，第三个参数是帧率即每秒钟展示多少张图片，第四个参数是图片大小信息
videowrite = cv2.VideoWriter(r'D:/3D_behavior/looming_behavior/looming_video_zhizuo/test.mp4', -1, 30, size)  # 20是帧数，size是图片尺寸
img_array = []
for filename in [r'D:/3D_behavior/looming_behavior/looming_video_zhizuo/figure/{0}.png'.format(i) for i in range(19885, 20410)]:  # 这个循环是为了读取所有要用的图片文件
    img = cv2.imread(filename)
    if img is None:
        print(filename + " is error!")
        continue
    img_array.append(img)
for i in range(525):  # 把读取的图片文件写进去
    videowrite.write(img_array[i])
videowrite.release()
print('end!')
