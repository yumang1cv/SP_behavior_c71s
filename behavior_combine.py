
"""
    fang-Spontaneous Behavior Class Combine
    1、Running:[33, 1, 2]              2、Trotting:[40, 9]                    3、Right turning:[5, 30, 14]
    4、Left turning:[6, 34, 19]        5、Jumping:[]                          6、Climbing up:[39, 11, 12]
    7、Falling:[27]                    8、Up search/Rising:[3, 19, 32, 16]    9、Grooming:[24, 21]
    10、Sniffing and Walking:[10, 35, 8, 7, 26, 38]                          11、Stepping:[25]
    12、Sniffing:[18, 20, 37, 36, 17, 4, 31, 29]                             13、Sniffing pause/Resting:[22, 15]
    14、Rearing/Diving:[28, 23, 13]
"""


"""
    fang SP behavior Correction-annoMV
    1、Running:[13, 28, 29]        2、Walking:[14, 22]       3、Right turning:[1, 2, 17, 18]
    4、Left turning:[12, 27]       5、Stepping:[5]           6、Climbing up:[25, 31, 32]
    7、Rearing:[16]                8、Hunching:[24]          9、Rising:[8, 34]
    10、Grooming:[15, 37, 40]      11、Sniffing&Walking:[9, 10, 23, 26, 33]
    11、Sniffing:[11, 30, 35, 36, 6, 38, 4, 3]               2、Up looking & walking:[19]
    12、Pause:[20, 21, 39]         13、Jumping:[7]                                     
              
"""

import pandas as pd
import os
from tqdm import tqdm

# class_label_dict = {1: [33, 1, 2], 2: [40, 9], 3: [5, 30, 14], 4: [6, 34, 19], 5: [], 6: [39, 11, 12],
#                     7: [27], 8: [3, 19, 32, 16], 9: [24, 21], 10: [10, 35, 8, 7, 26], 11: [25],
#                     12: [18, 20, 37, 36, 17, 4, 31, 29], 13: [22, 15], 14: [28, 23, 13]}
#
# # class_label_dict = {'Running': [33, 1, 2], 'Trotting': [40, 9], 'Right turning': [5, 30, 14], 'Left turning': [6, 34, 19],
# #                     'Jumping': [], 'Climbing up': [39, 11, 12], 'Falling': [27], 'Up search/Rising': [3, 19, 32, 16],
# #                     'Grooming': [24, 21], 'Sniffing and Walking': [10, 35, 8, 7, 26], 'Stepping': [25],
# #                     'Sniffing': [18, 20, 37, 36, 17, 4, 31, 29], 'Sniffing pause/Resting': [22, 15], 'Rearing/Diving': [28, 23, 13]}
# new_dict = {}
# for index, key in enumerate(class_label_dict):
#     for item in class_label_dict[key]:
#         new_dict.update({item: key})
# print(new_dict)

# class_label_dict = {33: 1, 1: 1, 2: 1, 40: 2, 9: 2, 5: 3, 30: 3, 14: 3, 6: 4, 34: 4, 19: 8, 39: 6, 11: 6, 12: 6, 27: 7,
#                     3: 8, 32: 8, 16: 8, 24: 9, 21: 9, 10: 10, 35: 10, 8: 10, 7: 10, 26: 10, 25: 11, 18: 12, 20: 12,
#                     37: 12, 36: 12, 17: 12, 4: 12, 31: 12, 29: 12, 22: 13, 15: 13, 28: 14, 23: 14, 13: 14, 38: 10}


