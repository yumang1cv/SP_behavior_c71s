# -*- coding:utf-8 -*-
# @FileName  :looming_3Dskeleon_select.py
# @Time      :2022/6/27 11:08
# @Author    :XuYang
import pandas as pd
import os
import numpy as np


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


if __name__ == '__main__':

    looming_time = pd.read_excel('D:/3D_behavior/looming_behavior/looming_time.xlsx')

    file_list_1 = []
    for item in looming_time['video_name'][0:len(looming_time['video_name'])]:
        item = item.replace("'", "")
        item = item.replace("'", "")

        file_list1 = search_csv(
            path=r"D:/3D_behavior/looming_behavior/LiuXue_Calibrated_3DSkeleton",
            name="{}_Cali_Data3d".format(item))
        file_list_1.append(file_list1)

    file_list_1 = list(np.ravel(file_list_1))

    for i in range(len(looming_time['video_name'])):
        data_name = looming_time['video_name'].loc[i]
        data_name = data_name.replace("'", "")
        data_name = data_name.replace("'", "")

        data = pd.read_csv(file_list_1[i])
        start_time = looming_time['looming start'][i]
        end_time = start_time + 1801
        data1 = data.loc[start_time:end_time]
        data1.to_csv('D:/3D_behavior/looming_behavior/LiuXue_Calibrated_3DSkeleton/data_select/{}_Cali_Data3d.csv'.format(data_name))
