# -*- coding:utf-8 -*-
# @FileName  :video_test.py
# @Time      :2022/4/12 15:29
# @Author    :XuYang


# import matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# matplotlib.use('Qt5Agg')
#
# fig = plt.figure(figsize=(6, 6))
# ax = plt.gca()
# ax.grid()
# ln1, = ax.plot([], [], '-', lw=2)
# ln2, = ax.plot([], [], '-', color='r', lw=2)
# theta = np.linspace(0, 2 * np.pi, 100)
# r_out = 1
# r_in = 0.5
#
#
# def init():
#     ax.set_xlim(-2, 2)
#     ax.set_ylim(-2, 2)
#     x_out = [r_out * np.cos(theta[i]) for i in range(len(theta))]
#     y_out = [r_out * np.sin(theta[i]) for i in range(len(theta))]
#     ln1.set_data(x_out, y_out)
#     return ln1,
#
#
# def update(i):
#     x_in = [(r_out - r_in) * np.cos(theta[i]) + r_in * np.cos(theta[j]) for j in range(len(theta))]
#     y_in = [(r_out - r_in) * np.sin(theta[i]) + r_in * np.sin(theta[j]) for j in range(len(theta))]
#     ln2.set_data(x_in, y_in)
#     return ln2,
#
#
# ani = animation.FuncAnimation(fig, update, range(len(theta)), init_func=init, interval=50)
# # ani.save('roll.gif', writer='imagemagick', fps=100)
#
# plt.show()

import matplotlib
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# matplotlib.use('Qt5Agg')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
dot, = ax.plot([], [], [], 'b.')


def init():
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(0, 13)
    return 1,


def update_dot(n, x, y, z, dot):
    dot.set_data(x[n], y[n])
    dot.set_3d_properties(z[n], 'z')
    return dot


z = np.linspace(0, 13, 1000)
x = 5 * np.sin(z)
y = 5 * np.cos(z)
ax.plot3D(x, y, z, 'green')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

'''
    函数FuncAnimation(fig,func,frames,init_func,interval,blit)是绘制动图的主要函数，其参数如下：
        a.fig 绘制动图的画布名称
        b.func自定义动画函数，即下边程序定义的函数update
        c.frames动画长度，一次循环包含的帧数，在函数运行时，其值会传递给函数update(n)的形参“n”
        d.init_func自定义开始帧，即传入刚定义的函数init,初始化函数
        e.interval更新频率，以ms计
        f.blit选择更新所有点，还是仅更新产生变化的点。应选择True，但mac用户请选择False，否则无法显
'''
ani = FuncAnimation(fig, update_dot, frames=500, fargs=(x, y, z, dot), interval=20, init_func=init)
# ani.save('sin_dot.gif', writer='pillow')
plt.show()
