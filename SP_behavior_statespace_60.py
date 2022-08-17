# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_statespace_60.py
# @Time      :2022/5/16 17:09
# @Author    :XuYang
import pandas as pd
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')

# color_list = sns.color_palette("Spectral", 40)
# color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
#               '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
#               '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
#               '#93DEB1']
# """
#     Arousal Behavior Class Combine
#     1、Right turning:[1]  (#845EC2)             2、Left turning:[26]  (#B39CD0)
#     3、Sniffing:[2, 4, 10, 11, 12, 16, 22, 25]  (#D65DB1)
#     4、Walking:[3, 6, 7, 19, 30]  (#4FFBDF)     5、Trembling:[5, 15, 32, 40]  (#FFC75F)
#     6、Climbing:[8, 29]   (#D5CABD)             7、Falling:[9]         (#B0A8B9)
#     8、Immobility:[13, 20, 33, 34] (#FF6F91)    9、Paralysis:[14, 35]  (#F9F871)
#     10、Standing:[17]      (#D7E8F0)            11、Trotting:[18, 31]  (#60DB73)
#     12、Grooming:[21]      (#E8575A)            13、Flight:[23, 38]    (#008B74)
#     14、Running:[24, 36]   (#00C0A3)            15、LORR:[27, 28, 39]  (#FF9671)
#     16、Stepping:[37]      (#93DEB1)
# """
# color_list = ['#FF6F91', '#FF9671', '#FFC75F', '#FACCFF', '#D65DB1',
#               '#4FFBDF', '#845EC2', '#D5CABD', '#00C2A8', '#008B74',
#               '#77CA9C', '#C4FCEF', '#C34A36', '#BE93FD']
# """
#     Spontaneous Behavior Class Combine
#     1、Running:[15, 16, 35, 22]   '#FF6F91'      2、Right turning:[7, 31, 34]  '#FF9671'     3、Left turning:[9, 21]  '#FFC75F'
#     4、Walking:[8, 18, 23, 24, 37] '#FACCFF'     5、Trotting:[3, 5, 6, 17, 19]  '#D65DB1'    6、Rearing:[12, 26]      '#4FFBDF'
#     7、Sniffing:[1, 4, 10, 13, 14, 20, 27, 28, 29, 30]  '#845EC2'                            8、Grooming:[39, 40]    '#D5CABD'
#     9、Diving:[11, 25]  '#00C2A8'                10、Rising:[2]   '#008B74'                   11、Hunching:[36]       '#77CA9C'
#     12、Falling:[32]   '#C4FCEF'                 13、Jumping:[33] '#C34A36'                   14、Stepping:[38]       '#BE93FD'
#
#     Right Sniffing:[1, 4, 13, 20, 28, 30]                            Right Sniffing:[14, 27, 29]
#     Immobility:{7、Sniffing:[1, 4, 6, 10, 14, 28, 29, 30],8、 Grooming:[39, 40], 9、Diving:[11, 25], 10、Rising:[2]}
# """

color_list = ['#D32F2F', '#FF8A65', '#FFCDD2', '#FFAB91', '#FFCC80',
              '#4CAF50', '#C5E1A5', '#78b778', '#F06292', '#4FC3F7',
              '#FBE9E7', '#00B8D4', '#9E9E9E', '#81C784']
# """
#     Spontaneous Behavior Class Combine-Final
#     1、Running:[15, 16, 22] '#D53624'     2、Fast walking/Trotting:[8] '#FF6F91'          3、Right turning:[7, 31, 34] '#FF9671'
#     4、Left turning:[9, 21, 38] '#FFC75F' 5、Jumping:[33, 35] '#C34A36'                   6、Climbing up:[26, 12]  '#00C2A8'
#     7、Falling:[32]  '#00a3af'            8、Up search/Rising:[13, 36, 17, 18] '#008B74'  9、Grooming:[2, 39, 40]  '#D5CABD'
#     10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#D65DB1'                               11、Stepping:[3, 19]  '#cb3a56'
#     12、Sniffing:[28, 27, 14, 20, 29, 1]   '#845EC2'                                     13、Sniffing pause:[4, 10, 30] '#B39CD0'
#     14、Rearing/Diving:[11, 25]  '#98d98e'
# """

