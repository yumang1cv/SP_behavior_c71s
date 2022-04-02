"""
    figure plot
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

sys.path.append(os.path.abspath(".."))

# color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
#               '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
#               '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
#               '#93DEB1']
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


def pre_data(file_path, dataframe, num, state=""):
    # j = 0
    A = np.zeros((16, 16))

    fre_list = []
    looming_time = int(dataframe.at[num, state])
    start = looming_time - 0 * 30
    end = looming_time + 300 * 30

    df2 = pd.read_csv(file_path)

    data = df2.iloc[start:end, 1:2]
    for i in range(1, len(data)):
        if data.iloc[i, 0] != data.iloc[i - 1, 0]:
            a = data.iloc[i, 0] - 1
            b = data.iloc[i - 1, 0] - 1
            A[a, b] = A[a, b] + 1

    class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                  9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}

    for line in data.iloc[:, 0]:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict
    behavior_fre = list(class_type.values())
    A = normalize_2d(A)

    behavior_fre_norm = behavior_fre / np.linalg.norm(behavior_fre)
    for j in range(len(behavior_fre_norm)):
        # A[j, j] = behavior_fre_norm[j]
        A[j, j] = 0

    return A


def del_pre_data(data_list):
    del_index = []
    del_data = data_list
    t = 0
    for i in range(len(del_data)):
        if np.any(del_data[:, [i]]) == 0 and np.any(del_data[[i], :]) == 0:
            # print(i, t, i - t)
            del_index.append(i - t)
            t = t + 1

    for item in del_index:
        del_data = np.delete(del_data, item, 1)
        del_data = np.delete(del_data, item, 0)

    names = ['Right turning', 'Left turning', 'Sniffing', 'Walking', 'Trembling', 'Climbing', 'Falling',
             'Immobility', 'Paralysis', 'Standing', 'Trotting', 'Grooming', 'Flight', 'Running', 'LORR', 'Stepping']

    color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
                  '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
                  '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
                  '#93DEB1']
    for item in del_index:
        del names[item]
        del color_list[item]

    return del_data, names, color_list


# explicit function to normalize array
def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix
    return matrix


if __name__ == '__main__':
    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/BeAMapping",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal',
                 name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    for item in b['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/BeAMapping",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    # Male_list = []
    # Female_list = []
    # # pre_data(file_path, dataframe, num, state="")
    # for i in range(len(file_list_1)):
    #     sub_list1 = pre_data(file_list_1[i], a, i, state="looming_time4")
    #     Male_list.append(sub_list1)
    #
    # for j in range(len(file_list_2)):
    #     sub_list2 = pre_data(file_list_2[j], b, j, state="looming_time4")
    #     Female_list.append(sub_list2)
    #
    # data1 = np.zeros((16, 16))
    # for item in Male_list:
    #     Male_data = data1 + item
    #
    # for item in Female_list:
    #     Female_data = data1 + item
    # j = 1
    # A = np.zeros((16, 16))
    # start = 0 * 60 * 30
    # end = 10 * 60 * 30
    # fre_list = []
    # df2 = pd.read_csv(file_list_1[j])
    #
    # data = df2.iloc[start:end, 1:2]
    # for i in range(1, len(data)):
    #     if data.iloc[i, 0] != data.iloc[i - 1, 0]:
    #         a = data.iloc[i, 0] - 1
    #         b = data.iloc[i - 1, 0] - 1
    #         A[a, b] = A[a, b] + 1
    #
    # class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
    #               9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
    #
    # for line in data.iloc[:, 0]:
    #     if line not in class_type:
    #         class_type[line] = 0
    #
    #     else:
    #         class_type[line] += 1
    #
    # class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict
    # behavior_fre = list(class_type.values())
    # A = normalize_2d(A)
    #
    # behavior_fre_norm = behavior_fre / np.linalg.norm(behavior_fre)
    # for j in range(len(behavior_fre_norm)):
    #     # A[j, j] = behavior_fre_norm[j]
    #     A[j, j] = 0
    sub_list2 = pre_data(file_list_2[0], b, 0, state="looming_time1")
    # data = Male_data + Female_data

    del_data, names, colors = del_pre_data(sub_list2)

    color = ListedColormap(colors)
    fig = plt.figure(figsize=(5, 5), dpi=300)
    ax = fig.add_subplot(111)
    # chord_diagram(flux, names, gap=0.03, use_gradient=True, sort='distance', cmap=color,
    #               chord_colors=colors,
    #               rotate_names=True, fontcolor="grey", ax=ax, fontsize=10)
    chord_diagram(del_data, gap=0.03, use_gradient=True, sort='distance', cmap=color,
                  chord_colors=colors, fontcolor="grey", ax=ax, fontsize=10)

    # str_grd = "_gradient" if grads[0] else ""

    plt.xlabel('Time (s)', fontsize=15)
    plt.ylabel('Fraction', fontsize=15)
    plt.tight_layout()

    plt.show()
