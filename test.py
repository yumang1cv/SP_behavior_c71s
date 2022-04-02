# encoding: utf-8
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from collections import defaultdict
import substring
from tqdm import tqdm
from numba import jit

sys.path.append(os.path.abspath(".."))


# csv_result = []


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


# # explicit function to normalize array
# def normalize_2d(matrix):
#     if matrix.all() != 0:
#         norm = np.linalg.norm(matrix)
#         matrix = matrix / norm  # normalized matrix
#     else:
#         matrix = matrix
#     return matrix

# explicit function to normalize array
def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix

    return matrix


def pre_data(file_path):
    # pre data
    # file_path = csv_FN[0]
    A = np.zeros((14, 14))

    df2 = pd.read_csv(file_path)

    data = df2.iloc[:, 1:2]
    for i in range(1, len(data)):
        if data.iloc[i, 0] != data.iloc[i - 1, 0]:
            a = data.iloc[i, 0] - 1
            b = data.iloc[i - 1, 0] - 1
            A[a, b] = A[a, b] + 1

    class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                  9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

    for line in data.iloc[:, 0]:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict
    behavior_fre = list(class_type.values())
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

    names = ['Running', 'Right turning', 'Left turning', 'Walking', 'Trotting', 'Rearing', 'Sniffing',
             'Grooming', 'Diving', 'Rising', 'Hunching', 'Falling', 'Jumping', 'Stepping']

    color_list = ['#FF6F91', '#FF9671', '#FFC75F', '#FACCFF', '#D65DB1',
                  '#4FFBDF', '#845EC2', '#D5CABD', '#00C2A8', '#008B74',
                  '#77CA9C', '#C4FCEF', '#C34A36', '#BE93FD']
    for item in del_index:
        del names[item]
        del color_list[item]

    return del_data, names, color_list


if __name__ == '__main__':
    a = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
                 name="video_info.xlsx", column="ExperimentTime", element="night")

    # 多条件筛选
    x = choose_data(a, column='gender', element='female')
    df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    # data = df_day.values.tolist()
    csv_FD = []
    for item in tqdm(df_day['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_FD.append(csv_result3[0])

    y = choose_data(a, column='gender', element='male')
    df_night = pd.DataFrame(y, columns=["Unique_serial_number"])
    # data = df_night.values.tolist()
    csv_FN = []
    for item in tqdm(df_night['Unique_serial_number']):
        csv_result4 = search_csv(
            path=r"D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_FN.append(csv_result4[0])

    # file_path = 'D:\\3D_behavior\\Spontaneous_behavior\\result\\BeAMapping\\BeAMapping_replace\\rec-30-G1' \
    #             '-2021114230_Movement_Labels.csv '
    file_path = csv_FN[1]
    # pre data
    # file_path = csv_FN[0]
    A = np.zeros((14, 14))

    df2 = pd.read_csv(file_path)

    data = df2.iloc[:, 1:2]

    for i in range(1, len(data)):
        if data.iloc[i, 0] != data.iloc[i - 1, 0]:
            a = data.iloc[i, 0] - 1
            b = data.iloc[i - 1, 0] - 1
            A[a, b] = A[a, b] + 1

    class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                  9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

    for line in data.iloc[:, 0]:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict
    behavior_fre = list(class_type.values())
    if behavior_fre.count(0) > len(behavior_fre) - 2:
        A = np.zeros((14, 14))
    else:
        A = normalize_2d(A)

    behavior_fre_norm = behavior_fre / np.linalg.norm(behavior_fre)
    for j in range(len(behavior_fre_norm)):
        # A[j, j] = behavior_fre_norm[j]
        A[j, j] = 0
