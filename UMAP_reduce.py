# -*- coding:utf-8 -*-
# @FileName  :UMAP_reduce.py
# @Time      :2022/9/2 13:45
# @Author    :XuYang
import os
import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')


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
data = pd.read_excel(file_list[2])

pca_data = data.to_numpy()
del_data = np.delete(pca_data, 0, 1)
del_data = del_data[:, 0:13]

reducer = umap.UMAP(n_components=2)
embedding = reducer.fit_transform(del_data)
# plt.scatter(embedding[:, 0], embedding[:, 1])
embedding = pd.DataFrame(embedding)
embedding = embedding.set_axis(['UMAP_1', 'UMAP_2'], axis='columns')
output_data = pd.concat([data, embedding], axis=1)
output_data.to_excel(file_list[2], index=False)