# color_list = ['#fd7f69', '#fa9b8b', '#64b0fb', '#87c0f9', '#fcb83c',
#               '#3e9a3e', '#95c695', '#78b778', '#fc3cfc', '#41a0fd',
#               '#fddc2f', '#fae15e', '#8b8b8b', '#5ca95c']
"""
    Spontaneous Behavior Class Combine-YJL
    1、Running:[15, 16, 22] '#D32F2F'     2、Fast walking/Trotting:[8] '#FF8A65'          3、Right turning:[7, 31, 34] '#FFCDD2'
    4、Left turning:[9, 21, 38] '#FFAB91' 5、Jumping:[33, 35] '#FFCC80'                   6、Climbing up:[26, 12]  '#4CAF50'
    7、Falling:[32]  '#C5E1A5'            8、Up search/Rising:[13, 36, 17, 18] '#78b778'  9、Grooming:[2, 39, 40]  '#F06292'
    10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#4FC3F7'                               11、Stepping:[3, 19]  '#FBE9E7'
    12、Sniffing:[28, 27, 14, 20, 29, 1]   '#00B8D4'                                     13、Sniffing pause:[4, 10, 30] '#9E9E9E'
    14、Rearing/Diving:[11, 25]  '#81C784'
"""


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


def pre_data(input_data, movement_label_num, special_time_start, special_time_end):
    # with open(file_path, 'rb') as f:
    csv_data = input_data

    label = csv_data.loc[:, 'new_label'].tolist()
    segBoundary = csv_data.loc[:, 'segBoundary'].tolist()

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


def one_hour_data(file_path, num):
    ten_min = pd.read_csv(file_path[num])  # 10min的 feature_space 数据

    twenty_min = pd.read_csv(file_path[num + 1])
    twenty_min_seg = twenty_min.loc[:, 'segBoundary'].tolist()
    twenty_min_seg = [x + ten_min.iloc[-1, 1] for x in twenty_min_seg]
    twenty_min['segBoundary'] = twenty_min_seg

    thirty_min = pd.read_csv(file_path[num + 2])
    thirty_min_seg = thirty_min.loc[:, 'segBoundary'].tolist()
    thirty_min_seg = [x + twenty_min.iloc[-1, 1] for x in thirty_min_seg]
    thirty_min['segBoundary'] = thirty_min_seg

    forty_min = pd.read_csv(file_path[num + 3])
    forty_min_seg = forty_min.loc[:, 'segBoundary'].tolist()
    forty_min_seg = [x + thirty_min.iloc[-1, 1] for x in forty_min_seg]
    forty_min['segBoundary'] = forty_min_seg

    fifty_min = pd.read_csv(file_path[num + 4])
    fifty_min_seg = fifty_min.loc[:, 'segBoundary'].tolist()
    fifty_min_seg = [x + forty_min.iloc[-1, 1] for x in fifty_min_seg]
    fifty_min['segBoundary'] = fifty_min_seg

    sixty_min = pd.read_csv(file_path[num + 5])
    sixty_min_seg = sixty_min.loc[:, 'segBoundary'].tolist()
    sixty_min_seg = [x + fifty_min.iloc[-1, 1] for x in sixty_min_seg]
    sixty_min['segBoundary'] = sixty_min_seg

    one_hour_data = pd.concat([ten_min, twenty_min, thirty_min, forty_min, fifty_min, sixty_min], axis=0)

    return one_hour_data


def data_combine(input_data, special_time_start, special_time_end):
    # special_time1 = special_time_start * 60 * 30
    # special_time2 = special_time_end * 60 * 30
    special_time1 = special_time_start
    special_time2 = special_time_end
    data = []
    for i in range(1, len(color_list) + 1):
        behavior = pre_data(input_data, i, special_time1, special_time2)
        data.append(behavior)
    return data