class_label_dict = {33: 'Running', 1: 'Running', 2: 'Running', 40: 'Trotting', 9: 'Trotting', 5: 'Right turning',
                    30: 'Right turning', 14: 'Right turning', 6: 'Left turning', 34: 'Left turning',
                    19: 'Up search/Rising', 39: 'Climbing up', 11: 'Climbing up', 12: 'Climbing up', 27: 'Falling',
                    3: 'Up search/Rising', 32: 'Up search/Rising', 16: 'Up search/Rising', 24: 'Grooming',
                    21: 'Grooming', 10: 'Sniffing and Walking', 35: 'Sniffing and Walking', 8: 'Sniffing and Walking',
                    7: 'Sniffing and Walking', 26: 'Sniffing and Walking', 25: 'Stepping', 18: 'Sniffing',
                    20: 'Sniffing', 37: 'Sniffing', 36: 'Sniffing', 17: 'Sniffing', 4: 'Sniffing', 31: 'Sniffing',
                    29: 'Sniffing', 22: 'Sniffing pause/Resting', 15: 'Sniffing pause/Resting', 28: 'Rearing/Diving',
                    23: 'Rearing/Diving', 13: 'Rearing/Diving', 38: 'Sniffing and Walking'}


# class_label_dict = {value:key for key,value in class_label_dict.items()}


def open_data(data_path, file_type):
    file_list = []
    path_list = os.listdir(data_path)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(data_path, filename))

    return file_list


def rename_label(file_path):
    for file in file_path:
        with open(file, 'rb') as f:
            df = pd.read_excel(f)

    return


if __name__ == '__main__':
    file_list = open_data(
        'D:/3D_behavior/YD_bone/fang_test_YJL/results/BeAOutputs/csv_file_output/',
        'feature_space.csv')
    # file_list = open_data('D:/3D_behavior/Spontaneous_behavior/result_fang/inf_add_results/BeAMapping/',
    #                       'Movement_Labels.csv')
    # file_list = sorted(file_list, key=int)   # sort file use num
    for i in tqdm(range(0, len(file_list))):
        with open(file_list[i], 'rb') as file:
            df = pd.read_csv(file)
            first_column = df.iloc[:, 0]
            new_label = []
            for j in range(len(first_column)):
                new_label.append(class_label_dict[first_column[j]])
            # df["new_label"] = new_label
            # df.rename(columns={'new_label': new_label[0]}, inplace=True)
            df["new_label_name"] = new_label
            # df.rename(columns={'new_label_name': new_label[0]}, inplace=True)
            df.to_csv(file_list[i], index=False)

        # df1 = df.iloc[:, [0]]  # 选取第一列数据：movement label
        # df.to_csv(file_list[0], columns="B")
    # """
    #     if df1.values[i] == class_label_dict
    #     df1 add the key in second column
    # """
    #
    # for i in range(0, len(df1)):
    #     if df1['31'].values[i] in class_label_dict[1]:
    #         df1['31'].value[i] == "1"


