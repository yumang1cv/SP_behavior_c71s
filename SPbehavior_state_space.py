# %%
# 徐阳
# 开发时间：2021/9/11 20:01
import pandas as pd
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
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

# color_list = ['#D53624', '#FF6F91', '#FF9671', '#FFC75F', '#C34A36',
#               '#00C2A8', '#00a3af', '#008B74', '#D5CABD', '#D65DB1',
#               '#cb3a56', '#845EC2', '#B39CD0', '#98d98e']
# """
#     Spontaneous Behavior Class Combine-Final
#     1、Running:[15, 16, 22] '#D53624'     2、Fast walking/Trotting:[8] '#FF6F91'          3、Right turning:[7, 31, 34] '#FF9671'
#     4、Left turning:[9, 21, 38] '#FFC75F' 5、Jumping:[33, 35] '#C34A36'                   6、Climbing up:[26, 12]  '#00C2A8'
#     7、Falling:[32]  '#00a3af'            8、Up search/Rising:[13, 36, 17, 18] '#008B74'  9、Grooming:[2, 39, 40]  '#D5CABD'
#     10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#D65DB1'                               11、Stepping:[3, 19]  '#cb3a56'
#     12、Sniffing:[28, 27, 14, 20, 29, 1]   '#845EC2'                                     13、Sniffing pause:[4, 10, 30] '#B39CD0'
#     14、Rearing/Diving:[11, 25]  '#98d98e'
# """

color_list = ['#fd7f69', '#fa9b8b', '#64b0fb', '#87c0f9', '#fcb83c',
              '#3e9a3e', '#95c695', '#78b778', '#fc3cfc', '#41a0fd',
              '#fddc2f', '#fae15e', '#8b8b8b', '#5ca95c']
"""
    Spontaneous Behavior Class Combine-YJL
    1、Running:[15, 16, 22] '#fd7f69'     2、Fast walking/Trotting:[8] '#fa9b8b'          3、Right turning:[7, 31, 34] '#64b0fb'
    4、Left turning:[9, 21, 38] '#87c0f9' 5、Jumping:[33, 35] '#fcb83c'                   6、Climbing up:[26, 12]  '#3e9a3e'
    7、Falling:[32]  '#95c695'            8、Up search/Rising:[13, 36, 17, 18] '#78b778'  9、Grooming:[2, 39, 40]  '#fc3cfc'
    10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#41a0fd'                               11、Stepping:[3, 19]  '#fddc2f'
    12、Sniffing:[28, 27, 14, 20, 29, 1]   '#fae15e'                                     13、Sniffing pause:[4, 10, 30] '#8b8b8b'
    14、Rearing/Diving:[11, 25]  '#5ca95c'
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


def pre_data(file_path, movement_label_num, special_time_start, special_time_end):
    with open(file_path, 'rb') as f:
        csv_data = pd.read_csv(f)

    label = csv_data.loc[:, 'new_label']
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
    for i in range(1, len(color_list)+1):
        behavior = pre_data(file_path, i, special_time1, special_time2)
        data.append(behavior)
    return data


if __name__ == '__main__':
    a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_circle/',
                 name="video_info.xlsx", column="gender", element="female")

    A = choose_data(a, column='ExperimentTime', element='day')

    # 多条件筛选
    x = choose_data(A, column='split_number', element=1)  # split_number=1 not have ''
    df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    # data = df_day.values.tolist()
    csv_FD = []
    for item in tqdm(df_day['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result_circle/BeAMapping-Final/BeAMapping_replace/",
            name="rec-{}-G1-2021114230_Feature_Space".format(item))
        csv_FD.append(csv_result3[0])

    y = choose_data(A, column='split_number', element=1)  # split_number=1 not have ''
    df_night = pd.DataFrame(y, columns=["Unique_serial_number"])
    # data = df_night.values.tolist()
    csv_FN = []
    for item in tqdm(df_night['Unique_serial_number']):
        csv_result4 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result_circle/BeAMapping-Final/BeAMapping_replace/",
            name="rec-{}-G1-2021114230_Feature_Space".format(item))
        csv_FN.append(csv_result4[0])

    Male_data = []
    for i in range(0, 7):
        single_data = data_combine(csv_FD[i], 0, 17998)
        Male_data.append(single_data)
    # single_data = data_combine(file_list_1[0], 0, 25)
    # Male_data.append(single_data)

    Female_data = []
    for i in range(1, 8):
        single_data = data_combine(csv_FN[i], 0, 17998)
        # print('第{}个文件sucess'.format(i))
        Female_data.append(single_data)
    #
    # # plt.figure(figsize=(5, 1), dpi=300)
    # fig, ax = plt.subplot()
    fig = plt.figure(figsize=(5, 3), dpi=300)
    ax = fig.add_subplot(111)
    for j in range(len(Male_data)):
        for i in range(len(Male_data[0])):
            plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
            plt.broken_barh(Female_data[j][i], (j + 6, 0.8), facecolors=color_list[i])

    # for i in range(len(Female_data[6])):
    #     plt.broken_barh(Female_data[6][i], (12, 0.8), facecolors=color_list[i])

    # plt.axhline(y=5.9, linewidth=1.5, color='black', linestyle='--')
    # plt.yticks([3, 9], ['Males', 'Females'], fontsize=12)
    plt.xticks([0, 9000, 18000], ['50', '55', '60'], fontsize=12)
    plt.yticks([])
    plt.tight_layout()
    # plt.axis('off')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.5)
    # plt.ion()
    plt.show()