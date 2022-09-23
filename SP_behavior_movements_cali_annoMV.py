# -*- coding:utf-8 -*-
# @FileName  :SP_behavior_movements_cali_annoMV.py
# @Time      :2022/9/1 10:22
# @Author    :XuYang
import os
import pandas as pd
from collections import defaultdict
import numpy as np
import substring
from tqdm import tqdm

movement_index = {'running': 1,
                  'walking': 2,
                  'right_turning': 3,
                  'left_turning': 4,
                  'stepping': 5,
                  'climb_up': 6,
                  'rearing': 7,
                  'hunching': 8,
                  'rising': 9,
                  'grooming': 10,
                  'sniffing': 11,
                  'pause': 12,
                  'jumping': 13,
                  }

color_dict = {'running': '#F44336',
              'walking': '#FF5722',
              'right_turning': '#FFCDD2',
              'left_turning': '#FFAB91',
              'stepping': '#BCAAA4',
              'climb_up': '#43A047',
              'rearing': '#66BB6A',
              'hunching': '#81C784',
              'rising': '#9CCC65',
              'grooming': '#AB47BC',
              'sniffing': '#26A69A',
              'pause': '#B0BEC5',
              'jumping': '#FFB74D',
              }
movement_label = list(movement_index.keys())


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


def open_data(datapath, file_type):
    file_list = []
    path_list = os.listdir(datapath)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(datapath, filename))

    return file_list


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


def read_single_file(sub_file_path):
    """
    read single file to dict
    """
    class_type = {}
    with open(sub_file_path) as f:  # read single file to dict
        reader = f
        for line in reader:
            line = substring.substringByChar(line, startChar=",")
            line = line[1:2]
            line = line.strip('\n')
            # sorted(class_type.keys())
            if line not in class_type:
                class_type[str(line)] = 0

            else:
                class_type[str(line)] += 1
        # print("Original dict", class_type)

        class_type_int = {int(k): int(v) for k, v in class_type.items()}  # data str to int
        class_type_sorted = dict(sorted(class_type_int.items(), key=lambda item: item[0]))  # sort dict
        # print("After sorted dict:", class_type_sorted)

    return class_type_sorted


def read_several_file(file_path):  # several file variance analysis
    """
    Statistics several file data to one dict
    """
    class_fre = []
    for file in file_path:
        class_frequency = read_single_file(file)
        class_fre.append(class_frequency)
        # print("总共有   ", len(class_frequency), "  个类别")

    class_fre_result = defaultdict(list)
    for element in class_fre:
        for key, value in element.items():
            class_fre_result[key].append(value)

    class_fre_result_sorted = dict(sorted(class_fre_result.items(), key=lambda item: item[0]))  # sort dict

    # print(class_fre_result_sorted)

    return class_fre_result_sorted


def several_file_sum(sev_file_dict):  # several file mean analysis
    """
    Sum dict all value and normalization
    """
    for key in sev_file_dict:  # sum
        sev_file_dict[key] = sum(sev_file_dict[key])

    factor = 1.0 / sum(sev_file_dict.values())  # normalization
    for k in sev_file_dict:
        sev_file_dict[k] = sev_file_dict[k] * factor

    print("结果为：", sev_file_dict)
    print('\n')

    return sev_file_dict


def single_mouse_behavior(file_path, start_index, delay_time):
    behavior_all = []
    for item in tqdm(file_path):
        f = pd.read_csv(item)
        class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                      9: 0, 10: 0, 11: 0, 12: 0, 13: 0}
        """
            pandas计算步骤
        """
        for i in range(start_index * 1800, start_index + delay_time * 1800 - 65):
            if int(f.iloc[i, 5:6]) not in class_type:
                class_type[int(f.iloc[i, 5:6])] = 0
            else:
                class_type[int(f.iloc[i, 5:6])] += 1
        # print(class_type)
        behavior_fre = list(class_type.values())
        behavior_all.append(behavior_fre)
        # print('{} ---> 已完成计算'.format(item))
        # print(behavior_all)

    final_array = np.array(behavior_all)
    final_data = pd.DataFrame(final_array)
    final_data = final_data.set_axis(movement_label, axis='columns')
    final_data = final_data.set_axis(mouse_label, axis='index')

    return final_data


