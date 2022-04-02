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
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
from mpl_toolkits import mplot3d

matplotlib.use('Qt5Agg')

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
color_list = ['#D53624', '#FF6F91', '#FF9671', '#FFC75F', '#C34A36',
              '#00C2A8', '#00a3af', '#008B74', '#D5CABD', '#D65DB1',
              '#cb3a56', '#845EC2', '#B39CD0', '#98d98e']
"""
    Spontaneous Behavior Class Combine-Final
    1、Running:[15, 16, 22] '#D53624'     2、Fast walking/Trotting:[8] '#FF6F91'          3、Right turning:[7, 31, 34] '#FF9671'
    4、Left turning:[9, 21, 38] '#FFC75F' 5、Jumping:[33, 35] '#C34A36'                   6、Climbing up:[26, 12]  '#00C2A8'
    7、Falling:[32]  '#00a3af'            8、Up search/Rising:[13, 36, 17, 18] '#008B74'  9、Grooming:[2, 39, 40]  '#D5CABD'
    10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#D65DB1'                               11、Stepping:[3, 19]  '#cb3a56'
    12、Sniffing:[28, 27, 14, 20, 29, 1]   '#845EC2'                                     13、Sniffing pause:[4, 10, 30] '#B39CD0'
    14、Rearing/Diving:[11, 25]  '#98d98e'
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


def sort_data(list_1):
    male_std = []
    for i in range(len(list_1)):
        male_1 = np.std(list_1[i])
        male_std.append(male_1)

    dictionary = dict(zip(male_std, list_1))
    # dictionary1 = {l: sorted(m) for l, m in dictionary.items()}
    # dictionary = sorted(dictionary.keys())

    sort_list = []

    # convert the dictionary to list using dict.keys
    dictlist = list(dictionary.keys())
    # sort the list
    dictlist.sort()
    # Print the corresponding key and value by traversing this list
    for key in dictlist:
        # print key and value
        # print(key, ":", dictionary[key])
        sort_list.append(dictionary[key])

    return sort_list


def pre_data(file_list):
    list_one = []
    list_all = []

    for j in range(len(file_list)):
        df1 = pd.read_csv(file_list[j])
        # num = 1 * 1800
        # looming_time = int(dataframe.at[num, state])
        for i in range(0, 18000, 18000):
            # data = df1.iloc[i:i + 1800, 0:1]
            data = df1.iloc[i:i + 1800, 1:2]
            data1 = data.iloc[:, 0].tolist()

            class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                          9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
            # class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
            #               9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
            #               16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0,
            #               23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0,
            #               30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0,
            #               37: 0, 38: 0, 39: 0, 40: 0}
            for line in data1:
                if line not in class_type:
                    class_type[line] = 0
                else:
                    class_type[line] += 1

            list_1 = list(class_type.values())
            """
                Spontaneous Behavior Class Combine-Final
                1、Running:[15, 16, 22] '#D53624'     2、Fast walking/Trotting:[8] '#FF6F91'          3、Right turning:[7, 31, 34] '#FF9671'
                4、Left turning:[9, 21, 38] '#FFC75F' 5、Jumping:[33, 35] '#C34A36'                   6、Climbing up:[26, 12]  '#00C2A8'
                7、Falling:[32]  '#00a3af'            8、Up search/Rising:[13, 36, 17, 18] '#008B74'  9、Grooming:[2, 39, 40]  '#D5CABD'
                10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#D65DB1'                               11、Stepping:[3, 19]  '#cb3a56'
                12、Sniffing:[28, 27, 14, 20, 29, 1]   '#845EC2'                                     13、Sniffing pause:[4, 10, 30] '#B39CD0'
                14、Rearing/Diving:[11, 25]  '#98d98e'
            """
            """
            删除特定的行为
            """
            behavior_label = [x for x in range(1, 15)]
            save_label = [3, 6, 9, 10, 14]  # female night √
            # save_label = [2, 6, 9, 10, 12, 14]  # female day √
            # save_label = [6, 9, 10, 12, 14]  # male day ×
            # save_label = [3, 4, 6, 9, 10]  # male night √
            remove_list_index = list(set(behavior_label) - set(save_label))
            for item in remove_list_index:
                list_1[item - 1] = 0

            list_one.append(list_1)

        list_all.append(list_one)
        list_one = []

    list_1minute = []
    for j in range(len(list_all[0])):
        for i in range(1, len(file_list)):  # i:mice number
            # for i in range(0, 15):
            list_1minute.append(list_all[i][j])
            list_1minute = sort_data(list_1minute)

    return list_1minute


def PCA_reduce(data):  # PCA降维代码
    pca = PCA(n_components=3, svd_solver='full')
    data = np.array(data)
    data_pca = pca.fit(data.T)
    # print(pca.explained_variance_ratio_)
    print('降维效果：',
          pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1] + pca.explained_variance_ratio_[2])
    data_pca = data_pca.components_.T
    data_pca = pd.DataFrame(data_pca)

    return data_pca


if __name__ == '__main__':

    gender = 'female'
    ExperimentTime = 'night'
    state = 1
    i = 6
    # for i in range(2, 7):
    a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_circle/',
                 name="video_info.xlsx", column="gender", element=gender)

    b = choose_data(a, column='ExperimentTime', element=ExperimentTime)
    # 多条件筛选
    x = choose_data(b, column='split_number', element=state)  # split_number=1 not have ''
    df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    # data = df_day.values.tolist()
    csv_FD = []
    for item in tqdm(df_day['Unique_serial_number']):
        csv_result3 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result_circle/BeAMapping-Final/BeAMapping_replace/",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_FD.append(csv_result3[0])

    y = choose_data(b, column='split_number', element=i)
    df_night = pd.DataFrame(y, columns=["Unique_serial_number"])
    # data = df_night.values.tolist()
    csv_FN = []
    for item in tqdm(df_night['Unique_serial_number']):
        csv_result4 = search_csv(
            path=r"D:/3D_behavior/Spontaneous_behavior/result_circle/BeAMapping-Final/BeAMapping_replace/",
            name="rec-{}-G1-2021114230_Movement_Labels".format(item))
        csv_FN.append(csv_result4[0])

    list_10min = pre_data(csv_FD)
    list_20min = pre_data(csv_FN)

    list_10with60 = list_10min + list_20min


    """
        绘制3D scatter plot
    """
    # # PCA 降至3维
    # list_10min_PCA = PCA_reduce(list_10min)
    # list_20min_PCA = PCA_reduce(list_20min)
    #
    # x1, y1, z1, = list_10min_PCA[0].tolist(), list_10min_PCA[1].tolist(), list_10min_PCA[2].tolist()
    # x2, y2, z2, = list_20min_PCA[0].tolist(), list_20min_PCA[1].tolist(), list_20min_PCA[2].tolist()
    #
    # fig = plt.figure(figsize=(10, 7))
    # ax = plt.axes(projection="3d")
    # # Create Plot
    # ax.scatter3D(x1, y1, z1, marker='<', s=20, label='10min')
    # ax.scatter3D(x2, y2, z2, marker='o', s=20, label='60min')
    # # Add legend
    # ax.legend(loc=1)
    # # Show plot
    # plt.show()

    """
        绘制矩阵热图
    """
    X = np.corrcoef(list_10with60)

    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    ax = sns.heatmap(X, center=0, cmap="Spectral", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
    # ax = sns.heatmap(X, center=0, cmap="vlag", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
    # ax = sns.heatmap(X, center=0, cmap="RdBu", yticklabels=False, xticklabels=False)
    # ax.set_xticklabels(['Wakefulness', 'RoRR'])

    cbar = ax.collections[0].colorbar
    # here set the labelsize by 20
    cbar.ax.tick_params(labelsize=25)
    plt.tight_layout()
    plt.show()
    # plt.savefig("D:/3D_behavior/Spontaneous_behavior/result/analysis_result/state_correlation/v2/{}_{}time_{}0 "
    #             "with {}0min_v3.tiff".format(gender, ExperimentTime, state, i), dpi=300)
    # plt.close(fig)

    # list_10min = []
    # list_20min = []
    # list_10with60 = []

    # fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    # Z = linkage(list_10with60, method='ward')
    # dendro = dendrogram(Z)
    # plt.xticks(fontsize=15)
    # plt.tight_layout()
    # plt.show()

    """
    Arousal Analysis
    """
    # a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all',
    #              name="video_info.xlsx", column="looming_time1", state_name="Female_Wakefulness")  # Male_Wakefulness
    #
    # file_list_1 = []
    # for item in a['Video_name'][0:8]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_1.append(file_list1)
    # file_list_1 = list(np.ravel(file_list_1))
    #
    # b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all', name="video_info.xlsx",
    #              column="looming_time1", state_name="Female_RoRR")  # Female_Wakefulness
    #
    # file_list_2 = []
    # for item in b['Video_name'][0:8]:
    #     item = item.replace("-camera-0", "")
    #     file_list1 = search_csv(
    #         path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/BeAMapping/BeAMapping_replace",
    #         name="{}_Movement_Labels".format(item))
    #     file_list_2.append(file_list1)
    # file_list_2 = list(np.ravel(file_list_2))
    #
    # Male_list = []
    # for i in range(len(file_list_1)):
    #     sub_list1 = pre_data(file_list_1[i], a, i, state="looming_time1")
    #     # print(sub_list1)
    #     Male_list.append(sub_list1)
    # Male_list = sort_data(Male_list)
    #
    # Female_list = []
    # for i in range(len(file_list_2)):
    #     sub_list2 = pre_data(file_list_2[i], b, i, state="looming_time1")
    #     # print(sub_list2)
    #     Female_list.append(sub_list2)
    # Female_list = sorted(Female_list)
    # # Female_list = sort_data(Female_list)
    #
    # Female_list2 = []
    # for i in range(len(file_list_2)):
    #     sub_list3 = pre_data(file_list_2[i], b, i, state="looming_time2")
    #     # print(sub_list2)
    #     Female_list2.append(sub_list3)
    # Female_list2 = sort_data(Female_list2)
    #
    # Female_list3 = []
    # for i in range(len(file_list_2)):
    #     sub_list4 = pre_data(file_list_2[i], b, i, state="looming_time3")
    #     # print(sub_list2)
    #     Female_list3.append(sub_list4)
    # # Female_list3 = sort_data(Female_list3)
    #
    # # all_list = Male_list + Female_list + Female_list2 + Female_list3
    # all_list = Male_list + Female_list3
    # # X = np.corrcoef(all_list)
    # # ax = sns.heatmap(X, center=0, cmap="YlGnBu")
    #
    # # sort_list = sort_data(all_list)
    # # x_ticks = ['', '', '', 'Wakefulness', '', '', '', '', '', '', 'RoRR', '', '', '', ]
    # # y_ticks = ['Wakefulness', 'RoRR']
    # X = np.corrcoef(all_list)
    # fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    # # ax = sns.heatmap(X, center=0, cmap="Spectral", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
    # ax = sns.heatmap(X, center=0, cmap="vlag", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
    # # ax.set_xticklabels(['Wakefulness', 'RoRR'])
    #
    # cbar = ax.collections[0].colorbar
    # # here set the labelsize by 20
    # cbar.ax.tick_params(labelsize=25)
    # plt.tight_layout()
