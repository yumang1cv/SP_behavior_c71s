import copy
import numpy as np

# list_row = []  # 50行
# list_column = []  # 50列，行列确定小格子所处位置
# behavior_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
#                  9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
#
# # behavior_type = [0]*14
#
# for x in range(2):
#     tmp = copy.deepcopy(behavior_type)
#     list_column.append(tmp)
#
# for x in range(2):
#     tmp = copy.deepcopy(list_column)
#     list_row.append(tmp)
#
#
# list_row[0][0][2] = 1
# (((list_row[0])[0])[2]) = 1
# print(list_row[0][0])
#
# list_column[0][4] = 5





# map_array1 = np.zeros((25, 25))
# count = 0
# for i in range(map_array1.shape[0]):
#     for j in range(map_array1.shape[1]):
#         map_array1[i][j] = count
#         count += 1
#
# map_array2 = np.zeros((25, 25))
# count = 0
# m = 24
# for i in range(map_array2.shape[0] - 1, -1, -1):
#     for j in range(map_array2.shape[1]):
#         map_array2[i][j] = count
#         count += 1
#
#
#
# def get_location_value(map_array, location, target_list):
#     index = int(map_array[location[0]][location[1]])
#     return target_list[index]
#
#
# def change_location_value(map_array, location, target_list, key, new_num):
#     index = int(map_array[location[0]][location[1]])
#     target_list[index][key] = new_num
#     return target_list
#
# behavior_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
#                  9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
# total_behavior = []
# import copy
# for i in range(25*25):
#     tmp = copy.deepcopy(behavior_type)
#     total_behavior.append(tmp)
#
# # (2, 2)
# result = change_location_value(map_array=map_array1, location=[2, 2], target_list=total_behavior, key=5, new_num=1)
# print(result)


import numpy as np

list_row = []  # 50行
list_column = []  # 50列，行列确定小格子所处位置
behavior_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

total_behavior = []
for i in range(50*50):
    tmp = copy.deepcopy(behavior_type)
    total_behavior.append(tmp)


map_array = np.zeros((50, 50))
count = 0
for i in range(map_array.shape[0] - 1, -1, -1):
    for j in range(map_array.shape[1]):
        map_array[i][j] = count
        count += 1

# you want to change[24, 24]
index = int(map_array[24][24])
total_behavior[index][5] += 1
target = total_behavior[index]
print(target)
