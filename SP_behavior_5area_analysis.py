# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_5area_analysis.py
# @Time      :2022/5/6 11:22
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
from matplotlib.patches import Rectangle
import copy
import operator

matplotlib.use('Qt5Agg')

names = ['Running', 'Fast walking/Trotting', 'Right turning', 'Left turning',
         'Jumping', 'Climbing up', 'Falling', 'Up search/Rising', 'Grooming',
         'Sniffing and Walking', 'Stepping', 'Sniffing', 'Sniffing pause',
         'Rearing/Diving']

color_list = ['#D53624', '#FF6F91', '#FF9671', '#FFC75F', '#C34A36',
              '#00C2A8', '#00a3af', '#008B74', '#D5CABD', '#D65DB1',
              '#cb3a56', '#845EC2', '#B39CD0', '#98d98e']

behavior_color = dict(zip([i for i in range(1, 15, 1)], color_list))


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
    # df1 = dataframe
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
    # scaler = MinMaxScaler(feature_range=(-24, 24))  # 计算圆弧使用
    scaler = MinMaxScaler(feature_range=(1, 49))  # 计算 50*50 小方格使用
    norm = scaler.fit(norm_data)
    norm_data = scaler.transform(norm_data)
    norm_data = norm_data.reshape(len(data1), 1)

    return norm_data


def combine_behavior_1(zuobiao_file, behavior):  # 单个文件合并矫正
    data = pd.read_csv(zuobiao_file)
    behavior_data = pd.read_csv(behavior)
    behavior_label = behavior_data.iloc[:, 1:2]
    # behavior_label = behavior_label.tolist()

    rotation_data = rotation(data)

    rotation_data['back'] = normliza_data(rotation_data, data_name='back')
    rotation_data['back.1'] = normliza_data(rotation_data, data_name='back.1')
    rotation_data['behavior_label'] = behavior_label

    data['back_new'] = rotation_data['back']
    data['back.1_new'] = rotation_data['back.1']

    return rotation_data


def combine_behavior(zuobiao_file, behavior, start_num):  # 先把一小时坐标合并矫正再进行分割画图

    data0 = pd.read_csv(zuobiao_file[start_num])
    behavior_data0 = pd.read_csv(behavior[start_num])
    behavior_label0 = behavior_data0.iloc[:, 1:2]

    data1 = pd.read_csv(zuobiao_file[start_num + 1])
    behavior_data1 = pd.read_csv(behavior[start_num + 1])
    behavior_label1 = behavior_data1.iloc[:, 1:2]

    data2 = pd.read_csv(zuobiao_file[start_num + 2])
    behavior_data2 = pd.read_csv(behavior[start_num + 2])
    behavior_label2 = behavior_data2.iloc[:, 1:2]

    data3 = pd.read_csv(zuobiao_file[start_num + 3])
    behavior_data3 = pd.read_csv(behavior[start_num + 3])
    behavior_label3 = behavior_data3.iloc[:, 1:2]

    data4 = pd.read_csv(zuobiao_file[start_num + 4])
    behavior_data4 = pd.read_csv(behavior[start_num + 4])
    behavior_label4 = behavior_data4.iloc[:, 1:2]

    data5 = pd.read_csv(zuobiao_file[start_num + 5])
    behavior_data5 = pd.read_csv(behavior[start_num + 5])
    behavior_label5 = behavior_data5.iloc[:, 1:2]

    data_all = [data0.iloc[2:], data1.iloc[2:], data2.iloc[2:], data3.iloc[2:], data4.iloc[2:], data5.iloc[2:]]
    data_6_all = pd.concat(data_all, axis=0)
    # data_6_all = data_6_all.iloc[2:]
    rotation_data = rotation(data_6_all)
    rotation_data['back'] = normliza_data(rotation_data, data_name='back')
    rotation_data['back.1'] = normliza_data(rotation_data, data_name='back.1')

    # for x in range(1, 7):
    #     locals()['rotation_data_{}'.format(x)] = rotation_data.iloc[18000 * (x - 1):18000 * x]
    #     locals()['rotation_data_{}'.format(x)]['behavior_label'] = locals()['behavior_label{}'.format(x - 1)]

    rotation_data_1 = rotation_data.iloc[18000 * (1 - 1):18000 * 1]
    rotation_data_1['behavior_label'] = behavior_label0

    rotation_data_2 = rotation_data.iloc[18000 * (2 - 1):18000 * 2]
    rotation_data_2['behavior_label'] = behavior_label1

    rotation_data_3 = rotation_data.iloc[18000 * (3 - 1):18000 * 3]
    rotation_data_3['behavior_label'] = behavior_label2

    rotation_data_4 = rotation_data.iloc[18000 * (4 - 1):18000 * 4]
    rotation_data_4['behavior_label'] = behavior_label3

    rotation_data_5 = rotation_data.iloc[18000 * (5 - 1):18000 * 5]
    rotation_data_5['behavior_label'] = behavior_label4

    rotation_data_6 = rotation_data.iloc[18000 * (6 - 1):18000 * 6]
    rotation_data_6['behavior_label'] = behavior_label5

    return rotation_data_1, rotation_data_2, rotation_data_3, rotation_data_4, rotation_data_5, rotation_data_6