def one_hour_speed(file_path, num):
    ten_min = pd.read_csv(file_path[num])  # 10min的 feature_space 数据
    ten_min_x = ten_min.loc[2:, 'back'].tolist()
    ten_min_y = ten_min.loc[2:, 'back.1'].tolist()

    twenty_min = pd.read_csv(file_path[num + 1])
    twenty_min_x = twenty_min.loc[2:, 'back'].tolist()
    twenty_min_y = twenty_min.loc[2:, 'back.1'].tolist()

    thirty_min = pd.read_csv(file_path[num + 2])
    thirty_min_x = thirty_min.loc[2:, 'back'].tolist()
    thirty_min_y = thirty_min.loc[2:, 'back.1'].tolist()

    forty_min = pd.read_csv(file_path[num + 3])
    forty_min_x = forty_min.loc[2:, 'back'].tolist()
    forty_min_y = forty_min.loc[2:, 'back.1'].tolist()

    fifty_min = pd.read_csv(file_path[num + 4])
    fifty_min_x = fifty_min.loc[2:, 'back'].tolist()
    fifty_min_y = fifty_min.loc[2:, 'back.1'].tolist()

    sixty_min = pd.read_csv(file_path[num + 5])
    sixty_min_x = sixty_min.loc[2:, 'back'].tolist()
    sixty_min_y = sixty_min.loc[2:, 'back.1'].tolist()

    one_hour_x = ten_min_x + twenty_min_x + thirty_min_x + forty_min_x + fifty_min_x + sixty_min_x
    one_hour_x = list(np.array(one_hour_x, dtype='float'))

    one_hour_y = ten_min_y + twenty_min_y + thirty_min_y + forty_min_y + fifty_min_y + sixty_min_y
    one_hour_y = list(np.array(one_hour_y, dtype='float'))

    speed_all = []
    for i in range(len(one_hour_y) - 1):
        speed = np.sqrt(np.square(one_hour_x[i + 1] - one_hour_x[i]) + np.square(one_hour_y[i + 1] - one_hour_y[i]))
        speed_all.append(speed)

    speed_all.insert(-1, speed_all[-1])

    one_hour_x = pd.DataFrame(one_hour_x)
    one_hour_y = pd.DataFrame(one_hour_y)

    speed_all = pd.DataFrame(speed_all)
    # speed_all.columns = ['speed']

    one_hour_data_1 = pd.concat([one_hour_x, one_hour_y, speed_all], axis=1, join='inner')
    one_hour_data_1.columns = ['x', 'y', 'speed']

    return speed_all


