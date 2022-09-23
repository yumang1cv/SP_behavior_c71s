# -*- coding:utf-8 -*-
# @FileName  :HDF_2csv.py
# @Time      :2022/6/29 11:51
# @Author    :XuYang


import pandas as pd
import numpy as np
import os
from natsort import natsorted
import glob
import h5py

# 读取文件
work_path = r'E:\Ratstress_3D\results\new version-with correction\results7'  # result路径

data_path = natsorted(glob.glob(os.path.join(work_path, 'BeAOutputs', '*_results.h5')))

save_path = os.path.join(work_path, 'BeAOutputs/csv_file_output')
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 准备文件名字
file_dir = r"E:\Ratstress_3D\results\new version-with correction\results7\BeAOutputs"  # BeAOutputs路径
for files in os.walk(file_dir, topdown=False):
    # print(files[2])  # 当前路径下所有非目录子文件
    file_name = files[2]

file_name = natsorted(file_name)

file_rname = []
for i in range(len(file_name)):
    if 'mat' not in file_name[i]:
        file_rname.append(file_name[i])

file_replace = []
for item in file_rname:
    item = item.replace('_results.h5', '')
    file_replace.append(item)

file_rname = file_replace


def feature_space_output(file_path):
    feature_space = pd.DataFrame()

    with h5py.File(file_path, 'r') as f:
        Movement_features = f["Movement_features"]

        movement_label = Movement_features["movement_label"][()].tolist()
        movement_label = list(np.ravel(movement_label))
        movement_label = list(map(int, movement_label))

        segBoundary = Movement_features["segBoundary"][()].tolist()
        segBoundary = list(np.ravel(segBoundary))
        segBoundary = list(map(int, segBoundary))

        umap1 = Movement_features["umap1"][()].tolist()
        umap1 = list(np.ravel(umap1))

        umap2 = Movement_features["umap2"][()].tolist()
        umap2 = list(np.ravel(umap2))

        zs_velocity = Movement_features["zs_velocity"][()].tolist()
        zs_velocity = list(np.ravel(zs_velocity))

    feature_space['movement_label'] = movement_label
    feature_space['segBoundary'] = segBoundary
    feature_space['umap1'] = umap1
    feature_space['umap2'] = umap2
    feature_space['zs_velocity'] = zs_velocity

    return feature_space


def Paras_data_output(file_path):
    with h5py.File(file_path, 'r') as f:
        FrameLevel_paras = f["FrameLevel_paras"]
        Paras_data = FrameLevel_paras['Paras_data'][()]
        Paras_names = FrameLevel_paras['Paras_names'][()]
        Paras_all_data = np.vstack((Paras_names, Paras_data))

    Paras_all_data = pd.DataFrame(Paras_all_data)

    return Paras_all_data


def data3D_output(file_path):
    with h5py.File(file_path, 'r') as f:
        threeD_skeleon = f["3Dskeleton"]
        data3D = threeD_skeleon['data3D'][()]
    data3D = pd.DataFrame(data3D)

    return data3D


def movement_to_csv(data1):
    # data1 = pd.read_csv(file_path)
    movement_label = data1['movement_label'].values.tolist()
    segBoundary = data1['segBoundary'].values.tolist()
    segBoundary.insert(0, 0)

    movements_all = []
    for i in range(1, len(segBoundary), 1):
        movements_single = []
        movements_single = [movement_label[i - 1]] * (segBoundary[i] - segBoundary[i - 1])
        movements_all = movements_all + movements_single

    movements_all = pd.DataFrame(movements_all)

    return movements_all


if __name__ == '__main__':
    for i in range(len(data_path)):
        data3D_1 = data3D_output(data_path[i])
        data3D_1.to_csv('{}/{}_Cali_Data3d.csv'.format(save_path, file_rname[i]), index=False)

        feature_space_1 = feature_space_output(data_path[i])
        feature_space_1.to_csv('{}/{}_Feature_Space.csv'.format(save_path, file_rname[i]), index=False)

        movement_label_1 = movement_to_csv(feature_space_1)
        movement_label_1.to_csv('{}/{}_Movement_Labels.csv'.format(save_path, file_rname[i]), header=False, index=False)

        Paras_all_data_1 = Paras_data_output(data_path[i])
        Paras_all_data_1.to_csv('{}/{}_Paras.csv'.format(save_path, file_rname[i]), index=False)

        print('第{}个文件已生成, 还有{}文件待生成'.format(i + 1, len(data_path)-i-1))