# """
#     fang-Spontaneous Shank3B KO&WT Behavior Class Combine 0428NEW
#     1、Flight:[23,22]              2、Running:[1,31,32]                    3、Trotting:[2,16]
#     4、Walking:[11, 15, 29]        5、Stepping:[25,37]            6、Left turning:[7,8,17,24,30]
#     7、Right turning:[12,20,21]      8、Sniffing:[6,18,28,38]    9、Grooming:[9,10,19,27]
#     10、Rearing:[33]                         11、Hunching:[3,26,36]
#     12、Rising:[14,34,35,40]                           13、Climbing up:[4,39]
#     14、Pause:[5,13]
# """
#
# """
#     fang-Spontaneous Shank3B All Behavior Class Combine0511-4类
#     1、Kniematic:[1,2,3,4,5,6,7]              2、standing: [8,10,11,12,13]                    3、Grooming:[9]
#     4、Pause:[4]
# """
#
# # class_label_dict = {1: [1, 2, 3, 4, 5, 6, 7], 2: [8, 10, 11, 12, 13], 3: [9], 4: [14]}
#
# # class_label_dict = {1: [23,22] , 2: [1,31,32], 3: [2,16], 4: [11, 15, 29]  , 5: [25,37], 6: [7,8,17,24,30],
# #                     7: [12,20,21], 8: [6,18,28,38], 9: [9,10,19,27], 10: [33]  , 11: [3,26,36],
# #                     12: [14,34,35,40] , 13: [4,39],14:[5,13]}
# #
# # new_dict = {}
# # for index, key in enumerate(class_label_dict):
# #     for item in class_label_dict[key]:
# #         new_dict.update({item: key})
# # print(new_dict)
#
# import pandas as pd
# import os
# from tqdm import tqdm
#
# # class_label_dict = {33: 'Running', 1: 'Running', 2: 'Running', 40: 'Trotting', 9: 'Trotting', 5: 'Right turning',
# #                     30: 'Right turning', 14: 'Right turning', 6: 'Left turning', 34: 'Left turning',
# #                     19: 'Up search/Rising', 39: 'Climbing up', 11: 'Climbing up', 12: 'Climbing up', 27: 'Falling',
# #                     3: 'Up search/Rising', 32: 'Up search/Rising', 16: 'Up search/Rising', 24: 'Grooming',
# #                     21: 'Grooming', 10: 'Sniffing and Walking', 35: 'Sniffing and Walking', 8: 'Sniffing and Walking',
# #                     7: 'Sniffing and Walking', 26: 'Sniffing and Walking', 25: 'Stepping', 18: 'Sniffing',
# #                     20: 'Sniffing', 37: 'Sniffing', 36: 'Sniffing', 17: 'Sniffing', 4: 'Sniffing', 31: 'Sniffing',
# #                     29: 'Sniffing', 22: 'Sniffing pause/Resting', 15: 'Sniffing pause/Resting', 28: 'Rearing/Diving',
# #                     23: 'Rearing/Diving', 13: 'Rearing/Diving', 38: 'Sniffing and Walking'}
#
#
# # class_label_dict = {23: 1, 22: 1, 1: 2, 31: 2, 32: 2, 2: 3, 16: 3, 11: 4, 15: 4, 29: 4, 25: 5, 37: 5,
# #                     7: 6, 8: 6, 17: 6, 24: 6, 30: 6, 12: 7, 20: 7, 21: 7, 6: 8, 18: 8, 28: 8, 38: 8,
# #                     9: 9, 10: 9, 19: 9, 27: 9, 33: 10, 3: 11, 26: 11, 36: 11, 14: 12, 34: 12, 35: 12,
# #                     40: 12, 4: 13, 39: 13, 5: 14, 13: 14}
#
# class_label_dict = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 2, 10: 2, 11: 2, 12: 2, 13: 2, 9: 3, 14: 4}
#
#
# def open_data(data_path, file_type):
#     file_list = []
#     path_list = os.listdir(data_path)
#     for filename in path_list:
#         if file_type in filename:
#             file_list.append(os.path.join(data_path, filename))
#
#     return file_list
#
#
# def rename_label(file_path):
#     for file in file_path:
#         with open(file, 'rb') as f:
#             df = pd.read_excel(f)
#
#     return
#
#
# if __name__ == '__main__':
#     file_list = open_data(
#         'E:/Shank3B-square-SP-Looming-result/BeAMapping_Spontaneous/Sp_All_combine/',
#         'Feature_Space.csv')
#     # file_list = open_data('E:/Shank3B-square-SP-Looming-result/BeAMapping_Spontaneous/Sp_All_combine/',
#     #                       'Movement_Labels.csv')
#     # file_list = sorted(file_list, key=int)   # sort file use num
#     for i in tqdm(range(0, len(file_list))):
#         with open(file_list[i], 'rb') as file:
#             df = pd.read_csv(file)
#             first_column = df.iloc[:, 0]
#             new_label = []
#             for j in range(len(first_column)):
#                 new_label.append(class_label_dict[first_column[j]])
#             df["new_label_combine"] = new_label
#             # df.rename(columns={'new_label_combine': new_label[0]}, inplace=True)
#             # df["new_label_name"] = new_label
#             # df.rename(columns={'new_label_name': new_label[0]}, inplace=True)
#             df.to_csv(file_list[i], index=False)
#
#         # df1 = df.iloc[:, [0]]  # 选取第一列数据：movement label
#         # df.to_csv(file_list[0], columns="B")
#     # """
#     #     if df1.values[i] == class_label_dict
#     #     df1 add the key in second column
#     # """
#     #
#     # for i in range(0, len(df1)):
#     #     if df1['31'].values[i] in class_label_dict[1]:
#     #         df1['31'].value[i] == "1"
