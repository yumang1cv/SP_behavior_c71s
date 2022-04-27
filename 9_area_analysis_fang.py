# -*- coding:utf-8 -*-
# @FileName  :9_area_analysis_fang.py
# @Time      :2022/4/26 10:07
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
    df1 = dataframe.iloc[2:, 5:7]  # select back vector
    df1 = df1.astype(float)
    # df1['back'], df1['back.1'] = rotate_around_point_highperf(df1, 0.3, origin=(0, 0))
    x_max = df1['x'].max()
    # print(df1[df1['back'] == x_max].index.values)
    y1 = df1['y'][df1[df1['x'] == x_max].index.values]
    y1 = y1.values[0]
    x_min = df1['x'].min()
    y_max = df1['y'].max()
    y_min = df1['y'].min()
    x1 = df1['x'][df1[df1['y'] == y_min].index.values]
    x1 = x1.values[0]

    L1 = y1 - y_min
    L2 = x_max - x1
    theta = math.atan(L1 / L2) / math.pi * 180

    x_mean = df1['x'].mean()
    y_mean = df1['y'].mean()

    df2 = df1.copy()
    for i in range(len(df1)):
        point = [df1['x'].iloc[i], df1['y'].iloc[i]]
        df2['x'].iloc[i], df2['y'].iloc[i] = rotate_around_point_highperf(point, theta, origin=(0, 0))

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

    # file_path = []
    # path = r'D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/Calibrated_3DSkeleton'
    # for root, directories, file in os.walk(path):
    #     for file in file:
    #         if file.endswith(".csv"):
    #             # print(os.path.join(root, file))
    #             file_path.append(os.path.join(root, file))

    a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
                 name="video_info.xlsx", column='roundTime', element=1)

    A = choose_data(a, column='ExperimentTime', element='day')
    B = choose_data(A, column='gender', element='male')
    all_time = []
    angle_time_all = []
    circle_time_all = []
    for time_state in range(1, 2):
        # time_state = 1
        # 多条件筛选
        X = choose_data(a, column='split_number', element=time_state)  # split_number=1 not have ''
        df_day = pd.DataFrame(X, columns=["Unique_serial_number"])
        # data = df_day.values.tolist()
        csv_FD = []
        for item in tqdm(df_day['Unique_serial_number']):
            csv_result3 = search_csv(
                path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/back_coordinates_origin/",
                name="rec-{}-G1-2022114230_Cali_Data3d_Replace".format(item))
            csv_FD.append(csv_result3[0])

