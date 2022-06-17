# -*- coding:utf-8 -*-
# @FileName  :safe_area_40_iterate.py
# @Time      :2022/6/15 17:01
# @Author    :XuYang
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import math
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

matplotlib.use('Qt5Agg')


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


def rotate_around_point_highperf(point, radians, origin=(0, 0)):
    """Rotate a point around a given point.

    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    radians = radians / 180 * math.pi
    x_1, y_1 = point
    offset_x, offset_y = origin
    adjusted_x = (x_1 - offset_x)
    adjusted_y = (y_1 - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    return qx, qy


def rotation(dataframe):
    df1 = dataframe.iloc[2:, 36:38]  # select back vector
    df1 = df1.astype(float)
    # df1['back'], df1['back.1'] = rotate_around_point_highperf(df1, 0.3, origin=(0, 0))
    x_max = df1['back'].max()
    # print(df1[df1['back'] == x_max].index.values)
    y1 = df1['back.1'][df1[df1['back'] == x_max].index.values]
    y1 = y1.values[0]
    x_min = df1['back'].min()
    y_max = df1['back.1'].max()
    y_min = df1['back.1'].min()
    x1 = df1['back'][df1[df1['back.1'] == y_min].index.values]
    x1 = x1.values[0]

    L1 = y1 - y_min
    L2 = x_max - x1
    theta = math.atan(L1 / L2) / math.pi * 180

    x_mean = df1['back'].mean()
    y_mean = df1['back.1'].mean()

    df2 = df1.copy()
    for i in range(len(df1)):
        point = [df1['back'].iloc[i], df1['back.1'].iloc[i]]
        df2['back'].iloc[i], df2['back.1'].iloc[i] = rotate_around_point_highperf(point, theta, origin=(0, 0))

    return df2


def normliza_data(data1, data_name=''):
    size = int(len(data1) / 2)
    norm_data = np.array(data1[data_name]).reshape(size, 2)
    scaler = MinMaxScaler(feature_range=(-24, 24))  # 计算圆弧使用
    # scaler = MinMaxScaler(feature_range=(1, 49))  # 计算 50*50 小方格使用
    norm = scaler.fit(norm_data)
    norm_data = scaler.transform(norm_data)
    norm_data = norm_data.reshape(len(data1), 1)

    return norm_data


if __name__ == '__main__':

    file_path = []
    path = r'D:/3D_behavior/Spontaneous_behavior/result_fang/safe_area_test'
    for root, directories, file in os.walk(path):
        for file in file:
            if file.endswith(".csv"):
                # print(os.path.join(root, file))
                file_path.append(os.path.join(root, file))

    all_time = []
    angle_time_all = []
    circle_time_all = []

    location_all = np.zeros((40, 40))
    round_1_all = []
    round_2_all = []
    round_3_all = []
    round_4_all = []
    round_5_all = []
    round_data_all = []

    angle_time = []
    circle_time = []
    for j in range(0, len(file_path)):
        # for j in range(0, 1):
        data = pd.read_csv(file_path[j])

        rotation_data = data

        rotation_data['back'] = data['x']
        rotation_data['back.1'] = data['y']

        data['back_new'] = rotation_data['back']
        data['back.1_new'] = rotation_data['back.1']

        # fig = plt.figure(figsize=(5, 5), dpi=300)
        # ax = fig.add_subplot(111)
        # plt.style.use('ggplot')
        # ax = sns.scatterplot(data=rotation_data, x="back", y="back.1", alpha=0.7)

        """
            迭代统计safe area
        """
        for t in range(1, 29):
            locals()['round_' + str(t)] = 0
        # round_25 = 0

        for i in range(len(rotation_data)):
            for t in range(1, 29):
                if np.square(rotation_data['back'].iloc[i]-20) + np.square(rotation_data['back.1'].iloc[i]-20) <= t * t:
                    locals()['round_' + str(t)] = locals()['round_' + str(t)] + 1

        # for t in reversed(range(2, 58)):
        #     locals()['round_' + str(t)] = (locals()['round_' + str(t)] - locals()['round_' + str(t - 1)]) / (
        #             np.pi * ((t - 1) * 2 + 1))
        #
        # round_1 = round_1 / (np.pi * 1)

        for t in reversed(range(2, 29)):
            locals()['round_' + str(t)] = (locals()['round_' + str(t)] - locals()['round_' + str(t - 1)])

        round_data = []
        for t in range(1, 29):
            round_data.append(locals()['round_' + str(t)])

        print(sum(round_data))

        round_data_all.append(round_data)
        print('第{}个文件已处理'.format(j))

    all_time.append(round_data_all)

    all_time = all_time[0]

    time1 = np.array(all_time).T
    # time_all = time1
    # for i in range(1, 5):
    #     time_all = np.concatenate((time_all, np.array(all_time[i+1]).T), axis=1)


    # round_data_all = np.array(round_data_all).T
    # sns.heatmap(time_all)
    mean_data = []
    for i in range(len(time1)):
        mean_data.append(np.mean(time1[i, :])/30/60)
    x = [i for i in range(1, 29)]
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    plt.plot(x, mean_data)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('Side length of safety area(cm)', fontsize=13)
    plt.ylabel('Exploration duration(min)', fontsize=13)
    plt.tight_layout()
    plt.show()