def single_minute_fre(file_path, delay_time):
    behavior_all = []
    # x = csv_FD[0]
    # for x in csv_FD:
    delay_time = delay_time * 1800
    for time in range(0, 18000, delay_time):
        behavior_item = []
        for file in file_path:
            class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                          9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
            f = pd.read_csv(file)
            # time = 0
            f = f.iloc[time:time + delay_time - 5]
            # behavior_fre = []
            for i in range(0, len(f)):
                if int(f.iloc[i, 1:2]) not in class_type:
                    class_type[int(f.iloc[i, 1:2])] = 0
                else:
                    class_type[int(f.iloc[i, 1:2])] += 1
                # print(x, class_type)
            behavior_fre = list(class_type.values())
            # print(behavior_fre)
            behavior_item.append(behavior_fre)
        behavior_all.append(behavior_item)
        # print(behavior_all)
        # print('第{}分钟已计算'.format((time / 1800) + 1))
        print('第{}分钟已计算'.format((time / 1800)))

    mean_all = []
    for j in range(len(behavior_all)):
        mean_list = []
        data = behavior_all[j]
        data = pd.DataFrame(data)
        data = data.T
        for i in range(len(data)):
            mean_list.append(np.mean(data.iloc[i]))
        mean_all.append(mean_list)

    return mean_all


# explicit function to normalize array
def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix
    return matrix


