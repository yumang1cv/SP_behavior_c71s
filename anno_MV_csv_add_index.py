# -*- coding:utf-8 -*-
# @FileName  :anno_MV_csv_add_index.py
# @Time      :2022/8/30 13:20
# @Author    :XuYang
import pandas as pd
import os
import tqdm

movement_dict = {'running': [29, 28, 13],
                 'walking': [14, 22, 23, 33, 26, 9, 10, 19],
                 'right_turning': [18, 17, 2, 1],
                 'left_turning': [27, 12],
                 'stepping': [5],
                 'climb_up': [31, 32, 25],
                 'rearing': [16],
                 'hunching': [24],
                 'rising': [8, 34],
                 'grooming': [37, 40, 15],
                 'sniffing': [11, 30, 35, 36, 6, 38, 4, 3],
                 'pause': [39, 20, 21],
                 'jumping': [7],
                 }

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

big_cluster = {'Locomotion': [1, 2, 3, 4, 5, 13],
               'Exploration': [11, 6, 7, 8, 9],
               'Maintenance': [10],
               'Inactive': [12]
               }

big_cluster_index = {'Locomotion': 1,
                     'Exploration': 2,
                     'Maintenance': 3,
                     'Inactive': 4
                     }


def open_data(data_path, file_type):
    file_list = []
    path_list = os.listdir(data_path)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(data_path, filename))

    return file_list


def movement_labels_index(input_data):
    # data = pd.read_csv(file_list[0])

    movement_list = list(movement_index.keys())

    movement_index_list = []

    for i in range(len(input_data)):
        for j in range(len(movement_list)):
            if input_data['new_label'][i] == movement_list[j]:
                behavior_index = movement_index[movement_list[j]]
                movement_index_list.append(behavior_index)

    input_data['new_label_index'] = movement_index_list
    input_data.insert(5, 'new_label_index', input_data.pop('new_label_index'))

    return input_data


def feature_space_index(input_data):
    movement_list = list(movement_index.keys())

    movement_index_list = []

    for i in range(len(input_data)):
        for j in range(len(movement_list)):
            if input_data['movement_label'][i] == movement_list[j]:
                behavior_index = movement_index[movement_list[j]]
                movement_index_list.append(behavior_index)

    input_data['movement_label_index'] = movement_index_list
    input_data.insert(1, 'movement_label_index', input_data.pop('movement_label_index'))

    return input_data


def big_cluster_movement_labels_rename(input_data):
    big_cluster_list = list(big_cluster.values())
    big_cluster_name_list = list(big_cluster.keys())

    big_cluster_index_list = []
    big_cluster_index_name_list = []

    for i in range(len(input_data)):
        for j in range(len(big_cluster_list)):
            if input_data['new_label_index'][i] in big_cluster_list[j]:
                behavior_cluster_index = big_cluster_index[big_cluster_name_list[j]]

                big_cluster_index_name = big_cluster_name_list[j]

                big_cluster_index_list.append(behavior_cluster_index)
                big_cluster_index_name_list.append(big_cluster_index_name)

    input_data['big_cluster_name'] = big_cluster_index_name_list
    input_data.insert(6, 'big_cluster_name', input_data.pop('big_cluster_name'))

    input_data['big_cluster_label_index'] = big_cluster_index_list
    input_data.insert(7, 'big_cluster_label_index', input_data.pop('big_cluster_label_index'))

    return input_data


def big_cluster_feature_space_rename(input_data):
    big_cluster_list = list(big_cluster.values())
    big_cluster_name_list = list(big_cluster.keys())

    big_cluster_index_list = []
    big_cluster_index_name_list = []

    for i in range(len(input_data)):
        for j in range(len(big_cluster_list)):
            if input_data['movement_label_index'][i] in big_cluster_list[j]:
                behavior_cluster_index = big_cluster_index[big_cluster_name_list[j]]

                big_cluster_index_name = big_cluster_name_list[j]

                big_cluster_index_list.append(behavior_cluster_index)
                big_cluster_index_name_list.append(big_cluster_index_name)

    input_data['big_cluster_name'] = big_cluster_index_name_list
    input_data.insert(2, 'big_cluster_name', input_data.pop('big_cluster_name'))

    input_data['big_cluster_label_index'] = big_cluster_index_list
    input_data.insert(3, 'big_cluster_label_index', input_data.pop('big_cluster_label_index'))

    return input_data


