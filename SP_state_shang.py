# %%
# 徐阳
# 开发时间：2021/9/11 20:01
import numpy as np
import pandas as pd
import os
from sklearn.decomposition import PCA

color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
              '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
              '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
              '#93DEB1']
"""
    Arousal Behavior Class Combine
    1、Right turning:[1]  (#845EC2)             2、Left turning:[26]  (#B39CD0)
    3、Sniffing:[2, 4, 10, 11, 12, 16, 22, 25]  (#D65DB1)
    4、Walking:[3, 6, 7, 19, 30]  (#4FFBDF)     5、Trembling:[5, 15, 32, 40]  (#FFC75F)
    6、Climbing:[8, 29]   (#D5CABD)             7、Falling:[9]         (#B0A8B9)
    8、Immobility:[13, 20, 33, 34] (#FF6F91)    9、Paralysis:[14, 35]  (#F9F871)
    10、Standing:[17]      (#D7E8F0)            11、Trotting:[18, 31]  (#60DB73)
    12、Grooming:[21]      (#E8575A)            13、Flight:[23, 38]    (#008B74)
    14、Running:[24, 36]   (#00C0A3)            15、LORR:[27, 28, 39]  (#FF9671)
    16、Stepping:[37]      (#93DEB1)
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


def read_csv(path='.', name="", column="", element="", state_name=""):
    """
        column[0]: file_name      column[1]:第一次looming时间点
        sheet1：Fwake状态          sheet2：Frorr状态
    """
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        csv_data = pd.read_excel(f, sheet_name=state_name)

    # df1 = csv_data.set_index([column])  # 选取某一列数据
    # sel_data = df1.loc[element]  # 根据元素提取特定数据

    return csv_data


def pre_data(file_path, start_time, end_time):
    fre = 1
    start = start_time * 60 * 30
    end = end_time * 60 * 30
    fre_list = []
    # j = 3
    for j in range(len(file_path)):
        df1 = pd.read_csv(file_path[j])

        data = df1.iloc[start:end, 1:2]
        for i in range(1, len(data)):
            if data.iloc[i, 0] != data.iloc[i - 1, 0]:
                fre = fre + 1
        fre_list.append(fre)
        # print('第{}个文件的熵值为:'.format(j), fre)
        fre = 1

    return fre_list


def pre_looming_data(file_path, dataframe, state=""):

    fre = 1
    fre_list = []
    # j = 3
    for j in range(len(file_path)):
        looming_time = int(dataframe.at[j, state])
        df1 = pd.read_csv(file_path[j])

        data = df1.iloc[looming_time - 5 * 30:looming_time + 115 * 30, 1:2]
        for i in range(1, len(data)):
            if data.iloc[i, 0] != data.iloc[i - 1, 0]:
                fre = fre + 1
        fre_list.append(fre)
        # print('第{}个文件的熵值为:'.format(j), fre)
        fre = 1

    return fre_list


if __name__ == '__main__':
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
                 name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    # Male_list = pre_data(file_list_1, 20, 25)
    # Female_list = pre_data(file_list_2, 20, 25)

    Male_list = pre_looming_data(file_list_1, a, state="looming_time1")
    Female_list = pre_looming_data(file_list_2, b, state="looming_time1")
    print(Male_list)
    print(Female_list)
    # fre = 1
    # start = 20 * 60 * 30
    # end = 25 * 60 * 30
    # fre_list = []
    # # j = 3
    # for j in range(len(file_list_2)):
    #     df1 = pd.read_csv(file_list_2[j])
    #
    #     data = df1.iloc[start:end, 1:2]
    #     for i in range(1, len(data)):
    #         if data.iloc[i, 0] != data.iloc[i - 1, 0]:
    #             fre = fre + 1
    #     fre_list.append(fre)
    #     # print('第{}个文件的熵值为:'.format(j), fre)
    #     fre = 1

    # # explicit function to normalize array
    # def normalize(arr, t_min, t_max):
    #     norm_arr = []
    #     diff = t_max - t_min
    #     diff_arr = max(arr) - min(arr)
    #     for i in arr:
    #         temp = (((i - min(arr)) * diff) / diff_arr) + t_min
    #         norm_arr.append(temp)
    #     return norm_arr
    #
    #
    # range_to_normalize = (-1, 1)
    # normalized_array_1d = normalize(newX,
    #                                 range_to_normalize[0],
    #                                 range_to_normalize[1])