def plot_figure(post_data):
    fig = plt.figure(figsize=(6, 6), dpi=300)
    ax = fig.add_subplot(111)
    # plt.style.use('ggplot')
    ax = sns.scatterplot(data=post_data, x="back", y="back.1", hue='behavior_label', size=0.01,
                         palette=behavior_color, alpha=0.7, legend=False)
    ax.add_patch(Rectangle((12.5, 12.5), 25, 25, color="gray", alpha=0.15))
    color = 'black'
    alpha_value = 0.7
    line_value = 0.7
    ax.plot([0, 0], [0, 50], linewidth=line_value, color=color, alpha=alpha_value)
    ax.plot([50, 50], [0, 50], linewidth=line_value, color=color, alpha=alpha_value)
    ax.plot([0, 50], [0, 0], linewidth=line_value, color=color, alpha=alpha_value)
    ax.plot([0, 50], [50, 50], linewidth=line_value, color=color, alpha=alpha_value)
    plt.axis('off')
    plt.show()
    # plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area/'
    #             'inside_outside/{}.tiff'.format(j + 1), dpi=300)
    # plt.close()
    return


if __name__ == '__main__':

    """
        behavior + trace plot
    """
    # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    #              name="video_info.xlsx", column='roundTime', element=1)
    # ExperimentTime = 'night'
    # # gender = 'male'
    #
    # A = choose_data(a, column='ExperimentTime', element=ExperimentTime)
    # # B = choose_data(A, column='gender', element=gender)
    # # for time_state in range(1, 7):
    # time_state = 6
    # # 多条件筛选
    # X = choose_data(A, column='split_number', element=time_state)  # split_number=1 not have ''
    #
    # a = pd.read_excel('D:/3D_behavior/Spontaneous_behavior/result_fang/video_info.xlsx')
    #
    # df_day = pd.DataFrame(a, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    #
    # csv_FD = []
    # for item in tqdm(df_day['Unique_serial_number'][0:432]):
    #     csv_result3 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/back_coordinates_origin/",
    #         name="rec-{}-G1-2022114230_Cali_Data3d_Replace".format(item))
    #     csv_FD.append(csv_result3[0])
    #
    # behavior_file = []
    # for item in tqdm(df_day['Unique_serial_number'][0:432]):
    #     csv_result4 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    #         name="rec-{}-G1-2022114230_Movement_Labels".format(item))
    #     behavior_file.append(csv_result4[0])
    #
    # for j in range(len(csv_FD)):
    #     data = pd.read_csv(csv_FD[j])
    #     behavior_label = pd.read_csv(behavior_file[j])
    #     data['behavior_label'] = behavior_label.iloc[:, 1:2]
    #     fig = plt.figure(figsize=(6, 6), dpi=300)
    #     ax = fig.add_subplot(111)
    #     # ax.plot(data['x'], data['y'], color='black')
    #     ax.add_patch(Rectangle((-170, -170), 340, 340, color="lightgray", alpha=0.6))
    #     ax = sns.scatterplot(data=data, x="x", y="y", hue='behavior_label', size=0.01,
    #                          palette=behavior_color, alpha=0.7, legend=False)
    #     color = 'black'
    #     alpha_value = 0.7
    #     line_value = 1.5
    #     ax.plot([250, 250], [-250, 250], linewidth=line_value, color=color, alpha=alpha_value)
    #     ax.plot([-250, -250], [-250, 250], linewidth=line_value, color=color, alpha=alpha_value)
    #     ax.plot([-250, 250], [250, 250], linewidth=line_value, color=color, alpha=alpha_value)
    #     ax.plot([-250, 250], [-250, -250], linewidth=line_value, color=color, alpha=alpha_value)
    #     # ax.add_patch(Rectangle((-250, -250), 500, 500, color="lightgray", alpha=0.4))
    #     plt.axis('off')
    #     plt.show()
    #     plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area/inside_outside/add_behavior_34/'
    #                 '{}.tiff'.format(j), dpi=300, transparent=True)
    #     plt.close()

    """
        trace plot 
        # color  aera1 : #a697c8    area2 : #a3d7e3    area3 : #c9e2a2   area4 : #fad69f   area5 : #f1a691
    """
    # a = pd.read_excel('D:/3D_behavior/Spontaneous_behavior/result_fang/video_info.xlsx')
    # df_day = pd.DataFrame(a, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    #
    # csv_FD = []
    # for item in tqdm(df_day['Unique_serial_number'][0:432]):
    #     csv_result3 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/back_coordinates_origin/",
    #         name="rec-{}-G1-2022114230_Cali_Data3d_Replace".format(item))
    #     csv_FD.append(csv_result3[0])
    #
    # # behavior_file = []
    # # for item in tqdm(df_day['Unique_serial_number']):
    # #     csv_result4 = search_csv(
    # #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    # #         name="rec-{}-G1-2022114230_Movement_Labels".format(item))
    # #     behavior_file.append(csv_result4[0])
    # # for j in range(1):
    # for j in range(len(csv_FD)):
    #     data = pd.read_csv(csv_FD[j])
    #     fig = plt.figure(figsize=(6, 6), dpi=300)
    #     ax = fig.add_subplot(111)
    #     # ax = sns.scatterplot(data=data, x="x", y="y")
    #     color = 'black'
    #     alpha_value = 0.7
    #     line_value = 0.7
    #     # ax.plot([250, 250], [-250, 250], linewidth=line_value, color=color, alpha=alpha_value)
    #     # ax.plot([-250, -250], [-250, 250], linewidth=line_value, color=color, alpha=alpha_value)
    #     # ax.plot([-250, 250], [250, 250], linewidth=line_value, color=color, alpha=alpha_value)
    #     # ax.plot([-250, 250], [-250, -250], linewidth=line_value, color=color, alpha=alpha_value)
    #     ax.add_patch(Rectangle((-250, -250), 500, 500, color="lightgray", alpha=0.4))
    #     ax.add_patch(Rectangle((-170, -170), 340, 340, color="#c29799", alpha=0.4))
    #
    #     # ax.add_patch(Rectangle((-250, -250), 500, 500, color="#a697c8", alpha=1))
    #     # ax.add_patch(Rectangle((-200, -200), 400, 400, color="#a3d7e3", alpha=1))
    #     # ax.add_patch(Rectangle((-150, -150), 300, 300, color="#c9e2a2", alpha=1))
    #     # ax.add_patch(Rectangle((-100, -100), 200, 200, color="#fad69f", alpha=1))
    #     # ax.add_patch(Rectangle((-50, -50), 100, 100, color="#f1a691", alpha=1))
    #
    #     ax.plot(data['x'], data['y'], color='black')
    #     plt.axis('off')
    #     plt.show()
    #     plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area/inside_outside/trace_34/'
    #                 '{}.tiff'.format(j), dpi=300, transparent=True)
    #     plt.close()

    """
        total distance
    """
    ExperimentTime = 'night'
    gender = 'male'
    # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    #              name="video_info.xlsx", column='roundTime', element=1)
    a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
                 name="video_info.xlsx", column='ExperimentTime', element=ExperimentTime)

    # A = choose_data(a, column='ExperimentTime', element=ExperimentTime)

    B = choose_data(a, column='gender', element=gender)
    for time_state in range(1, 7):
        # time_state = 6
        # globals()['distance' + str(time_state * 10 - 5)] = []  # 5min
        globals()['distance' + str(time_state * 10)] = []
        # 多条件筛选
        X = choose_data(B, column='split_number', element=time_state)  # split_number=1 not have ''

        # a = pd.read_excel('D:/3D_behavior/Spontaneous_behavior/result_fang/video_info.xlsx')

        df_day = pd.DataFrame(X, columns=["Unique_serial_number"])
        # data = df_day.values.tolist()

        csv_FD = []
        for item in tqdm(df_day['Unique_serial_number'][0:15]):
            csv_result3 = search_csv(
                path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/back_coordinates_origin/",
                name="rec-{}-G1-2022114230_Cali_Data3d_Replace".format(item))
            csv_FD.append(csv_result3[0])

        for x in range(len(csv_FD)):
            data_1 = pd.read_csv(csv_FD[x])
            distance = []
            for i in range(1, len(data_1)):
                dis = np.sqrt(np.square(data_1['x'].iloc[i] - data_1['x'].iloc[i - 1]) + np.square(
                    data_1['y'].iloc[i] - data_1['y'].iloc[i - 1]))
                distance.append(dis)

            distance.insert(0, np.mean(distance))
            data_1['distance'] = distance

            # distance_1 = data_1['distance'].iloc[0 * 9000:(0 + 1) * 9000].sum()
            # distance_2 = data_1['distance'].iloc[1 * 9000:(1 + 1) * 9000].sum()  # 5min

            distance_2 = data_1['distance'].iloc[0 * 9000:(1 + 1) * 9000].sum()  # 10min

            # globals()['distance' + str(time_state * 10 - 5)].append(distance_1)
            globals()['distance' + str(time_state * 10)].append(distance_2)

    """
        5min导出结果
    """
    # distance_all = []
    # for x in range(5, 65, 5):
    #     distance_all = distance_all + globals()['distance' + str(x)]
    #
    # distance_all = np.array(distance_all).reshape(12, int(len(distance_all) / 12))
    # distance_all = pd.DataFrame(distance_all)
    # distance_all = distance_all.applymap(lambda y: y / 1000)
    # # distance_all = distance_all.rename(columns={0: '5min', 1: '10min'}, index={0: 'mouse1', 1: 'mouse2'})
    # distance_all = distance_all.rename(index={0: '5min', 1: '10min'}, columns={0: 'mouse1', 1: 'mouse2'})
    # # distance_all = distance_all.rename(columns={distance_all.columns[0]: '5min'})
    # distance_all.to_excel('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/total_distance/fang/'
    #                       '{}_{}_5min.xlsx'.format(gender, ExperimentTime))

    """
        10min导出结果
    """
    distance_all = []
    for x in range(10, 70, 10):
        distance_all = distance_all + globals()['distance' + str(x)]

    distance_all = np.array(distance_all).reshape(6, int(len(distance_all) / 6))
    distance_all = pd.DataFrame(distance_all)
    distance_all = distance_all.applymap(lambda y: y / 1000)
    # distance_all = distance_all.rename(columns={0: '10min', 1: '20min'}, index={0: 'mouse1', 1: 'mouse2'})
    distance_all = distance_all.rename(index={0: '10min', 1: '20min'}, columns={0: 'mouse1', 1: 'mouse2'})
    # distance_all = distance_all.rename(columns={distance_all.columns[0]: '5min'})
    distance_all.to_excel('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/total_distance/fang/'
                          '{}_{}_10min.xlsx'.format(gender, ExperimentTime))
