# -*- coding:utf-8 -*-
# @FileName  :data_normlization.py
# @Time      :2022/4/19 17:56
# @Author    :XuYang
import pandas as pd

data = pd.read_excel('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/shang_value/fang/all_data.xlsx')
del data['Unnamed: 0']


data1 = (data-data.min())/(data.max()-data.min())
data1.to_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/shang_value/fang/all_data_norm.csv')