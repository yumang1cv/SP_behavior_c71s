# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_state_space_annoMV.py
# @Time      :2022/8/31 10:49
# @Author    :XuYang
import pandas as pd
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')
"""
    fang SP behavior Correction-annoMV
    1、Running:[13, 28, 29]        2、Walking:[14, 22]       3、Right turning:[1, 2, 17, 18]
    4、Left turning:[12, 27]       5、Stepping:[5]           6、Climbing up:[25, 31, 32]
    7、Rearing:[16]                8、Hunching:[24]          9、Rising:[8, 34]
    10、Grooming:[15, 37, 40]      11、Sniffing&Walking:[9, 10, 23, 26, 33]
    11、Sniffing:[11, 30, 35, 36, 6, 38, 4, 3]               2、Up looking & walking:[19]
    12、Pause:[20, 21, 39]         13、Jumping:[7]                                     

"""

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

color_list = list(color_dict.values())


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


def pre_data(file_path, movement_label_num, special_time_start, special_time_end):
    with open(file_path, 'rb') as f:
        csv_data = pd.read_csv(f)

    label = csv_data.loc[:, 'movement_label_index']
    segBoundary = csv_data.loc[:, 'segBoundary']

    seg_space_list = []
    seg_before_list = []

    # special_time_end = 27000
    # special_time_start = 0
    # movement_label_num = 15
    for j in range(1, len(segBoundary), 1):
        if segBoundary[j] >= special_time_end > segBoundary[j - 1]:
            stop_num = j

    for k in range(1, len(segBoundary), 1):
        if special_time_start == 0:
            start_num = 0

        elif segBoundary[k] >= special_time_start > segBoundary[k - 1]:
            start_num = k - 1

    for i in range(start_num, stop_num + 1, 1):
        # for i in range(641, 671, 1):
        if label[i] == movement_label_num:
            if i == start_num:
                if i == 0:
                    seg_space = segBoundary[i]
                    seg_space_list.append(seg_space)
                    seg_before = 0
                    seg_before_list.append(seg_before)
                else:
                    # print(i)
                    seg_space = segBoundary[i] - special_time_start
                    seg_space_list.append(seg_space)
                    seg_before = special_time_start
                    seg_before_list.append(seg_before)
                    # print(seg_before_list, seg_space_list)

            elif i == stop_num:
                seg_space = special_time_end - segBoundary[i - 1]
                seg_space_list.append(seg_space)

                seg_before = segBoundary[i - 1]
                seg_before_list.append(seg_before)

            else:
                seg_space = segBoundary[i] - segBoundary[i - 1]
                seg_space_list.append(seg_space)

                seg_before = segBoundary[i - 1]
                seg_before_list.append(seg_before)

    # seg_space_list.remove(seg_space_list[1])
    # seg_before_list.remove(seg_before_list[1])

    # seg_before_list.insert(0, seg_before_list[0])

    x_range_list = []

    for i in range(0, len(seg_before_list), 1):
        x_left = seg_before_list[i] - special_time_start
        x_broken = seg_space_list[i]
        x_range_list.append((x_left, x_broken))

    # seg_before_list.insert(0, seg_before_list[0])

    return x_range_list


def data_combine(file_path, special_time_start, special_time_end):
    # special_time1 = special_time_start * 60 * 30
    # special_time2 = special_time_end * 60 * 30
    special_time1 = special_time_start
    special_time2 = special_time_end
    data = []
    for i in range(1, len(color_list) + 1):
        behavior = pre_data(file_path, i, special_time1, special_time2)
        data.append(behavior)
    return data


if __name__ == '__main__':

    gender = 'male'
    ExperimentTime = 'day'
    Round_time = 3
    camera_type = 'RGB'
    a = read_csv(path=r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new/',
                 name="02_animal_info_square.xlsx", column='camera_type', element=camera_type)

    A = choose_data(a, column='ExperimentTime', element=ExperimentTime)
    B = choose_data(A, column="gender", element=gender)

    C = choose_data(a, column="gender", element='female')
    D = choose_data(C, column='ExperimentTime', element=ExperimentTime)

    df_day = pd.DataFrame(B, columns=["re_seg_Index"]).drop_duplicates()
    data = df_day.values.tolist()

    csv_FD = []
    for item in tqdm(df_day['re_seg_Index']):
        csv_result3 = search_csv(
            path=r"D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new\anno_MV_csv/",
            name="rec-{}-G1-anno_Feature_Space".format(item))
        csv_FD.append(csv_result3[0])

    df_night = pd.DataFrame(D, columns=["re_seg_Index"]).drop_duplicates()
    data = df_night.values.tolist()

    csv_FN = []
    for item in tqdm(df_night['re_seg_Index']):
        csv_result4 = search_csv(
            path=r"D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new\anno_MV_csv/",
            name="rec-{}-G1-anno_Feature_Space".format(item))
        csv_FN.append(csv_result4[0])

    Male_data = []
    for i in range(0, 10):
        single_data = data_combine(csv_FD[i], 0, 18000 * 6 - 10)
        Male_data.append(single_data)
    # single_data = data_combine(file_list_1[0], 0, 25)
    # Male_data.append(single_data)

    Female_data = []
    for i in range(0, 10):
        single_data = data_combine(csv_FN[i], 0, 18000 * 6 - 10)
        # print('第{}个文件sucess'.format(i))
        Female_data.append(single_data)
    #
    # # plt.figure(figsize=(5, 1), dpi=300)
    # fig, ax = plt.subplot()

    fig = plt.figure(figsize=(9, 4), dpi=300)
    ax = fig.add_subplot(111)
    for j in range(len(Male_data)):
        for i in range(len(Male_data[0])):
            plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
            plt.broken_barh(Female_data[j][i], (j + len(Male_data), 0.8), facecolors=color_list[i])

    # for i in range(len(Female_data[6])):
    #     plt.broken_barh(Female_data[6][i], (12, 0.8), facecolors=color_list[i])

    plt.axhline(y=len(Male_data) - 0.1, linewidth=1.5, color='black', linestyle='--')

    # y_tickets = df_day.values.tolist() + df_night.values.tolist()
    # y_tickets = list(np.ravel(y_tickets))

    plt.yticks([len(Male_data) / 2 - 0.1, len(Male_data) + len(Male_data) / 2 - 0.1], ['Males', 'Females'], fontsize=12)
    # plt.yticks([i for i in np.arange(0.4, 24, 1)], y_tickets, fontsize=5)

    # plt.xticks([0, 9000, 18000], ['50', '55', '60'], fontsize=12)
    plt.xticks([i for i in range(0, 18000 * 6 + 1, 9000 * 2)], [i for i in range(0, 61, 5 * 2)], fontsize=12)
    # plt.yticks([])
    plt.tight_layout()
    # plt.axis('off')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.5)
    # plt.ion()
    plt.show()

    plt.savefig(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\state_space/'
                r'{}_all_v2.tiff'.format(ExperimentTime), transparent=True, dpi=300)

    # plt.savefig(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\state_space/'
    #             r'Round{}_all.tiff'.format(Round_time), dpi=300)
    plt.close()
