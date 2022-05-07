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
    """
        方形安全区域
    """
    # # file_path = []
    # # path = r'D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/Calibrated_3DSkeleton'
    # # for root, directories, file in os.walk(path):
    # #     for file in file:
    # #         if file.endswith(".csv"):
    # #             # print(os.path.join(root, file))
    # #             file_path.append(os.path.join(root, file))
    #
    # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    #              name="video_info.xlsx", column='roundTime', element=1)
    #
    # A = choose_data(a, column='ExperimentTime', element='day')
    # B = choose_data(A, column='gender', element='male')
    # all_time = []
    # angle_time_all = []
    # circle_time_all = []
    # for time_state in range(1, 7):
    #     # time_state = 1
    #     # 多条件筛选
    #     X = choose_data(a, column='split_number', element=time_state)  # split_number=1 not have ''
    #     df_day = pd.DataFrame(X, columns=["Unique_serial_number"])
    #     # data = df_day.values.tolist()
    #     csv_FD = []
    #     for item in tqdm(df_day['Unique_serial_number']):
    #         csv_result3 = search_csv(
    #             path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/Calibrated_3DSkeleton_replace/",
    #             name="rec-{}-G1-2022114230_Cali_Data3d".format(item))
    #         csv_FD.append(csv_result3[0])
    #
    #     location_all = np.zeros((50, 50))
    #     round_1_all = []
    #     round_2_all = []
    #     round_3_all = []
    #     round_4_all = []
    #     round_5_all = []
    #     round_data_all = []
    #
    #     for j in range(0, len(csv_FD)):
    #         # for j in range(0, 1):
    #         data = pd.read_csv(csv_FD[j])
    #
    #         rotation_data = rotation(data)
    #
    #         rotation_data['back'] = normliza_data(rotation_data, data_name='back')
    #         rotation_data['back.1'] = normliza_data(rotation_data, data_name='back.1')
    #
    #         data['back_new'] = rotation_data['back']
    #         data['back.1_new'] = rotation_data['back.1']
    #
    #         # fig = plt.figure(figsize=(5, 5), dpi=300)
    #         # ax = fig.add_subplot(111)
    #         # plt.style.use('ggplot')
    #         # ax = sns.scatterplot(data=rotation_data, x="back", y="back.1", alpha=0.7)
    #
    #         """
    #             迭代统计safe area
    #         """
    #         for t in range(1, 26):
    #             locals()['round_' + str(t)] = 0
    #         # round_25 = 0
    #
    #         for i in range(len(rotation_data)):
    #             for t in range(1, 26):
    #                 # if (-1) * (t - 1) < np.abs(rotation_data['back'].iloc[i]) <= 1 * t and \
    #                 #         (-1) * (t - 1) < np.abs(rotation_data['back.1'].iloc[i]) <= 1 * t:
    #                 #     locals()['round_' + str(t)] = locals()['round_' + str(t)] + 1
    #                 if -t < np.abs(rotation_data['back'].iloc[i]) <= t \
    #                         and -25 < np.abs(rotation_data['back.1'].iloc[i]) <= t:
    #                     # if -t * np.pi < np.abs(rotation_data['back'].iloc[i]) <= t * np.pi \
    #                     #         and -25 * np.pi < np.abs(rotation_data['back.1'].iloc[i]) <= t * np.pi:
    #                     # round_25 = round_25 + 1
    #                     locals()['round_' + str(t)] = locals()['round_' + str(t)] + 1
    #
    #         for t in reversed(range(2, 26)):
    #             # locals()['round_' + str(t)] = locals()['round_' + str(t)] - locals()['round_' + str(t - 1)]
    #             locals()['round_' + str(t)] = (locals()['round_' + str(t)] - locals()['round_' + str(t - 1)]) / (
    #                         99 - (25 - t) * 2)
    #
    #         # locals()['round_' + str(1)] = locals()['round_' + str(1)]/4
    #         round_1 = round_1 / 4
    #
    #         round_data = []
    #         for t in range(1, 26):
    #             round_data.append(locals()['round_' + str(t)])
    #
    #         print(sum(round_data))
    #         round_data_all.append(round_data)
    #         print('第{}个文件已处理'.format(j))
    #     all_time.append(round_data_all)
    #
    # time1 = np.array(all_time[0]).T
    # time_all = time1
    # for i in range(1, 5):
    #     time_all = np.concatenate((time_all, np.array(all_time[i + 1]).T), axis=1)
    #
    # # 安全区域可视化代码
    # # round_data_all = np.array(round_data_all).T
    # # sns.heatmap(time_all)
    # mean_data = []
    # for i in range(len(time_all)):
    #     mean_data.append(np.mean(time_all[i, :]) / 30 / 60)
    # x = [i for i in range(1, 26)]
    # fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    # plt.plot(x, mean_data, color='#845EC2')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # plt.xlabel('Distance from center point(cm)', fontsize=13)
    # plt.ylabel('Exploration duration(min)', fontsize=13)
    # plt.tight_layout()
    # plt.show()
    # plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area/'
    #             'range_safe_area.tiff', dpi=300, transparent=True)

    # import statistics
    # print(statistics.mean(all_time))

    """
        圆形安全区域
    """
    a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
                 name="video_info.xlsx", column='roundTime', element=1)

    A = choose_data(a, column='ExperimentTime', element='day')
    B = choose_data(A, column='gender', element='male')
    all_time = []
    angle_time_all = []
    circle_time_all = []
    for time_state in range(1, 7):
        # time_state = 1
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

        location_all = np.zeros((50, 50))
        round_1_all = []
        round_2_all = []
        round_3_all = []
        round_4_all = []
        round_5_all = []
        round_data_all = []

        for j in range(0, len(csv_FD)):
            # for j in range(0, 1):
            data = pd.read_csv(csv_FD[j])

            rotation_data = rotation(data)

            rotation_data['back'] = normliza_data(rotation_data, data_name='back')
            rotation_data['back.1'] = normliza_data(rotation_data, data_name='back.1')

            data['back_new'] = rotation_data['back']
            data['back.1_new'] = rotation_data['back.1']

            # fig = plt.figure(figsize=(5, 5), dpi=300)
            # ax = fig.add_subplot(111)
            # plt.style.use('ggplot')
            # ax = sns.scatterplot(data=rotation_data, x="back", y="back.1", alpha=0.7)

            """
                迭代统计safe area
            """
            for t in range(1, 36):
                locals()['round_' + str(t)] = 0
            # round_25 = 0

            for i in range(len(rotation_data)):
                for t in range(1, 36):
                    if np.square(rotation_data['back'].iloc[i]) + np.square(rotation_data['back.1'].iloc[i]) <= t * t:
                        locals()['round_' + str(t)] = locals()['round_' + str(t)] + 1

            for t in reversed(range(2, 36)):
                locals()['round_' + str(t)] = (locals()['round_' + str(t)] - locals()['round_' + str(t - 1)]) / (
                        np.pi * ((t - 1) * 2 + 1))

            round_1 = round_1 / (np.pi * 1)

            round_data = []
            for t in range(1, 36):
                round_data.append(locals()['round_' + str(t)])

            print(sum(round_data))

            round_data_all.append(round_data)
            print('第{}个文件已处理'.format(j))

        all_time.append(round_data_all)

    time1 = np.array(all_time[0]).T
    time_all = time1
    for i in range(1, 5):
        time_all = np.concatenate((time_all, np.array(all_time[i + 1]).T), axis=1)

    # 安全区域可视化代码
    # round_data_all = np.array(round_data_all).T
    # sns.heatmap(time_all)

    mean_data = []
    for i in range(len(time_all)):
        mean_data.append(np.mean(time_all[i, :]) / 30 / 60)
    x = [i for i in range(1, 26)]
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    plt.plot(x, mean_data, color='#845EC2')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('Distance from center point(cm)', fontsize=13)
    plt.ylabel('Exploration duration(min)', fontsize=13)
    plt.tight_layout()
    plt.show()
