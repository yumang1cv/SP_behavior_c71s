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
#
# import pandas as pd
# import os
# from tqdm import tqdm
#
# # class_label_dict = {1: [15, 16, 35, 22], 2: [7, 31, 34], 3: [9, 21], 4: [8, 18, 23, 24, 37],
# #                     5: [3, 5, 6, 17, 19], 6: [12, 26], 7: [1, 4, 10, 13, 14, 20, 27, 28, 29, 30],
# #                     8: [39, 40], 9: [11, 25], 10: [2], 11: [36], 12: [32], 13: [33], 14: [38]}
# # new_dict = {}
# # for index, key in enumerate(class_label_dict):
# #     for item in class_label_dict[key]:
# #         new_dict.update({item:key})
# # print(new_dict)
#
# class_label_dict = {15: 1, 16: 1, 35: 1, 22: 1, 7: 2, 31: 2, 34: 2, 9: 3, 21: 3, 8: 4, 18: 4, 23: 4, 24: 4, 37: 4, 3: 5,
#                     5: 5, 6: 5, 17: 5, 19: 5, 12: 6, 26: 6, 1: 7, 4: 7, 10: 7, 13: 7, 14: 7, 20: 7, 27: 7, 28: 7, 29: 7,
#                     30: 7, 39: 8, 40: 8, 11: 9, 25: 9, 2: 10, 36: 11, 32: 12, 33: 13, 38: 14}
#
#
# # class_label_dict = {value:key for key,value in class_label_dict.items()}
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
# def replace_label(file_path):
#     with open(file_path, 'rb') as file:
#         dataframe = pd.read_csv(file)
#         # dataframe_1 = dataframe.iloc[:, [0]]  # 选取第一列数据：movement label
#
#         dataframe_2 = dataframe.iloc[:, [0]].replace({15: 1, 16: 1, 35: 1, 22: 1})  # 1、Running:[15, 16, 35, 22]
#         dataframe_2 = dataframe_2.replace({7: 2, 31: 2, 34: 2, 9: 3, 21: 3})  # 2、Right turning:[7, 31, 34]  3、Left
#         # turning:[9, 21]
#         dataframe_2 = dataframe_2.replace({8: 4, 18: 4, 23: 4, 24: 4, 37: 4})  # 4、Walking:[8, 18, 23, 24, 37]
#         dataframe_2 = dataframe_2.replace({3: 5, 5: 5, 6: 5, 17: 5, 19: 5})  # 5、Trotting:[3, 5, 6, 17, 19]
#         dataframe_2 = dataframe_2.replace({1: 7, 4: 7, 10: 7, 13: 7, 14: 7, 20: 7, 27: 7, 28: 7, 29: 7, 30: 7})
#         # 7、Sniffing:[1, 4, 10, 13, 14, 20, 27, 28, 29, 30]
#         dataframe_2 = dataframe_2.replace({12: 6, 26: 6, 39: 8, 40: 8})  # 6、Rearing:[12, 26]   8、Grooming:[39, 40]
#         dataframe_2 = dataframe_2.replace(
#             {11: 9, 25: 9, 2: 10, 36: 11})  # 9、Diving:[11, 25]  10、Rising:[2]  11、Hunching:[36]
#         dataframe_2 = dataframe_2.replace({32: 12, 33: 13, 38: 14})  # 12、Falling:[32]  13、Jumping:[33] 14、Stepping:[38]
#
#     return dataframe_2
#
#
# if __name__ == '__main__':
#     # file_list = open_data('D:/3D_behavior/Spontaneous_behavior/result/BeAMapping/BeAMapping_replace',
#     #                       'Feature_Space.csv')
#     file_list = open_data('D:/3D_behavior/Spontaneous_behavior/result/BeAMapping/BeAMapping_replace',
#                           'Movement_Labels.csv')
#     # file_list = sorted(file_list, key=int)   # sort file use num
#     for i in tqdm(range(0, len(file_list))):
#         with open(file_list[i], 'rb') as file:
#             df = pd.read_csv(file)
#             first_column = df.iloc[:, 0]
#             new_label = []
#             for j in range(len(first_column)):
#                 new_label.append(class_label_dict[first_column[j]])
#             df["new_label"] = new_label
#             df.rename(columns={'new_label': '2'}, inplace=True)
#             df.to_csv(file_list[i], index=False)
#         # df1 = df.iloc[:, [0]]  # 选取第一列数据：movement label
#         # df.to_csv(file_list[0], columns="B")
#     """
#         if df1.values[i] == class_label_dict
#         df1 add the key in second column
#     """
#
#     # for i in range(0, len(df1)):
#     #     if df1['31'].values[i] in class_label_dict[1]:
#     #         df1['31'].value[i] == "1"

