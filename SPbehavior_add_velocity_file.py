# %%
# 徐阳
# 开发时间：2021/9/11 20:01
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import matplotlib
from tqdm import tqdm

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
#     1、Running:[15, 16, 35, 22]         2、Right turning:[7, 31, 34]       3、Left turning:[9, 21]
#     4、Walking:[8, 18, 23, 24, 37]      5、Trotting:[3, 5, 6, 17, 19]      6、Rearing:[12, 26]
#     7、Sniffing:[1, 4, 10, 13, 14, 20, 27, 28, 29, 30]                     8、Grooming:[39, 40]
#     9、Diving:[11, 25]                  10、Rising:[2]                     11、Hunching:[36]
#     12、Falling:[32]                    13、Jumping:[33]                   14、Stepping:[38]
#
#     Right Sniffing:[1, 4, 13, 20, 28, 30]                            Right Sniffing:[14, 27, 29]
#     Immobility:{7、Sniffing:[1, 4, 6, 10, 14, 28, 29, 30],8、 Grooming:[39, 40], 9、Diving:[11, 25], 10、Rising:[2]}
# """
color_list = ['#FF9671', '#FFC75F', '#D65DB1', '#FF6F91', '#F9F871',
              '#A178DF', '#DCB0FF', '#FACCFF', '#00D2FC', '#4FFBDF',
              '#FF8066', '#00C2A8', '#008B74', '#845EC2']
"""
    Spontaneous Behavior Class Combine-Final
    1、Running:[15, 16, 22] '#FF9671'     2、Fast walking/Trotting:[8] '#FFC75F'          3、Right turning:[7, 31, 34] '#D65DB1'
    4、Left turning:[9, 21, 38] '#FF6F91' 5、Jumping:[33, 35] '#F9F871'                   6、Climbing up:[26, 12]  '#A178DF'
    7、Falling:[32]  '#DCB0FF'            8、Up search/Rising:[13, 36, 17, 18] '#FACCFF'  9、Grooming:[2, 39, 40]  '#00D2FC'
    10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#4FFBDF'                               11、Stepping:[3, 19]  '#FF8066'
    12、Sniffing:[28, 27, 14, 20, 29, 1]   '#00C2A8'                                     13、Sniffing pause:[4, 10, 30] '#008B74'
    14、Rearing/Diving:[11, 25]  '#845EC2'
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


def velocity_to_csv(file_path1, file_path2, num):
    with open(file_path1[num], 'rb') as f:
        df = pd.read_csv(f)
        df1 = df.iloc[2:, 36:39]  # select back vector
        df1 = df1.astype(float)
        v = df1.diff()
        v_x = v.iloc[1:, 0].tolist()
        v_y = v.iloc[1:, 1].tolist()
        v_z = v.iloc[1:, 2].tolist()
        v_list = []
        for j in range(0, len(v_x)):
            absolute_v = np.sqrt(np.square(v_x[j]) + np.square(v_y[j]) + +np.square(v_z[j]))  # Cali absolute velocity
            # absolute_v = smooth(absolute_v, 30)
            v_list.append(absolute_v)
        v_list.insert(0, np.mean(v_list))
        v_list.insert(-1, np.mean(v_list))

    with open(file_path2[num], 'rb') as f:
        df1_move = pd.read_csv(f)
        df1_move['velocity'] = v_list[1:]
        df1_move.to_csv(file_path2[num], index=False)

    return


if __name__ == '__main__':
    # a = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
    #              name="video_info.xlsx", column="gender", element="male")
    a = read_csv(path=r'D:\\3D_behavior\\Spontaneous_behavior\\result',
                 name="video_info.xlsx", column="gender", element="male")

    df_day = pd.DataFrame(a, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    csv_FD = []
    csv_FD_move = []
    for item in tqdm(df_day['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result/3Dskeleton_result_all/Calibrated_3DSkeleton_colsupdate"
                 r"/Calibrated_3DSkeleton_colsupdate_rename/",
            name="rec-{}-G1-2021114230_Cali_Data3d".format(item))
        csv_FD.append(csv_result3[0])

        csv_result1 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result/BeAMapping/BeAMapping_replace/",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_FD_move.append(csv_result1[0])

    for i in range(len(csv_FD)):
        velocity_to_csv(csv_FD, csv_FD_move, i)

    # with open(csv_FN[0], 'rb') as f:
    #     df = pd.read_csv(f)
    #     df1 = df.iloc[2:, 36:39]  # select back vector
    #     df1 = df1.astype(float)
    #     v = df1.diff()
    #     v_x = v.iloc[1:, 0].tolist()
    #     v_y = v.iloc[1:, 1].tolist()
    #     v_z = v.iloc[1:, 2].tolist()
    #     v_list = []
    #     for j in range(0, len(v_x)):
    #         absolute_v = np.sqrt(np.square(v_x[j]) + np.square(v_y[j]) + +np.square(v_z[j]))  # Cali absolute velocity
    #         # absolute_v = smooth(absolute_v, 30)
    #         v_list.append(absolute_v)
    #     v_list.insert(0, np.mean(v_list))
    #     v_list.insert(-1, np.mean(v_list))
    #
    # with open(csv_FN_move[0], 'rb') as f:
    #     df1_move = pd.read_csv(f)
    #
    #     df1_move['velocity'] = v_list[1:]
    #     df1_move.to_csv(csv_FN_move[0], index=False)
    # csv_FD_data = []
    # for i in range(0, 7):
    # # for i in range(0, len(csv_FD)):
    #     single_data = data_combine(csv_FD[i])
    #     csv_FD_data.append(single_data)
    #
    # csv_FN_data = []
    # # for i in range(0, len(csv_FN)):
    # for i in range(1, 8):
    #     single_data = data_combine(csv_FN[i])
    #     csv_FN_data.append(single_data)
    #
    # Male_data = csv_FD_data
    # Female_data = csv_FN_data
    #
    # # fig = plt.figure(figsize=(15, 3), dpi=300)
    # fig = plt.figure(figsize=(4, 2), dpi=300)
    # ax = fig.add_subplot(111)
    # for j in range(len(Male_data)):
    #     for i in range(len(Male_data[0])):
    #         # plt.broken_barh(Male_data[j][i], (j, 0.8), facecolors=color_list[i])
    #         plt.broken_barh(Female_data[j][i], (j + 7, 0.8), facecolors=color_list[i])
    #
    # # for i in range(len(Female_data[0])):
    # #     plt.broken_barh(Female_data[0][i], (0, 0.8), facecolors=color_list[i])
    #
    # # plt.axhline(y=6.9, linewidth=1.5, color='black', linestyle='--')
    # # plt.yticks([4, 11], ['Males', 'Females'], fontsize=12)
    # # plt.yticks([4], ['Females daytime'], fontsize=8, rotation=90)
    # # plt.xticks([0, 9000], ['0', '5'], fontsize=12)
    # plt.yticks([])
    # plt.xticks([0, 9000, 18000], ['30', '35', '40'])
    # # plt.xticks([0, 9000, 18000, 27000, 36000, 45000], ['0', '5', '10', '15', '20', '25'], fontsize=12)
    # plt.tight_layout()
    # # plt.axis('off')
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # for axis in ['top', 'bottom', 'left', 'right']:
    #     ax.spines[axis].set_linewidth(1.5)
    # plt.show()
