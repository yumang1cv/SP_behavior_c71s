# -*- coding:utf-8 -*-
# @FileName  :seaborn_scatter.py
# @Time      :2022/9/2 14:16
# @Author    :XuYang
import os
import pandas as pd
import matplotlib
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm  # 导入sklearn包的相应模块
from sklearn.svm import SVC
import sklearn

matplotlib.use('Qt5Agg')

font = {'family': 'Arial',
        'weight': 'normal',
        'size': 13,
        }


def open_data(data_path, file_type):
    file_list = []
    path_list = os.listdir(data_path)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(data_path, filename))

    return file_list


file_list = open_data(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre/',
                      '.xlsx')
file_list = sorted(file_list)

# for item in file_list[0]:
#     data = pd.read_excel(item)
#
#     pca_data = data.to_numpy()
#     del_data = np.delete(pca_data, 0, 1)
# for item in file_list:
data_0 = pd.read_excel(file_list[0])


# data_1 = pd.read_excel(file_list[1])
# data_2 = pd.read_excel(file_list[2])
# data_3 = pd.read_excel(file_list[3])
#
# data_4 = pd.read_excel(file_list[-1])
#
# data_5 = pd.read_excel(file_list[-2])
# data_6 = pd.read_excel(file_list[-3])


def border_of_classifier(sklearn_cl, x, y):
    """
    param sklearn_cl: sklearn的分类器
    param x: np.array
    param y: np.array
    """

    # 1.生成网格数据
    x_min, y_min = x.min(axis=0) - 1
    x_max, y_max = x.max(axis=0) + 1
    # 利用一组网格数据求出方程的值， 然后把边界画出来
    # 生成网格点坐标矩阵。
    x_values, y_values = np.meshgrid(np.arange(x_min, x_max, 0.01),
                                     np.arange(y_min, y_max, 0.01))
    # 计算处分类器对所有数据点的分类姐夫哦，生成网格采样
    mesh_output = sklearn_cl.predict(np.c_[x_values.ravel(), y_values.ravel()])
    mesh_output = mesh_output.reshape(x_values.shape)
    fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
    # 根据mesh_output结果自动从cmap中选择颜色
    plt.pcolormesh(x_values, y_values, mesh_output, cmap='PiYG', alpha=0.8)

    plt.scatter(x[:, 0], x[:, 1], c=y, s=100, linewidth=1, cmap='jet', alpha=0.5)

    plt.xlim(x_values.min(), x_values.max())
    plt.ylim(y_values.min(), y_values.max())
    plt.xticks((np.arange(np.ceil(min(x[:, 0]) - 1), np.ceil(max(x[:, 0]) + 1), 1.0)))
    plt.yticks((np.arange(np.ceil(min(x[:, 1]) - 1), np.ceil(max(x[:, 1]) + 1), 1.0)))
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    plt.show()


if __name__ == '__main__':
    # X1 = data_0.iloc[:, 15:17].values
    # Y1 = data_0.iloc[:, 21:22].values
    #
    # from sklearn.datasets import load_iris
    # from sklearn.tree import DecisionTreeClassifier
    #
    # dtree = DecisionTreeClassifier(max_depth=3)
    # iris = load_iris()
    # x, y = X1, Y1
    # dtree.fit(x, y)
    # # 用决策树方法看特征的重要性
    # dtree.feature_importances_
    #
    # # 画数据点和边界
    # import numpy as np
    # import matplotlib.pyplot as plt
    #
    # plt.style.use('ggplot')
    #
    # # # SVM 支持向量机 惩罚系数
    # # #### 1 观察支持向量机惩罚系数 C
    # # # svc_line1 = SVC(C=0.01, kernel='rbf')
    # # # svc_line2 = SVC(C=5.0, kernel='rbf')
    # # svc_line3 = SVC(C=100.0, kernel='rbf')
    # # # svc_line1.fit(x, y)
    # # # svc_line2.fit(x, y)
    # # svc_line3.fit(x, y)
    # # # border_of_classifier(svc_line1, x, y)
    # # # border_of_classifier(svc_line2, x, y)
    # # border_of_classifier(svc_line3, x, y)

    fig, ax = plt.subplots(figsize=(5, 5), dpi=300)
    ax = sns.scatterplot(data=data_0, x="PCA_1", y="PCA_2", hue='time', palette="deep", sizes=(20, 200), legend=False)
    plt.xticks([])
    plt.yticks([])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.5)  # 设置底部坐标轴的粗细
    ax.spines['left'].set_linewidth(1.5)  # 设置左边坐标轴的粗细
    plt.xlabel('UMAP1', fontdict=font)
    plt.ylabel('UMAP2', fontdict=font)
    # plt.legend(["Day time", "Night time"])
    # plt.savefig(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre/Day-night-UMAP.tiff'
    #             , dpi=300, transparent=True)