if __name__ == '__main__':

    """
        单组分分析   Round1/2/3、Female_night、Female_day、Male_night、Male_day
    """
    ExperimentTime = 'night'
    gender = 'male'
    Round_time = 3
    origin_seg = 6
    a = read_csv(path=r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new/',
                 name="02_animal_info_square.xlsx", column='camera_type', element='RGB')

    # 多条件筛选
    # x = choose_data(a, column='gender', element=gender)   # 选取实验性别
    y = choose_data(a, column='ExperimentTime', element=ExperimentTime)  # 选取实验时间
    # z = choose_data(y, column='origin_seg', element=origin_seg)   # 选取实验时段

    df_day = pd.DataFrame(y, columns=["re_seg_Index"]).drop_duplicates()
    # data = df_day.values.tolist()
    csv_FD = []
    for item in tqdm(df_day['re_seg_Index']):
        csv_result3 = search_csv(
            path=r"D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new\anno_MV_csv/",
            name="rec-{}-G1-anno_Movement_Labels".format(item))
        csv_FD.append(csv_result3[0])

    mouse_label = []
    for item in df_day['re_seg_Index']:
        mouse_label.append('mouse_{}'.format(item))

    # behavior_all = []
    # for item in csv_FD:
    #     f = pd.read_csv(item)
    #     class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
    #                   9: 0, 10: 0, 11: 0, 12: 0, 13: 0}
    #     """
    #         pandas计算步骤
    #     """
    #     for i in range(len(f)):
    #         if int(f.iloc[i, 5:6]) not in class_type:
    #             class_type[int(f.iloc[i, 5:6])] = 0
    #         else:
    #             class_type[int(f.iloc[i, 5:6])] += 1
    #     # print(class_type)
    #     behavior_fre = list(class_type.values())
    #     behavior_all.append(behavior_fre)
    #     print('{}已完成计算'.format(item))
    #     # print(behavior_all)
    #
    # final_array = np.array(behavior_all)
    # final_data = pd.DataFrame(final_array)
    #
    # final_data = final_data.set_axis(movement_label, axis='columns')
    # final_data = final_data.set_axis(mouse_label, axis='index')

    # output_data = single_mouse_behavior(csv_FD, 0, 5)
    # output_data.to_excel(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre'
    #                      r'\{}_{}_{}.xlsx'.format(gender, ExperimentTime, origin_seg))

    behavior_mean = []
    for delay in range(0, 60):
        output_data = single_mouse_behavior(csv_FD, delay, delay + 1)
        col_mean = output_data.mean(axis=0)
        output_mean = []
        for item in col_mean:
            output_mean.append(item)
        print(output_mean)
        behavior_mean.append(output_mean)
        output_data.empty
        print('第{}分钟结果已计算'.format(delay + 1))

    print('输出的为{}时间结果'.format(ExperimentTime))

    behavior_mean = pd.DataFrame(behavior_mean)
    change = behavior_mean.diff(periods=1, axis=0)
    behavior_mean.columns = movement_label
    behavior_mean.to_excel(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre'
                           r'\{}_time_single_minute.xlsx'.format(ExperimentTime), index=False)

    """
        多组分分析   Four group:F-NDN、M-NDN、F-DND、M-DND
    """
    # ExperimentTime = 'night'
    # gender = 'female'
    # Round = 1
    # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    #              name="video_info.xlsx", column="ExperimentTime", element=ExperimentTime)
    #
    # # 多条件筛选
    # x = choose_data(a, column='gender', element=gender)
    # y = choose_data(x, column='roundTime', element=Round)
    # df_day = pd.DataFrame(y, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result3 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FD.append(csv_result3[0])
    #
    # data_1 = single_mouse_behavior(csv_FD)
    #
    # a1 = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    #               name="video_info.xlsx", column="ExperimentTime", element='day')
    #
    # # 多条件筛选
    # x1 = choose_data(a1, column='gender', element=gender)
    # y1 = choose_data(x1, column='roundTime', element=2)
    # df_day = pd.DataFrame(y1, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD1 = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result31 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FD1.append(csv_result31[0])
    #
    # data_2 = single_mouse_behavior(csv_FD1)
    #
    # y2 = choose_data(x, column='roundTime', element=3)
    # df_day = pd.DataFrame(y2, columns=["Unique_serial_number"])
    # # data = df_day.values.tolist()
    # csv_FD2 = []
    # for item in tqdm(df_day['Unique_serial_number']):
    #     csv_result32 = search_csv(
    #         path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    #         name="rec-{}-G1-2021114230_Movement_Labels".format(item))
    #     csv_FD2.append(csv_result32[0])
    #
    # data_3 = single_mouse_behavior(csv_FD2)
    # data_all = pd.concat([data_1, data_2, data_3], ignore_index=True)
    # data_all.to_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/'
    #                 'F_NDN_group2.csv')

    """
        活跃曲线数据预处理
    """
    # delay_time = 10
    # ExperimentTime = 'night'
    # gender = 'male'
    # # Round = 1
    # # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    # #              name="video_info.xlsx", column='roundTime', element=1)
    # # type = 'inf'
    # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    #              name="video_info.xlsx", column='type', element='inf')
    # # 多条件筛选
    # all_time_list = []
    # b = choose_data(a, column='ExperimentTime', element=ExperimentTime)
    # c = choose_data(b, column='gender', element=gender)
    # for i in range(1, 7, 1):
    #     x = choose_data(c, column='split_number', element=i)
    #     # y = choose_data(x, column='roundTime', element=Round)
    #     df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    #     # data = df_day.values.tolist()
    #     csv_FD = []
    #     for item in tqdm(df_day['Unique_serial_number']):
    #         if item > 450:
    #             csv_result3 = search_csv(
    #                 path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    #                 name="rec-{}-G1-2022114230_Movement_Labels".format(item))
    #             csv_FD.append(csv_result3[0])
    #
    #     ten_min_list = single_minute_fre(csv_FD, delay_time)
    #     print('前{}0分钟已处理结束'.format(i))
    #     all_time_list.append(ten_min_list)
    #
    # list_all = all_time_list
    # list_all = list(np.ravel(list_all))
    # list_all = np.array_split(list_all, len(list_all) / 14)
    # list_all = pd.DataFrame(list_all)
    # list_all = np.array(list_all)
    # list_all = normalize_2d(list_all)
    # list_all = pd.DataFrame(list_all)
    # list_all.to_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline'
    #                 '/fang_data/{}-{}_round1_{}min_inf.csv'.format(gender, ExperimentTime, delay_time))

    # delay_time = 2
    # ExperimentTime = 'night'
    # gender = 'female'
    # # Round = 1
    # # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    # #              name="video_info.xlsx", column='roundTime', element=1)
    # # type = 'inf'
    # a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
    #              name="video_info.xlsx", column='ExperimentTime', element=ExperimentTime)
    # # 多条件筛选
    # all_time_list = []
    # # b = choose_data(a, column='ExperimentTime', element=ExperimentTime)
    # c = choose_data(a, column='gender', element=gender)
    # for i in range(1, 7, 1):
    #     x = choose_data(c, column='split_number', element=i)
    #     # y = choose_data(x, column='roundTime', element=Round)
    #     df_day = pd.DataFrame(x, columns=["Unique_serial_number"])
    #     # data = df_day.values.tolist()
    #     csv_FD = []
    #     for item in tqdm(df_day['Unique_serial_number']):
    #         if item < 433:
    #             csv_result3 = search_csv(
    #                 path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/BeAMapping_replace/",
    #                 name="rec-{}-G1-2022114230_Movement_Labels".format(item))
    #             csv_FD.append(csv_result3[0])
    #
    #     ten_min_list = single_minute_fre(csv_FD, delay_time)
    #     print('前{}0分钟已处理结束'.format(i))
    #     all_time_list.append(ten_min_list)
    #
    # list_all = all_time_list
    # list_all = list(np.ravel(list_all))
    # list_all = np.array_split(list_all, len(list_all) / 14)
    # list_all = pd.DataFrame(list_all)
    # list_all = np.array(list_all)
    # list_all = normalize_2d(list_all)
    # list_all = pd.DataFrame(list_all)
    # list_all.to_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline'
    #                 '/fang_data/{}-{}_round1_{}min.csv'.format(gender, ExperimentTime, delay_time))
