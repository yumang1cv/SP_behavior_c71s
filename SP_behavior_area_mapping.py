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

    # file_path = []
    # path = r'D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/Calibrated_3DSkeleton'
    # for root, directories, file in os.walk(path):
    #     for file in file:
    #         if file.endswith(".csv"):
    #             # print(os.path.join(root, file))
    #             file_path.append(os.path.join(root, file))
    a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
                 name="video_info.xlsx", column='roundTime', element=1)
    ExperimentTime = 'night'
    gender = 'female'

    # A = choose_data(a, column='ExperimentTime', element=ExperimentTime)
    # B = choose_data(A, column='gender', element=gender)
    for time_state in range(1, 7):
        # time_state = 6
        # 多条件筛选
        X = choose_data(a, column='split_number', element=time_state)  # split_number=1 not have ''
        df_day = pd.DataFrame(X, columns=["Unique_serial_number"])
        # data = df_day.values.tolist()

        csv_FD = []
        for item in tqdm(df_day['Unique_serial_number']):
            csv_result3 = search_csv(
                path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/Calibrated_3DSkeleton_replace/",
                name="rec-{}-G1-2022114230_Cali_Data3d".format(item))
            csv_FD.append(csv_result3[0])

        behavior_file = []
        for item in tqdm(df_day['Unique_serial_number']):
            csv_result4 = search_csv(
                path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
                name="rec-{}-G1-2022114230_Movement_Labels".format(item))
            behavior_file.append(csv_result4[0])

            # location_all = np.zeros((50, 50))

            """
                combine behavior test code
            """
            # for j in range(0, len(csv_FD), 6):

            # for j in range(13, 19, 6):
            #     data0 = pd.read_csv(csv_FD[j])
            #     behavior_data0 = pd.read_csv(behavior_file[j])
            #     behavior_label0 = behavior_data0.iloc[:, 1:2]
            #
            #     data1 = pd.read_csv(csv_FD[j + 1])
            #     behavior_data1 = pd.read_csv(behavior_file[j + 1])
            #     behavior_label1 = behavior_data1.iloc[:, 1:2]
            #
            #     data2 = pd.read_csv(csv_FD[j + 2])
            #     behavior_data2 = pd.read_csv(behavior_file[j + 2])
            #     behavior_label2 = behavior_data2.iloc[:, 1:2]
            #
            #     data3 = pd.read_csv(csv_FD[j + 3])
            #     behavior_data3 = pd.read_csv(behavior_file[j + 3])
            #     behavior_label3 = behavior_data3.iloc[:, 1:2]
            #
            #     data4 = pd.read_csv(csv_FD[j + 4])
            #     behavior_data4 = pd.read_csv(behavior_file[j + 4])
            #     behavior_label4 = behavior_data4.iloc[:, 1:2]
            #
            #     data5 = pd.read_csv(csv_FD[j + 5])
            #     behavior_data5 = pd.read_csv(behavior_file[j + 5])
            #     behavior_label5 = behavior_data5.iloc[:, 1:2]
            #
            #     data_all = [data0.iloc[2:], data1.iloc[2:], data2.iloc[2:], data3.iloc[2:], data4.iloc[2:], data5.iloc[2:]]
            #     data_6_all = pd.concat(data_all, axis=0)
            #     # data_6_all = data_6_all.iloc[2:]
            #     # rotation_data = rotation(data_6_all)
            #
            #     # rotation_data['back'] = normliza_data(rotation_data, data_name='back')
            #     # rotation_data['back.1'] = normliza_data(rotation_data, data_name='back.1')
            #     #
            #     # for x in range(1, 7):
            #     #     locals()['rotation_data_{}'.format(x)] = rotation_data.iloc[18000 * (x - 1):18000 * x]
            #     #     locals()['rotation_data_{}'.format(x)]['behavior_label'] = locals()['behavior_label{}'.format(x - 1)]
            #
            #     # data1, data2, data3, data4, data5, data6 = combine_behavior(csv_FD, behavior_file, x)
            #
            #     # fig = plt.figure(figsize=(6, 6), dpi=300)
            #     # ax = fig.add_subplot(111)
            #     # # plt.style.use('ggplot')
            #     # ax = sns.scatterplot(data=post_data, x="back", y="back.1", hue='behavior_label', size=0.01,
            #     #                      palette=behavior_color, alpha=0.7, legend=False)
            #     # ax.add_patch(Rectangle((12.5, 12.5), 25, 25, color="gray", alpha=0.15))
            #     # color = 'black'
            #     # alpha_value = 0.7
            #     # line_value = 0.7
            #     # ax.plot([0, 0], [0, 50], linewidth=line_value, color=color, alpha=alpha_value)
            #     # ax.plot([50, 50], [0, 50], linewidth=line_value, color=color, alpha=alpha_value)
            #     # ax.plot([0, 50], [0, 0], linewidth=line_value, color=color, alpha=alpha_value)
            #     # ax.plot([0, 50], [50, 50], linewidth=line_value, color=color, alpha=alpha_value)
            #     # plt.axis('off')
            #     # plt.show()
            #     # plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area/'
            #     #             'inside_outside/{}.tiff'.format(j + 1), dpi=300)
            #     # plt.close()
            #
            # df1 = data_6_all.iloc[2:, 36:38]  # select back vector
            # # df1 = dataframe
            # df1 = df1.astype(float)
            # # df1['back'], df1['back.1'] = rotate_around_point_highperf(df1, 0.3, origin=(0, 0))
            # x_max = df1['back'].max()
            # # print(df1[df1['back'] == x_max].index.values)
            # y1 = df1['back.1'][df1[df1['back'] == x_max].index.values]
            # y1 = y1.values[0]
            # x_min = df1['back'].min()
            # y_max = df1['back.1'].max()
            # y_min = df1['back.1'].min()
            # x1 = df1['back'][df1[df1['back.1'] == y_min].index.values]
            # x1 = x1.values[0]
            #
            # L1 = y1 - y_min
            # L2 = x_max - x1
            # theta = math.atan(L1 / L2) / math.pi * 180
            #
            # x_mean = df1['back'].mean()
            # y_mean = df1['back.1'].mean()
            #
            # df2 = df1.copy()
            # for i in range(len(df1)):
            #     point = [df1['back'].iloc[i], df1['back.1'].iloc[i]]
            #     # df2['back'].iloc[i], df2['back.1'].iloc[i] = rotate_around_point_highperf(point, theta, origin=(0, 0))
            #     df2['back'].iloc[i], df2['back.1'].iloc[i] = rotate_around_point_highperf(point, theta, origin=(0, 0))
            #
            # # plot_figure(rotation_data_2)
            # ax = sns.scatterplot(data=df1, x="back", y="back.1")
            # ax = sns.scatterplot(data=df2, x="back", y="back.1")

            """
                50*50 小方格分析(分析所待时间)
            """
            # location_all = np.zeros((50, 50))
            # for i in range(len(csv_FD)):
            #     post_data = combine_behavior_1(csv_FD[i], behavior_file[i])
            #     location = np.zeros((50, 50))
            #     for t in range(len(post_data['back'])):
            #         post_data['back'].iloc[t] = int(post_data['back'].iloc[t])
            #         post_data['back.1'].iloc[t] = int(post_data['back.1'].iloc[t])
            #         x = int(post_data['back'].iloc[t])
            #         y = int(post_data['back.1'].iloc[t])
            #         location[x, y] += 1
            #
            #     location_all += location
            #     print('第{}个文件已计算'.format(i))
            #
            # location_all = location_all / len(csv_FD)
            #
            # # 画图代码
            # fig = plt.figure(figsize=(6, 5), dpi=300)
            # ax = fig.add_subplot(111)
            # ax = sns.heatmap(location_all, cmap="jet", yticklabels=False, xticklabels=False, vmin=0, vmax=200)
            # # ax = sns.heatmap(location_all, cmap="rocket", yticklabels=False, xticklabels=False, vmin=0, vmax=150)
            # plt.tight_layout()
            # plt.show()
            # plt.savefig("D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/"
            #             "safe_area/2500_cell/{}_{}_{}_v2.tiff".format(gender, ExperimentTime, time_state), dpi=300)
            # plt.close(fig)

            """
                50*50 小方格mapping
            """
            # location_all = np.zeros((50, 50))
            # class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
            #               9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
            # location_all[0, 0] = class_type
            # for i in range(len(csv_FD)):
            #     post_data = combine_behavior_1(csv_FD[i], behavior_file[i])
            #     location = np.zeros((50, 50))
            #     for t in range(len(post_data['back'])):
            #         post_data['back'].iloc[t] = int(post_data['back'].iloc[t])
            #         post_data['back.1'].iloc[t] = int(post_data['back.1'].iloc[t])
            #         x = int(post_data['back'].iloc[t])
            #         y = int(post_data['back.1'].iloc[t])
            #         location[x, y] += 1
            #
            #     location_all += location
            #     print('第{}个文件已计算'.format(i))
            #
            # location_all = location_all / len(csv_FD)

            """
                ①生成一个三级列表
                ②第一级是：50行、第二级是：50列、第三级是：行为字典
            """
        # list_row = []  # 50行
        # list_column = []  # 50列，行列确定小格子所处位置
        # behavior_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
        #                  9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        # for x in range(50):
        #     tmp = copy.deepcopy(behavior_type)
        #     list_column.append(tmp)
        #
        # for x in range(50):
        #     tmp = copy.deepcopy(list_column)
        #     list_row.append(tmp)

        behavior_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                         9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

        total_behavior = []
        for i in range(50 * 50):
            tmp = copy.deepcopy(behavior_type)
            total_behavior.append(tmp)

        map_array = np.zeros((50, 50))
        count = 0
        for i in range(map_array.shape[0] - 1, -1, -1):
            for j in range(map_array.shape[1]):
                map_array[i][j] = count
                count += 1

        # for i in range(0, 1):
        for i in range(0, len(csv_FD)):
            post_data = combine_behavior_1(csv_FD[i], behavior_file[i])
            location = np.zeros((50, 50))
            for t in range(len(post_data['back']) - 5):
                post_data['back'].iloc[t] = int(post_data['back'].iloc[t])
                post_data['back.1'].iloc[t] = int(post_data['back.1'].iloc[t])
                x = int(post_data['back'].iloc[t])
                y = int(post_data['back.1'].iloc[t])
                behavior_label = int(post_data['behavior_label'].iloc[t])
                # list_row[x][y][behavior_label] += 1
                index = int(map_array[x][y])
                total_behavior[index][behavior_label] += 1
            print('第{}个文件已处理'.format(i))

        behavior_list = []

        for item in total_behavior:
            new_ma_val = max(item.items(), key=operator.itemgetter(1))[0]
            behavior_list.append(new_ma_val)

        behavior_list1 = np.array(behavior_list).reshape(50, 50)
        behavior_list1[0:1, :] = behavior_list1[49:50, :] = behavior_list1[:, 0:1] = behavior_list1[:, 49:50] = 15
        color_list = ['#D53624', '#FF6F91', '#FF9671', '#FFC75F', '#C34A36',
                      '#00C2A8', '#00a3af', '#008B74', '#D5CABD', '#D65DB1',
                      '#cb3a56', '#845EC2', '#B39CD0', '#98d98e', '#4B4453']
        colormap = sns.color_palette(color_list)
        # colormap = sns.color_palette("hls")
        fig = plt.figure(figsize=(5, 5), dpi=300)
        ax = fig.add_subplot(111)
        ax = sns.heatmap(behavior_list1, cmap=colormap[1:], xticklabels=False, yticklabels=False, cbar=False)
        # ax = sns.heatmap(behavior_list1, cmap=colormap[1:], xticklabels=False, yticklabels=False)
        plt.tight_layout()
        plt.show()
        plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area'
                    '/mapping/state{}.tiff'.format(time_state), dpi=300)
        plt.close()

    """
        5个区域分析
    """
    #     round_1 = 0
    #     round_2 = 0
    #     round_3 = 0
    #     round_4 = 0
    #     round_5 = 0
    #     for i in range(len(rotation_data)):
    #         for t in range(1, 6):
    #             if (-5) * (t - 1) < np.abs(rotation_data['back'].iloc[i]) <= 5 * t and \
    #                     (-5) * (t - 1) < np.abs(rotation_data['back.1'].iloc[i]) <= 5 * t:
    #                 locals()['round_' + str(t)] = locals()['round_' + str(t)] + 1
    #         #         locals()['round_' + str(t)] = locals()['round_' + str(t)] + 1
    #         # if -5 < rotation_data['back'].iloc[i] <= 5 and -5 < rotation_data['back.1'].iloc[i] <= 5:
    #         #     round_1 = round_1 + 1
    #         # elif -10 < rotation_data['back'].iloc[i] <= 10 and -10 < rotation_data['back.1'].iloc[i] <= 10:
    #         #     round_2 = round_2 + 1
    #         # elif -15 < rotation_data['back'].iloc[i] <= 15 and -15 < rotation_data['back.1'].iloc[i] <= 15:
    #         #     round_3 = round_3 + 1
    #         # elif -20 < rotation_data['back'].iloc[i] <= 20 and -20 < rotation_data['back.1'].iloc[i] <= 20:
    #         #     round_4 = round_4 + 1
    #         # elif -25 < rotation_data['back'].iloc[i] <= 25 and -25 < rotation_data['back.1'].iloc[i] <= 25:
    #         #     round_5 = round_5 + 1
    #     round_5 = (round_5 - round_4) / 30 / 60
    #     round_4 = (round_4 - round_3) / 30 / 60
    #     round_3 = (round_3 - round_2) / 30 / 60
    #     round_2 = (round_2 - round_1) / 30 / 60
    #     round_1 = round_1 / 30 / 60
    #     print(round_5 + round_4 + round_3 + round_2 + round_1)
    #
    #     round_1_all.append(round_1)
    #     round_2_all.append(round_2)
    #     round_3_all.append(round_3)
    #     round_4_all.append(round_4)
    #     round_5_all.append(round_5)
    #     round_all = [round_1_all, round_2_all, round_3_all, round_4_all, round_5_all]
    #     print('第{}个文件已计算结束'.format(j))
    #
    # all_time.append(round_all)
    # for m in range(len(all_time)):
    #     all_time[m] = list(np.ravel(all_time[m]))
    # all_time = pd.DataFrame(all_time).T
    # all_time = all_time.rename(columns={0: "10min", 1: '20min', 2: "30min",
    #                                     3: '40min', 4: '50min', 5: '60min'})
    # sns.heatmap(all_time)

    # all_time.to_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area/fang_5area.csv')