if __name__ == '__main__':
    file_list = open_data('D:/3D_behavior/Spontaneous_behavior/Sp_behavior_new/results_new/anno_MV_csv/',
                          'Movement_Labels.csv')
    file_list = sorted(file_list)

    for i in range(1, len(file_list)):
        data = pd.read_csv(file_list[i])
        # data = movement_labels_index(data)  # 修改movement_labels中behavior的index
        # data = feature_space_index(data)      # 修改feature_space中behavior的index
        data = big_cluster_movement_labels_rename(data)  # 修改movement_labels中behavior的大组index
        # data = big_cluster_feature_space_rename(data)  # 修改feature_space中behavior的大组index

        data.to_csv(file_list[i], index=False)
        print('第{}个文件已加过index, 还有{}个文件待处理'.format(i, len(file_list) - i))

    """feature_space 大组修改index"""
    # data = pd.read_csv(
    #     r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new\anno_MV_csv\rec-6-G1-anno_Feature_Space.csv')
    #
    # # data = pd.read_csv(file_list[0])
    # big_cluster_list = list(big_cluster.values())
    # big_cluster_name_list = list(big_cluster.keys())
    #
    # big_cluster_index_list = []
    # big_cluster_index_name_list = []
    #
    # for i in range(len(data)):
    #     for j in range(len(big_cluster_list)):
    #         if data['movement_label_index'][i] in big_cluster_list[j]:
    #             behavior_cluster_index = big_cluster_index[big_cluster_name_list[j]]
    #
    #             big_cluster_index_name = big_cluster_name_list[j]
    #
    #             big_cluster_index_list.append(behavior_cluster_index)
    #             big_cluster_index_name_list.append(big_cluster_index_name)
    #
    # data['big_cluster_name'] = big_cluster_index_name_list
    # data.insert(2, 'big_cluster_name', data.pop('big_cluster_name'))
    #
    # data['big_cluster_label_index'] = big_cluster_index_list
    # data.insert(3, 'big_cluster_label_index', data.pop('big_cluster_label_index'))
    #
    # data.to_csv(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new\anno_MV_csv\rec-6-G1'
    #             r'-anno_Feature_Space.csv', index=False)

    """Movement_Labels 大组修改index"""
    # data = pd.read_csv(
    #     r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new\anno_MV_csv\rec-6-G1-anno_Movement_Labels.csv')
    #
    # big_cluster_list = list(big_cluster.values())
    # big_cluster_name_list = list(big_cluster.keys())
    #
    # big_cluster_index_list = []
    # big_cluster_index_name_list = []
    #
    # for i in range(len(data)):
    #     for j in range(len(big_cluster_list)):
    #         if data['new_label_index'][i] in big_cluster_list[j]:
    #             behavior_cluster_index = big_cluster_index[big_cluster_name_list[j]]
    #
    #             big_cluster_index_name = big_cluster_name_list[j]
    #
    #             big_cluster_index_list.append(behavior_cluster_index)
    #             big_cluster_index_name_list.append(big_cluster_index_name)
    #
    # data['big_cluster_name'] = big_cluster_index_name_list
    # data.insert(6, 'big_cluster_name', data.pop('big_cluster_name'))
    #
    # data['big_cluster_label_index'] = big_cluster_index_list
    # data.insert(7, 'big_cluster_label_index', data.pop('big_cluster_label_index'))
    #
    # data.to_csv(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\results_new\anno_MV_csv\rec-6-G1'
    #             r'-anno_Movement_Labels.csv', index=False)
