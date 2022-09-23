# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_big_cluster_state_convert_annoMV.py
# @Time      :2022/9/15 17:03
# @Author    :XuYang
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from collections import defaultdict
import substring
from tqdm import tqdm

matplotlib.use('Qt5Agg')
sys.path.append(os.path.abspath(".."))

big_cluster_index = {'Locomotion': 1,
                     'Exploration': 2,
                     'Maintenance': 3,
                     'Inactive': 4
                     }

color_dict = {'Locomotion': '#E6C7BE',
              'Exploration': '#88C5BC',
              'Maintenance': '#AB47BC',
              'Inactive': '#B0BEC5'
              }

color_list = list(color_dict.values())
movement_names = list(big_cluster_index.keys())


def search_csv(path=".", name=""):  # 抓取csv文件
    result = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search_csv(item_path, name)
        elif os.path.isfile(item_path):
            if name + ".csv" == item:
                # global csv_result
                # csv_result.append(name)
                result.append(item_path)
                # print(csv_result)
                # print(item_path + ";", end="")
                # result = item
    return result


def open_data(datapath, file_type):
    file_list = []
    path_list = os.listdir(datapath)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(datapath, filename))

    return file_list


def read_csv(path='.', name="", column="", element=""):
    """
    Unique_serial_number:1,2,...,438          date:20210916
    mouse:#13                                 gender:female/male
    ExperimentTime:day/night                  origin_seg:1,2,3
    re_seg_Index:1,2,...,73                   split_number:1,2,...,6
    coordinate_file:calibrationimages_XY20210916_1
    """
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        df = pd.read_excel(f)

    df1 = df.set_index([column])  # 选取某一列数据
    sel_data = df1.loc[element]  # 根据元素提取特定数据

    return sel_data


def choose_data(dataframe, column="", element=""):
    df = dataframe.loc[dataframe[column].isin([element])]  # 限定条件挑选数据(二次限定使用)

    return df


# explicit function to normalize array
def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix

    return matrix


def pre_data(file_path, start_index):
    # pre data
    # file_path = csv_FN[0]
    A = np.zeros((4, 4))

    df2 = pd.read_csv(file_path)

    data = df2.iloc[(start_index - 1) * 18000 + 1:start_index * 18000, 7:8]

    for i in range(1, len(data)):
        if data.iloc[i, 0] != data.iloc[i - 1, 0]:
            a = data.iloc[i, 0] - 1
            b = data.iloc[i - 1, 0] - 1
            A[a, b] = A[a, b] + 1

    class_type = {1: 0, 2: 0, 3: 0, 4: 0}

    for line in data.iloc[:, 0]:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict
    behavior_fre = list(class_type.values())
    if behavior_fre.count(0) > len(behavior_fre) - 2:
        A = np.zeros((4, 4))
    else:
        A = normalize_2d(A)

    behavior_fre_norm = behavior_fre / np.linalg.norm(behavior_fre)
    for j in range(len(behavior_fre_norm)):
        # A[j, j] = behavior_fre_norm[j]
        A[j, j] = 0

    return A


def del_pre_data(data_list):
    del_index = []
    del_data = data_list
    t = 0
    for i in range(len(del_data)):
        if np.any(del_data[:, [i]]) == 0 and np.any(del_data[[i], :]) == 0:
            # print(i, t, i - t)
            del_index.append(i - t)
            t = t + 1

    for item in del_index:
        del_data = np.delete(del_data, item, 1)
        del_data = np.delete(del_data, item, 0)

    names = movement_names

    color_list_1 = color_list

    for item in del_index:
        del names[item]
        del color_list[item]

    return del_data, names, color_list_1