if __name__ == '__main__':

    """
        state space 60min
    """
    # gender = 'male'
    # ExperimentTime = 'night'
    #
    # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang/',
    #              name="video_info.xlsx", column='roundTime', element=1)
    #
    # B = choose_data(a, column="gender", element=gender)
    # A = choose_data(B, column='ExperimentTime', element=ExperimentTime)
    #
    # C = choose_data(a, column="gender", element='female')
    # D = choose_data(C, column='ExperimentTime', element=ExperimentTime)
    #
    # df_night = pd.DataFrame(A, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_MD = []
    # for item in tqdm(df_night['Unique_serial_number']):
    #     csv_result3 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    #         name="rec-{}-G1-2022114230_Feature_Space".format(item))
    #     csv_MD.append(csv_result3[0])
    #
    # df_day = pd.DataFrame(D, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result3 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    #         name="rec-{}-G1-2022114230_Feature_Space".format(item))
    #     csv_FD.append(csv_result3[0])
    #
    # # num = 0
    # # ten_min = pd.read_csv(csv_FD[num])  # 10min的 feature_space 数据
    # #
    # # twenty_min = pd.read_csv(csv_FD[num + 1])
    # # twenty_min_seg = twenty_min.loc[:, 'segBoundary'].tolist()
    # # twenty_min_seg = [x + ten_min.iloc[-1, 1] for x in twenty_min_seg]
    # # twenty_min['segBoundary'] = twenty_min_seg
    # #
    # # thirty_min = pd.read_csv(csv_FD[num + 2])
    # # thirty_min_seg = thirty_min.loc[:, 'segBoundary'].tolist()
    # # thirty_min_seg = [x + twenty_min.iloc[-1, 1] for x in thirty_min_seg]
    # # thirty_min['segBoundary'] = thirty_min_seg
    # #
    # # forty_min = pd.read_csv(csv_FD[num + 3])
    # # forty_min_seg = forty_min.loc[:, 'segBoundary'].tolist()
    # # forty_min_seg = [x + thirty_min.iloc[-1, 1] for x in forty_min_seg]
    # # forty_min['segBoundary'] = forty_min_seg
    # #
    # # fifty_min = pd.read_csv(csv_FD[num + 4])
    # # fifty_min_seg = fifty_min.loc[:, 'segBoundary'].tolist()
    # # fifty_min_seg = [x + forty_min.iloc[-1, 1] for x in fifty_min_seg]
    # # fifty_min['segBoundary'] = fifty_min_seg
    # #
    # # sixty_min = pd.read_csv(csv_FD[num + 5])
    # # sixty_min_seg = sixty_min.loc[:, 'segBoundary'].tolist()
    # # sixty_min_seg = [x + fifty_min.iloc[-1, 1] for x in sixty_min_seg]
    # # sixty_min['segBoundary'] = sixty_min_seg
    # #
    # # one_hour_data = pd.concat([ten_min, twenty_min, thirty_min, forty_min, fifty_min, sixty_min], axis=0)
    #
    # Male_data = []
    # for num in range(0, len(csv_MD), 6):
    #     one_hour = one_hour_data(csv_MD, num)
    #     single_data = data_combine(one_hour, 0, 108000 - 5)
    #     Male_data.append(single_data)
    #
    # Female_data = []
    # for num in range(0, len(csv_FD), 6):
    #     one_hour = one_hour_data(csv_FD, num)
    #     single_data = data_combine(one_hour, 0, 108000 - 5)
    #     Female_data.append(single_data)
    #
    # fig = plt.figure(figsize=(20, 4), dpi=300)
    # ax = fig.add_subplot(111)
    # for j in range(len(Male_data)):
    #     for i in range(len(Male_data[0])):
    #         plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
    #         plt.broken_barh(Female_data[j][i], (j + 6, 0.8), facecolors=color_list[i])
    #
    # # for i in range(len(Female_data[6])):
    # #     plt.broken_barh(Female_data[6][i], (12, 0.8), facecolors=color_list[i])
    #
    # plt.axhline(y=5.9, linewidth=1.5, color='black', linestyle='--')
    # # plt.yticks([3, 9], ['Males', 'Females'], fontsize=12)
    # plt.xticks([0, 18000, 36000, 18000 * 3, 18000 * 4, 18000 * 5, 18000 * 6], ['0', '10', '20', '30', '40', '50', '60'],
    #            fontsize=20)
    # # plt.xticks([0, 9000, 18000], time_ticks, fontsize=12)
    # plt.yticks([])
    # plt.tight_layout()
    # # plt.axis('off')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # for axis in ['top', 'bottom', 'left', 'right']:
    #     ax.spines[axis].set_linewidth(1.5)
    # # plt.ion()
    # plt.show()
    # # plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/state_space/fang_figure/'
    # #             '{}.tiff'.format(ExperimentTime), dpi=300)
    # # plt.close()

    """
        velocity+state space 60min
    """

    gender = 'male'
    ExperimentTime = 'night'

    a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang/',
                 name="video_info.xlsx", column='roundTime', element=1)

    B = choose_data(a, column="gender", element=gender)
    A = choose_data(B, column='ExperimentTime', element=ExperimentTime)

    C = choose_data(a, column="gender", element='female')
    D = choose_data(C, column='ExperimentTime', element=ExperimentTime)

    df_night = pd.DataFrame(A, columns=["Unique_serial_number"])
    # data = df_day.values.tolist()
    csv_MD = []
    for item in tqdm(df_night['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
            name="rec-{}-G1-2022114230_Feature_Space".format(item))
        csv_MD.append(csv_result3[0])

    csv_MD_velocity = []
    for item in tqdm(df_night['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/Calibrated_3DSkeleton_replace/",
            name="rec-{}-G1-2022114230_Cali_Data3d".format(item))
        csv_MD_velocity.append(csv_result3[0])

    df_day = pd.DataFrame(D, columns=["Unique_serial_number"])
    # data = df_day.values.tolist()
    csv_FD = []
    for item in tqdm(df_day['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
            name="rec-{}-G1-2022114230_Feature_Space".format(item))
        csv_FD.append(csv_result3[0])

    csv_FD_velocity = []
    for item in tqdm(df_day['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/Calibrated_3DSkeleton_replace/",
            name="rec-{}-G1-2022114230_Cali_Data3d".format(item))
        csv_FD_velocity.append(csv_result3[0])

    Male_data = []
    for num in range(0, len(csv_MD), 6):
        one_hour = one_hour_data(csv_MD, num)
        single_data = data_combine(one_hour, 0, 108000 - 5)
        Male_data.append(single_data)

    Male_speed_data = pd.DataFrame()
    for i in range(0, len(csv_MD_velocity), 6):
        one_hour_speed_data_single = pd.DataFrame()
        one_hour_speed_data_single = one_hour_speed(csv_MD_velocity, i)
        Male_speed_data = pd.concat([Male_speed_data, one_hour_speed_data_single], axis=1)

    Female_data = []
    for num in range(0, len(csv_FD), 6):
        one_hour = one_hour_data(csv_FD, num)
        single_data = data_combine(one_hour, 0, 108000 - 5)
        Female_data.append(single_data)

    Female_speed_data = pd.DataFrame()
    for i in range(0, len(csv_FD_velocity), 6):
        one_hour_speed_data_single = pd.DataFrame()
        one_hour_speed_data_single = one_hour_speed(csv_FD_velocity, i)
        Female_speed_data = pd.concat([Female_speed_data, one_hour_speed_data_single], axis=1)

    fig, ax = plt.subplots(24, 1, figsize=(25, 10), dpi=300)
    fig.tight_layout()

    for x in range(1, 13, 2):
        ax[x].bar([i for i in range(len(Female_speed_data.iloc[:, int(x / 2)]))], Female_speed_data.iloc[:, int(x / 2)])
        ax[x].spines['top'].set_visible(False)
        ax[x].spines['bottom'].set_visible(False)
        ax[x].spines['left'].set_visible(False)
        ax[x].spines['right'].set_visible(False)
        ax[x].set_ylim(0, 15)
        ax[x].axes.xaxis.set_visible(False)
        ax[x].axes.yaxis.set_visible(False)

    for x in range(13, 24, 2):
        ax[x].bar([i for i in range(len(Male_speed_data.iloc[:, int((x - 12) / 2)]))],
                  Male_speed_data.iloc[:, int((x - 12) / 2)])
        ax[x].spines['top'].set_visible(False)
        ax[x].spines['bottom'].set_visible(False)
        ax[x].spines['left'].set_visible(False)
        ax[x].spines['right'].set_visible(False)
        ax[x].set_ylim(0, 15)
        ax[x].axes.xaxis.set_visible(False)
        ax[x].axes.yaxis.set_visible(False)

    for x in range(0, 12, 2):
        for i in range(len(Male_data[0])):
            ax[x].broken_barh(Male_data[int(x / 2)][i], (0, 0.8), facecolors=color_list[i])
            ax[x].spines['right'].set_visible(False)
            ax[x].spines['top'].set_visible(False)
            ax[x].spines['bottom'].set_visible(False)
            ax[x].spines['left'].set_visible(False)
            ax[x].set_yticks([])
            ax[x].axes.xaxis.set_visible(False)

    for x in range(12, 24, 2):
        for i in range(len(Male_data[0])):
            ax[x].broken_barh(Female_data[int((x - 12) / 2)][i], (0, 0.8), facecolors=color_list[i])
            ax[x].spines['right'].set_visible(False)
            ax[x].spines['top'].set_visible(False)
            ax[x].spines['bottom'].set_visible(False)
            ax[x].spines['left'].set_visible(False)
            ax[x].set_yticks([])
            ax[x].axes.xaxis.set_visible(False)

    # ax[0].set_xticks([0, 18000, 36000, 18000 * 3, 18000 * 4, 18000 * 5, 18000 * 6],
    #                  ['0', '10', '20', '30', '40', '50', '60'],
    #                  fontsize=20)

    # set the spacing between subplots
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.2,
                        hspace=0.2)

    plt.show()
    plt.savefig('D:/3D_behavior/test_v4.tiff', dpi=300)
    plt.close()

    # fig = plt.figure(figsize=(20, 4), dpi=300)
    # ax = fig.add_subplot(111)
    # for j in range(len(Male_data)):
    #     for i in range(len(Male_data[0])):
    #         plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
    #         plt.broken_barh(Female_data[j][i], (j + 6, 0.8), facecolors=color_list[i])
    #
    # # for i in range(len(Female_data[6])):
    # #     plt.broken_barh(Female_data[6][i], (12, 0.8), facecolors=color_list[i])
    #
    # plt.axhline(y=5.9, linewidth=1.5, color='black', linestyle='--')
    # # plt.yticks([3, 9], ['Males', 'Females'], fontsize=12)
    # plt.xticks([0, 18000, 36000, 18000 * 3, 18000 * 4, 18000 * 5, 18000 * 6], ['0', '10', '20', '30', '40', '50', '60'],
    #            fontsize=20)
    # # plt.xticks([0, 9000, 18000], time_ticks, fontsize=12)
    # plt.yticks([])
    # plt.tight_layout()
    # # plt.axis('off')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # for axis in ['top', 'bottom', 'left', 'right']:
    #     ax.spines[axis].set_linewidth(1.5)
    # # plt.ion()
    # plt.show()
    # # plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/state_space/fang_figure/'
    # #             '{}.tiff'.format(ExperimentTime), dpi=300)
    # # plt.close()