# """
#     Arousal Behavior Class Combine
#     1、Right turning:[1]               2、Left turning:[26]
#     3、Sniffing:[2, 4, 10, 11, 12, 16, 22, 25]
#     4、Walking:[3, 6, 7, 19, 30]       5、Trembling:[5, 15, 32, 40]
#     6、Climbing:[8, 29]                7、Falling:[9]
#     8、Immobility:[13, 20, 33, 34]     9、Paralysis:[14, 35]
#     10、Standing:[17]                  11、Trotting:[18, 31]
#     12、Grooming:[21]                  13、Flight:[23, 38]
#     14、Running:[24, 36]               15、LORR:[27, 28, 39]
#     16、Stepping:[37]
# """
#
# import pandas as pd
# import os
# from tqdm import tqdm
#
# # class_label_dict = {1: [1], 2: [26], 3: [2, 4, 10, 11, 12, 16, 22, 25], 4: [3, 6, 7, 19, 30],
# #                     5: [5, 15, 32, 40], 6: [8, 29], 7: [9], 8: [13, 20, 33, 34], 9: [14, 35], 10: [17],
# #                     11: [18, 31], 12: [21], 13: [23, 38], 14: [24, 36], 15: [27, 28, 39], 16:[37]}
# # new_dict = {}
# # for index, key in enumerate(class_label_dict):
# #     for item in class_label_dict[key]:
# #         new_dict.update({item:key})
# # print(new_dict)
#
# class_label_dict = {1: 1, 26: 2, 2: 3, 4: 3, 10: 3, 11: 3, 12: 3, 16: 3, 22: 3,
#                     25: 3, 3: 4, 6: 4, 7: 4, 19: 4, 30: 4, 5: 5, 15: 5, 32: 5, 40: 5,
#                     8: 6, 29: 6, 9: 7, 13: 8, 20: 8, 33: 8, 34: 8, 14: 9, 35: 9, 17: 10,
#                     18: 11, 31: 11, 21: 12, 23: 13, 38: 13, 24: 14, 36: 14, 27: 15, 28: 15, 39: 15, 37: 16}
#
# # class_label_dict = {value:key for key,value in class_label_dict.items()}
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
# def replace_label(file_path):
#     with open(file_path, 'rb') as file:
#         dataframe = pd.read_csv(file)
#         # dataframe_1 = dataframe.iloc[:, [0]]  # 选取第一列数据：movement label
#
#         dataframe_2 = dataframe.iloc[:, [0]].replace({15: 1, 16: 1, 35: 1, 22: 1})  # 1、Running:[15, 16, 35, 22]
#         dataframe_2 = dataframe_2.replace({7: 2, 31: 2, 34: 2, 9: 3, 21: 3})  # 2、Right turning:[7, 31, 34]  3、Left
#         # turning:[9, 21]
#         dataframe_2 = dataframe_2.replace({8: 4, 18: 4, 23: 4, 24: 4, 37: 4})  # 4、Walking:[8, 18, 23, 24, 37]
#         dataframe_2 = dataframe_2.replace({3: 5, 5: 5, 6: 5, 17: 5, 19: 5})  # 5、Trotting:[3, 5, 6, 17, 19]
#         dataframe_2 = dataframe_2.replace({1: 7, 4: 7, 10: 7, 13: 7, 14: 7, 20: 7, 27: 7, 28: 7, 29: 7, 30: 7})
#         # 7、Sniffing:[1, 4, 10, 13, 14, 20, 27, 28, 29, 30]
#         dataframe_2 = dataframe_2.replace({12: 6, 26: 6, 39: 8, 40: 8})  # 6、Rearing:[12, 26]   8、Grooming:[39, 40]
#         dataframe_2 = dataframe_2.replace(
#             {11: 9, 25: 9, 2: 10, 36: 11})  # 9、Diving:[11, 25]  10、Rising:[2]  11、Hunching:[36]
#         dataframe_2 = dataframe_2.replace({32: 12, 33: 13, 38: 14})  # 12、Falling:[32]  13、Jumping:[33] 14、Stepping:[38]
#
#     return dataframe_2
#
#
# if __name__ == '__main__':
#     file_list = open_data('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/results_add/BeAMapping',
#                           'Feature_Space.csv')
#     # file_list = open_data('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/results_add/BeAMapping',
#     #                       'Movement_Labels.csv')
#     # file_list = sorted(file_list, key=int)   # sort file use num
#     for i in tqdm(range(0, len(file_list))):
#         with open(file_list[i], 'rb') as file:
#             df = pd.read_csv(file)
#             first_column = df.iloc[:, 0]
#             new_label = []
#             for j in range(len(first_column)):
#                 new_label.append(class_label_dict[first_column[j]])
#             df["new_label"] = new_label
#             # df.rename(columns={'new_label': new_label[0]}, inplace=True)
#             df.to_csv(file_list[i], index=False)
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