if __name__ == '__main__':
    # a = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
    #              name="video_info.xlsx", column='gender', element='male')
    #
    # A = choose_data(a, column='ExperimentTime', element='day')
    #
    # # 多条件筛选
    # x = choose_data(A, column='split_number', element=5)  # split_number=1 not have ''
    # df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result3 = search_csv(
    #         path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping-Final\\BeAMapping_replace\\",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FD.append(csv_result3[0])
    #
    # y = choose_data(A, column='split_number', element=6)
    # df_night = pd.DataFrame(y, columns=["Unique_serial_number"])
    # # data = df_night.values.tolist()
    # csv_FN = []
    # for item in tqdm(df_night['Unique_serial_number']):
    #     csv_result4 = search_csv(
    #         path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping-Final\\BeAMapping_replace\\",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FN.append(csv_result4[0])
    #
    # A = 0
    # for item in csv_FD:
    #     a = pre_data(item)
    #     # if not np.isnan(a.all()):
    #     #     # print(a, item)
    #     A = A + a
    # A = A / len(csv_FD)
    #
    # B = 0
    # for item in csv_FN:
    #     b = pre_data(item)
    #     B = B + b
    # B = B / len(csv_FN)
    #
    # # C = np.abs(np.subtract(A, B))
    #
    # del_data, names, colors = del_pre_data(B)
    # color = ListedColormap(colors)
    # fig = plt.figure(figsize=(5, 5), dpi=300)
    # ax = fig.add_subplot(111)
    # # chord_diagram(flux, names, gap=0.03, use_gradient=True, sort='distance', cmap=color,
    # #               chord_colors=colors,
    # #               rotate_names=True, fontcolor="grey", ax=ax, fontsize=10)
    # chord_diagram(del_data, gap=0.03, use_gradient=True, sort='distance', cmap=color,
    #               chord_colors=colors, fontcolor="grey", ax=ax, fontsize=10)
    #
    # # str_grd = "_gradient" if grads[0] else ""
    # plt.tight_layout()
    # plt.show()
    gender = 'female'
    ExperimentTime = 'day'
    # data_a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang/',
    #                   name="video_info.xlsx", column='gender', element=gender)
    data_a = read_csv(path=r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new/',
                      name="02_animal_info_square.xlsx", column='camera_type', element='RGB')
    data_A = choose_data(data_a, column='ExperimentTime', element=ExperimentTime)

    for i in range(1, 2):
        # B = choose_data(data_A, column='roundTime', element=1)

        # 多条件筛选
        x = choose_data(data_A, column='split_number', element=i)  # split_number=1 not have ''
        df_day = pd.DataFrame(x, columns=["re_seg_Index"]).drop_duplicates()
        # data = df_day.values.tolist()
        csv_FD = []
        for item in tqdm(df_day['re_seg_Index']):
            csv_result3 = search_csv(
                path=r"D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new\anno_MV_csv/",
                name="rec-{}-G1-anno_Movement_Labels".format(item))
            csv_FD.append(csv_result3[0])

        A = 0
        for item in csv_FD:
            a = pre_data(item, i)
            # if not np.isnan(a.all()):
            #     # print(a, item)
            A = A + a
        A = A / len(csv_FD)

        # C = np.abs(np.subtract(A, B))

        del_data, names, colors = del_pre_data(A)
        color = ListedColormap(colors)
        fig = plt.figure(figsize=(5, 5), dpi=300)
        ax = fig.add_subplot(111)
        # chord_diagram(flux, names, gap=0.03, use_gradient=True, sort='distance', cmap=color,
        #               chord_colors=colors,
        #               rotate_names=True, fontcolor="grey", ax=ax, fontsize=10)
        chord_diagram(del_data, gap=0.03, use_gradient=True, sort='distance', cmap=color,
                      chord_colors=colors, fontcolor="grey", ax=ax, fontsize=10)

        # str_grd = "_gradient" if grads[0] else ""
        plt.tight_layout()
        plt.show()
        # plt.savefig(
        #     r"D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\state_convert"
        #     "/{}time_{}0~{}0min_big_cluster.tiff".format(ExperimentTime, i - 1, i), transparent=True, dpi=300)
        # # plt.savefig("D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/state_convert/fang_figure"
        # #             "/{}_{}time.tiff".format(gender, ExperimentTime), dpi=300)
        plt.close(fig)
