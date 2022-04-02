import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use('Qt5Agg')

data = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area'
                   '/angle_circle_ytime_24.csv')

data1 = data.copy()
# del data1["Unnamed: 0"]
data1 = data1.drop(['Unnamed: 0'], axis=1)
time_name = ['0~10min']*24 + ['11~20min']*24 + ['21~30min']*24 + ['31~40min']*24 + ['41~50min']*24 + ['51~60min']*24
data1['time'] = time_name

# jiao_time = np.ndarray(data1['angle_time_all']).reshape(24, 6)
jiao_time = data1['angle_time_all'].tolist()
jiao_time = np.array(jiao_time).reshape(6, 24).T


bian_time = data1['circle_time_all'].tolist()
bian_time = np.array(bian_time).reshape(6, 24).T
sns.heatmap(bian_time)

sns.barplot(x="time", y="angle_time_all", data=data1)
sns.barplot(x="time", y="circle_time_all", data=data1)