# """
#     Spontaneous Behavior Class Combine-YJL
#     1、Running:[15, 16, 22]            2、Fast walking/Trotting:[8]           3、Right turning:[7, 31, 34]
#     4、Left turning:[9, 21, 38]        5、Jumping:[33, 35]                    6、Rearing wall:[26, 12]
#     7、Grooming:[2, 39, 40]            8、Rearing:[11, 25, 32]                9、Rising:[13, 36]
#     10、Up searching:[17, 18]          11、Searching:[19, 24]                 12、Stepping:[3]
#     13、Down searching:[5, 6, 23, 24, 37]                                     14、Sniffing:[28, 27, 14, 10, 29]
#     15、Sniffing rest:[1, 4, 20, 30]
# """
#
# import pandas as pd
# import os
# from tqdm import tqdm
#
# # class_label_dict = {1: [15, 16, 22], 2: [8], 3: [7, 31, 34], 4: [9, 21, 38], 5: [33, 35], 6: [26, 12],
# #                     7: [2, 39, 40], 8: [11, 25, 32], 9: [13, 36], 10: [17, 18], 11: [19, 24], 12: [3],
# #                     13: [5, 6, 23, 24, 37], 14: [28, 27, 14, 10, 29], 15: [1, 4, 20, 30]}
# # class_label_dict = {'Running': [15, 16, 22], 'Fast_walking/Trotting': [8], 'Right_turning': [7, 31, 34],
# #                     'Left_turning': [9, 21, 38], 'Jumping': [33, 35], 'Rearing_wall': [26, 12],
# #                     'Grooming': [2, 39, 40], 'Rearing': [11, 25, 32], 'Rising': [13, 36], 'Up_searching': [17, 18],
# #                     'Searching': [19, 24], 'Stepping': [3], 'Down_searching': [5, 6, 23, 24, 37],
# #                     'Sniffing': [28, 27, 14, 10, 29], 'Sniffing_rest': [1, 4, 20, 30]}
# # new_dict = {}
# # for index, key in enumerate(class_label_dict):
# #     for item in class_label_dict[key]:
# #         new_dict.update({item: key})
# # print(new_dict)
#
# # class_label_dict = {15: 1, 16: 1, 22: 1, 8: 2, 7: 3, 31: 3, 34: 3, 9: 4, 21: 4, 38: 4, 33: 5,
# #                     35: 5, 26: 6, 12: 6, 2: 7, 39: 7, 40: 7, 11: 8, 25: 8, 32: 8, 13: 9, 36: 9,
# #                     17: 10, 18: 10, 19: 11, 24: 13, 3: 12, 5: 13, 6: 13, 23: 13, 37: 13, 28: 14,
# #                     27: 14, 14: 14, 10: 14, 29: 14, 1: 15, 4: 15, 20: 15, 30: 15}
#
# class_label_dict = {15: 'Running', 16: 'Running', 22: 'Running', 8: 'Fast_walking/Trotting', 7: 'Right_turning',
#                     31: 'Right_turning', 34: 'Right_turning', 9: 'Left_turning', 21: 'Left_turning', 38: 'Left_turning',
#                     33: 'Jumping', 35: 'Jumping', 26: 'Rearing_wall', 12: 'Rearing_wall', 2: 'Grooming', 39: 'Grooming',
#                     40: 'Grooming', 11: 'Rearing', 25: 'Rearing', 32: 'Rearing', 13: 'Rising', 36: 'Rising',
#                     17: 'Up_searching', 18: 'Up_searching', 19: 'Searching', 24: 'Down_searching', 3: 'Stepping',
#                     5: 'Down_searching', 6: 'Down_searching', 23: 'Down_searching', 37: 'Down_searching', 28: 'Sniffing',
#                     27: 'Sniffing', 14: 'Sniffing', 10: 'Sniffing', 29: 'Sniffing', 1: 'Sniffing_rest', 4: 'Sniffing_rest',
#                     20: 'Sniffing_rest', 30: 'Sniffing_rest'}
#
#
#
# # class_label_dict = {value:key for key,value in class_label_dict.items()}
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
# def replace_label(file_path):
#     with open(file_path, 'rb') as file:
#         dataframe = pd.read_csv(file)
#         # dataframe_1 = dataframe.iloc[:, [0]]  # 选取第一列数据：movement label
#
#         dataframe_2 = dataframe.iloc[:, [0]].replace({15: 1, 16: 1, 35: 1, 22: 1})  # 1、Running:[15, 16, 35, 22]
#         dataframe_2 = dataframe_2.replace({7: 2, 31: 2, 34: 2, 9: 3, 21: 3})  # 2、Right turning:[7, 31, 34]  3、Left
#         # turning:[9, 21]
#         dataframe_2 = dataframe_2.replace({8: 4, 18: 4, 23: 4, 24: 4, 37: 4})  # 4、Walking:[8, 18, 23, 24, 37]
#         dataframe_2 = dataframe_2.replace({3: 5, 5: 5, 6: 5, 17: 5, 19: 5})  # 5、Trotting:[3, 5, 6, 17, 19]
#         dataframe_2 = dataframe_2.replace({1: 7, 4: 7, 10: 7, 13: 7, 14: 7, 20: 7, 27: 7, 28: 7, 29: 7, 30: 7})
#         # 7、Sniffing:[1, 4, 10, 13, 14, 20, 27, 28, 29, 30]
#         dataframe_2 = dataframe_2.replace({12: 6, 26: 6, 39: 8, 40: 8})  # 6、Rearing:[12, 26]   8、Grooming:[39, 40]
#         dataframe_2 = dataframe_2.replace(
#             {11: 9, 25: 9, 2: 10, 36: 11})  # 9、Diving:[11, 25]  10、Rising:[2]  11、Hunching:[36]
#         dataframe_2 = dataframe_2.replace({32: 12, 33: 13, 38: 14})  # 12、Falling:[32]  13、Jumping:[33] 14、Stepping:[38]
#
#     return dataframe_2
#
#
# if __name__ == '__main__':
#     file_list = open_data(
#         'D:/3D_behavior/Spontaneous_behavior/result/BeAMapping-YJL/BeAMapping_replace',
#         'Feature_Space.csv')
#     # file_list = open_data('D:/3D_behavior/Spontaneous_behavior/result/BeAMapping-YJL/BeAMapping_replace',
#     #                       'Movement_Labels.csv')
#     # file_list = sorted(file_list, key=int)   # sort file use num
#     for i in tqdm(range(0, len(file_list))):
#         with open(file_list[i], 'rb') as file:
#             df = pd.read_csv(file)
#             first_column = df.iloc[:, 0]
#             new_label = []
#             for j in range(len(first_column)):
#                 new_label.append(class_label_dict[first_column[j]])
#             df["new_label_name"] = new_label
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
"""
    Circle-Spontaneous Behavior Class Combine-Final
    1、Running:[15, 16, 22]            2、Fast walking/Trotting:[8]           3、Right turning:[7, 31, 34]
    4、Left turning:[9, 21, 38]        5、Jumping:[33, 35]                    6、Climbing up:[26, 12]
    7、Falling:[32]                    8、Up search/Rising:[13, 36, 17, 18]   9、Grooming:[2, 39, 40]
    10、Sniffing and Walking:[5, 6, 23, 24, 37]                              11、Stepping:[3, 19]
    12、Sniffing:[28, 27, 14, 20, 29, 1]                                     13、Sniffing pause:[4, 10, 30]
    14、Rearing/Diving:[11, 25]
"""

"""
    fang-Spontaneous Behavior Class Combine
    1、Running:[33, 1, 2]              2、Trotting:[40, 9]                    3、Right turning:[5, 30, 14]
    4、Left turning:[6, 34, 19]        5、Jumping:[]                          6、Climbing up:[39, 11, 12]
    7、Falling:[27]                    8、Up search/Rising:[3, 19, 32, 16]    9、Grooming:[24, 21]
    10、Sniffing and Walking:[10, 35, 8, 7, 26, 38]                          11、Stepping:[25]
    12、Sniffing:[18, 20, 37, 36, 17, 4, 31, 29]                             13、Sniffing pause/Resting:[22, 15]
    14、Rearing/Diving:[28, 23, 13]
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
